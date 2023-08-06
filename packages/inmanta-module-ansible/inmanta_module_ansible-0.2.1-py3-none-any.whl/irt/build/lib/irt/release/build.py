"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import enum
import glob
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import warnings
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain
from typing import Callable, Dict, List, Optional, Set, Tuple, TypeVar

import click
import more_itertools
import requests
from packaging.requirements import Requirement, SpecifierSet
from packaging.version import Version, parse

from irt import release, util
from irt.credentials import CredentialName, CredentialStore
from irt.project import (
    DistType,
    ProductConfig,
    ProductProject,
    Project,
    ProjectConfig,
    ProjectConfigPublishRPM,
    PythonVersion,
)
from irt.release import BuildType

LOGGER = logging.getLogger(__name__)


PYTHON_DISTS_DIR: str = "dist"


def clone_product_repos(
    product_repo_url: str, branch: str, output_dir: str, token: Optional[str]
):
    os.makedirs(output_dir, exist_ok=True)
    if os.listdir(output_dir):
        raise Exception(f"Directory {output_dir} is not empty")

    # Clone product repo
    product_dir = _clone_repo(product_repo_url, branch, output_dir, token)

    config: ProductConfig = ProductProject(product_dir).get_project_config()
    for url in config.dependencies.get_all_python_component_repos().values():
        _clone_repo(url, branch, output_dir, token)


def _clone_repo(
    url: str, branch: str, output_dir: str, token: Optional[str] = None
) -> str:
    repo_name = util.get_git_repo_name_for_url(url)
    clone_dir = os.path.join(output_dir, repo_name)
    util.clone_repo(url=url, directory=clone_dir, branch=branch, token=token)
    return clone_dir


def build_python_bulk(
    directory: str,
    build_type: BuildType = BuildType.dev,
    output_dir: Optional[str] = None,
) -> None:
    """
    Build Python packages for all subdirectories of the given directory. Only setuptools projects are supported. Build artifacts
    are placed in specified output directory or in a dist subdirectory within each respective project directory if omitted.
    """
    if not os.path.isdir(directory):
        raise Exception(f"{directory} is not a directory")
    for subdir in (
        f
        for f in glob.iglob(os.path.join(os.path.abspath(directory), "*"))
        if os.path.isdir(f)
    ):
        build_python(subdir, build_type, output_dir)


def build_python(
    project_dir: str,
    build_type: BuildType = BuildType.dev,
    output_dir: Optional[str] = None,
) -> None:
    """
    Build a Python package for an Inmanta project residing in the given directory. Only setuptools projects are supported. Build
    artifacts are placed in specified output directory or in <project_dir>/dist/ if omitted.
    """
    if not os.path.isdir(project_dir):
        raise Exception(f"{project_dir} is not a directory")
    config: ProjectConfig = Project(project_dir).get_project_config()
    if config.build.python.hooks.pre is not None:
        util.subprocess_log(
            subprocess.check_output,
            [os.path.join(project_dir, config.build.python.hooks.pre)],
            logger=LOGGER,
            cwd=project_dir,
        )
    # build project and all subprojects and output them to a single directory
    if output_dir is None:
        output_dir = os.path.join(project_dir, PYTHON_DISTS_DIR)
    for directory in chain(
        [project_dir],
        (
            os.path.join(project_dir, subproject.directory)
            for _, subproject in config.build.python.subprojects.items()
        ),
    ):
        _build_python_project(
            directory,
            build_type,
            config.build.python.dists,
            config.build.python.env,
            output_dir,
            config.build.python.python_versions,
        )


def _build_python_project(
    project_dir: str,
    build_type: BuildType,
    dists: List[DistType],
    env: Dict[str, str],
    output_dir: str,
    python_versions: List[PythonVersion] = [PythonVersion.PYTHON_3],
) -> None:
    """
    Build a Python project for a Python project directory and output to the given directory.

    :param python_versions: Build a python distribution package for each of these versions of Python.
    """
    output_args: List[str] = ["-d", os.path.abspath(output_dir)]
    for python_version in python_versions:
        with tempfile.TemporaryDirectory() as tmp_dir:
            python_path = util.ensure_tmp_env(
                tmp_dir, python_version.get_name_python_binary()
            )
            # Install packages required to perform the build
            pip = build_type.get_pip(python_path=python_path)
            requirements_setup_txt = os.path.join(project_dir, "requirements.setup.txt")
            requires_files = (
                [requirements_setup_txt]
                if os.path.exists(requirements_setup_txt)
                else []
            )
            pip.install(
                pkg=["pip", "wheel", "setuptools"],
                requires_files=requires_files,
                update=True,
            )
            util.subprocess_log(
                subprocess.check_output,
                [
                    python_path,
                    "setup.py",
                    "egg_info",
                    "-Db",
                    build_type.get_build_tag_python(),
                    *chain.from_iterable([dist.value, *output_args] for dist in dists),
                ],
                logger=LOGGER,
                cwd=project_dir,
                env={**os.environ, **env},
            )


def publish_python_bulk(
    directory: str, build_type: BuildType, credentials: CredentialStore
) -> None:
    """
    Publish Python packages to the appropriate repository based on the build_type and the project's pyproject.toml.
    Publishes artifacts from each project's "dist" dir.
    """
    for subdir in (
        f
        for f in glob.iglob(os.path.join(os.path.abspath(directory), "*"))
        if os.path.isdir(f)
    ):
        if build_type == BuildType.stable:
            config: ProjectConfig = Project(subdir).get_project_config()
            if config.publish.python.public:
                publish_python_pypi(subdir, credentials)
                continue
        publish_python_devpi(subdir, build_type)


def publish_python_pypi(project_dir: str, credentials: CredentialStore) -> None:
    """
    Publish a Python package residing in a given project directory to PyPI. Build artifacts should be present in the project's
    "dist" directory.
    """
    if not os.path.isdir(project_dir):
        raise Exception(f"{project_dir} is not a directory")
    files: List[str] = list(
        chain.from_iterable(
            glob.iglob(os.path.join(project_dir, PYTHON_DISTS_DIR, f"*.{file_type}"))
            for file_type in ("whl", "tar.gz")
        )
    )
    if not files:
        raise Exception(
            f"Can't publish Python package for {project_dir}, dist directory does not contain any source artifacts."
        )
    pgp_passphrase = credentials.get_credentials_for(
        CredentialName.PGP_PASS, allow_unset=False
    )
    # Make mypy happy
    assert pgp_passphrase is not None
    pypi = PyPi(pgp_passphrase.password)
    for file in files:
        LOGGER.info("Pushing package: %s", file)
        pypi.sign_and_publish(file)


class PythonRepositoryConnector(ABC):
    """
    Abstract class for interactions with python package repositories.
    """

    def get_versions_for_package(
        self,
        package_name: str,
        version_constraint: Optional[Requirement] = None,
        allow_prereleases: bool = True,
    ) -> Set[Version]:
        """
        Return all the version of the given package that are available in the
        Python package repository. When `version_constraint` is provided, only
        return the version that match the given constraint.
        """
        versions = self.do_get_versions_for_package(package_name)
        if version_constraint:
            versions = set(ver for ver in versions if str(ver) in version_constraint)
        if not allow_prereleases:
            versions = set(ver for ver in versions if not ver.is_prerelease)
        return versions

    @abstractmethod
    def do_get_versions_for_package(self, package_name: str) -> Set[Version]:
        """
        Return all the versions of the given package that are available in the
        Python package repository.
        """
        raise NotImplementedError()


class PyPi(PythonRepositoryConnector):
    def __init__(self, pgp_passphrase: Optional[str] = None) -> None:
        self._pgp_passphrase: Optional[str] = pgp_passphrase

    def sign_and_publish(self, file: str) -> None:
        """
        Sign the given package and upload both the package and the signature to pypi.
        No upload is done when the given package already exists on pypi.

        Requirements:
            * The `TWINE_USERNAME` and `TWINE_PASSWORD` environment variables
              have to be set for this method to work properly.
            * The PGP passphrase has to be provided via the `gpg_passphrase` argument
              in the constructor.
        """
        if os.getenv("TWINE_USERNAME") is None or os.getenv("TWINE_PASSWORD") is None:
            raise Exception(
                "TWINE_USERNAME, TWINE_PASSWORD environment variables must be set to be able to publish to PyPI."
            )
        package_name, package_version = self._extract_name_and_version_from_file(file)
        if self.has_package(package_name, package_version):
            warnings.warn(
                f"Package {file} not published because a published package was found with the same version"
            )
            return
        signature_file = self._generate_signature(file)
        self._upload_package(file, signature_file)
        self._wait_pkg_becomes_available_on_pypi(package_name, package_version)
        self._sync_devpi_mirror_with_pypi(package_name)

    def _extract_name_and_version_from_file(self, file) -> Tuple[str, str]:
        match_tar: Optional[re.Match] = re.fullmatch(
            r"(.*)-([^-]*)\.tar\.gz", os.path.basename(file)
        )
        if match_tar and len(match_tar.groups()) == 2:
            package_name = match_tar[1]
            package_version = match_tar[2]
            return package_name, package_version

        match_whl: Optional[re.Match] = re.fullmatch(
            r"([^-]*)-([^-]*)-.*\.whl", os.path.basename(file)
        )
        if match_whl and len(match_whl.groups()) == 2:
            # The naming sheme of wheels uses _ in the package name as opposed to tarball that uses -.
            # The package name needs to be converted to use "-" as this is later used for queries.
            package_name = match_whl[1].replace("_", "-")
            package_version = match_whl[2]
            return package_name, package_version

        raise Exception(f"Could not parse {file} package and version")

    def _generate_signature(self, file: str) -> str:
        """
        :return: The path to the generated signature file.
        """
        if self._pgp_passphrase is None:
            raise Exception(
                "No pgp passphrase was set. Provide it to the constructor via the "
                "pgp_passphrase argument."
            )
        util.subprocess_log(
            subprocess.check_output,
            [
                "gpg",
                "--pinentry-mode",
                "loopback",
                "-u",
                "code@inmanta.com",
                "--passphrase",
                self._pgp_passphrase,
                "--detach-sign",
                "--batch",
                "--yes",
                "-a",
                file,
            ],
            logger=LOGGER,
        )
        return f"{file}.asc"

    def _upload_package(self, *files_to_upload) -> None:
        util.subprocess_log(
            subprocess.check_output,
            [
                sys.executable,
                "-m",
                "twine",
                "upload",
                *files_to_upload,
            ],
            logger=LOGGER,
        )

    def has_package(self, package_name: str, version: str) -> bool:
        pkg_metadata_json = self._get_pypi_package_json(package_name)
        if pkg_metadata_json is None:
            return False
        return version in pkg_metadata_json["releases"]

    def _wait_pkg_becomes_available_on_pypi(
        self, package_name: str, version: str, timeout_sec: int = 60
    ) -> None:
        """
        After publishing a package to pypi, it take a few moments until pypi
        reaches internal consistency. This method does a polling wait until
        pypi reaches internal consistency.
        """
        now = time.time()
        pkg_is_available = False
        LOGGER.info(
            "Waiting until package %s with version %s becomes available on pypi",
            package_name,
            version,
        )
        while not pkg_is_available and time.time() < now + timeout_sec:
            if self.has_package(package_name, version):
                pkg_is_available = True
            else:
                time.sleep(1)
        if not pkg_is_available:
            raise Exception(
                f"Timeout waiting for package {package_name} with version {version} to become available on pypi"
            )

    def _sync_devpi_mirror_with_pypi(self, package_name: str) -> None:
        """
        Force synchronization between the internal devpi mirror and
        the upstream pypi for a specific package.
        """
        url = f"https://artifacts.internal.inmanta.com/root/pypi/+simple/{package_name}/refresh"
        response = requests.post(url, timeout=10)
        if response.status_code != 200:
            raise Exception(
                f"Refresh request to {url} failed with status code {response.status_code}: {response.content}"
            )

    def _get_pypi_package_json(self, package_name: str) -> Optional[Dict[str, object]]:
        response: requests.Response = requests.get(
            f"https://pypi.org/pypi/{package_name}/json",
            timeout=10,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise Exception(
                f"Failed to process data for {package_name} PyPI package."
            ) from e

    def do_get_versions_for_package(self, package_name: str) -> Set[Version]:
        """
        Return all the versions of the given package that are available in the
        Python package repository.
        """
        result: Optional[Dict[str, object]] = self._get_pypi_package_json(package_name)
        if not result:
            return set()
        return set(Version(ver) for ver in result["releases"].keys())


class Devpi(PythonRepositoryConnector):
    def __init__(self, url: str) -> None:
        """
        :param url: The URL to the index this instance should interact with.
                    For example: https://artifacts.internal.inmanta.com/inmanta/dev)
        """
        if url.endswith("/"):
            url = url[0:-1]
        self.url = url

    def _get_url_for_package(self, package_name: str) -> str:
        return f"{self.url}/{package_name}"

    def do_get_versions_for_package(self, package_name: str) -> Set[Version]:
        """
        Return all the versions of the given package that are available in the
        Python package repository.
        """
        json_response: Optional[
            Dict[str, object]
        ] = self._get_json_metadata_for_package(package_name)
        if not json_response:
            return set()
        return set(Version(ver) for ver in json_response["result"].keys())

    def _get_json_metadata_for_package(
        self, package_name: str
    ) -> Optional[Dict[str, object]]:
        """
        Return the metadata for the given package as a dictionary. None is returned when
        no package with the given name exists.
        """
        url = self._get_url_for_package(package_name)
        headers = {"Accept": "application/json"}
        response: requests.Response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to process response for {url}") from e

    def download_universal_wheel(
        self, package_name: str, version: Version, destination_dir: str
    ) -> str:
        """
        Download the given version of a package as a universal wheel to the given destination directory.

        :return: The path to the downloaded wheel
        :raises Exception: No universal wheel exists with given package name and version.
        """
        version_str = str(version)
        json_response = self._get_json_metadata_for_package(package_name)
        if not json_response or not json_response["result"].get(version_str):
            raise Exception(
                f"Package {package_name} with version {version_str} doesn't exist in {self.url}"
            )
        link_to_universal_wheel = more_itertools.one(
            [
                link["href"]
                for link in json_response["result"][version_str]["+links"]
                if link["href"].endswith("-py3-none-any.whl")
            ],
            too_short=Exception(
                f"No universal wheel exists for {package_name}=={version_str} on {self.url}"
            ),
            too_long=Exception(
                f"More than one universal wheel found for {package_name}=={version_str} on {self.url}"
            ),
        )
        file_name = link_to_universal_wheel.rsplit("/", maxsplit=1)[-1]
        file_path = os.path.join(destination_dir, file_name)
        with urllib.request.urlopen(link_to_universal_wheel) as response:
            with open(file_path, "wb") as fh:
                shutil.copyfileobj(response, fh)
        return file_path


class PythonPackageSpec:
    def __init__(self, pkg_dir: str, file_name_sdist: str) -> None:
        self.pkg_name: str = util.get_name_python_project(pkg_dir)
        self.short_version: str = util.get_version_python_project(pkg_dir)
        pattern = f"{self.pkg_name}-{self.short_version}(\\.dev[^-]*|rc[^-]*|)\\.tar.gz"
        match: Optional[re.Match] = re.search(pattern, file_name_sdist)
        if match is None or len(match.groups()) != 1:
            raise Exception(f"Could not parse build_tag from {file_name_sdist}")
        self.build_tag: str = match[1]
        self.full_version: str = f"{self.short_version}{self.build_tag}"
        self.rpm_build_tag: str = self._get_rpm_build_tag(self.build_tag)

    @classmethod
    def _get_rpm_build_tag(cls, build_tag) -> str:
        if "rc" in build_tag:
            return f".{build_tag.replace('rc', 'next')}"
        return build_tag


def publish_python_devpi(project_dir: str, build_type: BuildType) -> None:
    """
    Publish a Python package residing in a given project directory to devpi. Build artifacts should be present in the project's
    "dist" directory.
    """
    if not os.path.isdir(project_dir):
        raise Exception(f"{project_dir} is not a directory")
    if not any(
        True for _ in glob.iglob(os.path.join(project_dir, PYTHON_DISTS_DIR, "*.whl"))
    ):
        raise Exception(
            f"Can't publish Python package for {project_dir}, dist directory does not contain any wheels"
        )

    def devpi_cli(*args: str) -> str:
        return util.subprocess_log(
            subprocess.check_output,
            [sys.executable, "-m", "devpi", *args],
            logger=LOGGER,
        ).decode()

    devpi_cli(
        "use", f"https://artifacts.internal.inmanta.com/inmanta/{build_type.value}"
    )
    try:
        devpi_cli(
            "login",
            os.environ["DEVPI_USER"],
            "--password=%s" % os.environ["DEVPI_PASS"],
        )
    except KeyError:
        raise Exception(
            "DEVPI_USER and DEVPI_PASS environment variables must be set to be able to publish to devpi."
        )
    for wheel in glob.iglob(os.path.join(project_dir, PYTHON_DISTS_DIR, "*.whl")):
        match: Optional[re.Match] = re.search(
            "([^-]*)-([^-]*)-.*\\.whl", os.path.basename(wheel)
        )
        if match is None or len(match.groups()) != 2:
            raise Exception(f"Could not parse {wheel} package and version")
        lst: str
        try:
            lst = devpi_cli("list", "%s==%s" % (match[1], match[2]))
        except subprocess.CalledProcessError:
            # no versions have been published yet for this package
            lst = ""
        if lst.strip() == "":
            devpi_cli(
                "upload",
                *glob.glob(
                    os.path.join(project_dir, PYTHON_DISTS_DIR, f"*{match[2]}*")
                ),
            )
        else:
            warnings.warn(
                f"Wheel {wheel} not published because a published package was found with the same version"
            )
    devpi_cli("logoff")


class NPMRepoConnectorGitHub:
    def __init__(self, token: Optional[str]):
        self._authenticate_to_github_npm_repository(token)

    def download_npm_package(
        self,
        git_repo_url: str,
        version_constraint: str,
        build_type: BuildType,
        output_dir: str,
    ) -> str:
        """
        :return: Return the version of the downloaded NPM package
        """
        npm_repo_path = self._convert_git_url_to_npm_repo_path(git_repo_url)
        if version_constraint == "master":
            if build_type != BuildType.dev:
                raise Exception(
                    f"Release type {build_type.value} cannot be used when the version "
                    f"constraint of {git_repo_url} is set to master"
                )
            version_to_download = self._get_version_latest_dev_release(npm_repo_path)
        elif re.fullmatch(r"==\d+\.\d+\.\d+", version_constraint):
            version_to_download = version_constraint[2:]
        elif re.fullmatch(r"~=\d+\.\d+(\.\d+)?(\.\d+)?(rc)?", version_constraint):
            version_to_download = self._get_latest_version_matching_constraint(
                version_constraint, npm_repo_path, build_type
            )
        else:
            raise Exception(
                f"Invalid version constraint ({version_constraint}) specified for NPM "
                f"package {npm_repo_path}. Expected: ['master', '==x.y.z', '~=x.y.z', '~=x.y']"
            )
        return self._download_npm_package(
            npm_repo_path, version_to_download, output_dir
        )

    def _get_latest_version_matching_constraint(
        self, version_constraint: str, npm_repo_path: str, build_type: BuildType
    ) -> str:
        specifier_set = self._get_specifier_set(version_constraint, build_type)
        all_versions: List[str] = self._get_all_versions_for_pkg(npm_repo_path)
        parsed_versions: Dict[Version, str] = {
            parse(v.replace("-next", "-rc")): v for v in all_versions
        }
        filtered_versions = {
            x: y
            for x, y in parsed_versions.items()
            if specifier_set.contains(x, prereleases=not build_type.is_stable_release())
        }
        if len(filtered_versions) == 0:
            raise Exception(
                f"No matching version found for NPM package {npm_repo_path} with constraint {version_constraint}"
            )
        latest_matching_version = sorted(filtered_versions.keys())[-1]
        return filtered_versions[latest_matching_version]

    def _get_all_versions_for_pkg(self, npm_repo_path: str) -> List[str]:
        cmd = ["npm", "view", f"@{npm_repo_path}", "versions", "--json"]
        return json.loads(subprocess.check_output(cmd).decode("utf-8").strip())

    def _get_specifier_set(
        self, version_constraint: str, build_type: BuildType
    ) -> SpecifierSet:
        if build_type.is_dev_release():
            # Ensure that specifier includes dev releases
            version_constraint = f"{version_constraint}.dev"
        requirement = Requirement(f"pkg{version_constraint}")
        return requirement.specifier

    def _convert_git_url_to_npm_repo_path(self, git_repo_url: str) -> str:
        splitted_url = git_repo_url.strip().split("/")
        org_name = splitted_url[-2]
        repo_name = splitted_url[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[0:-4]
        return f"{org_name}/{repo_name}"

    def _authenticate_to_github_npm_repository(
        self, github_token: Optional[str]
    ) -> None:
        # Set URL to NPM repository
        cmd = [
            "npm",
            "config",
            "set",
            "@inmanta:registry",
            "https://npm.pkg.github.com",
        ]
        util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)
        # Set auth token
        if github_token is not None:
            cmd = [
                "npm",
                "config",
                "set",
                "//npm.pkg.github.com/:_authToken",
                github_token,
            ]
            util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)

    def _get_version_latest_dev_release(self, npm_repo: str) -> str:
        cmd = ["npm", "view", f"@{npm_repo}", "--json"]
        output_str: str = subprocess.check_output(cmd).decode("utf-8")
        output_dct: dict = json.loads(output_str)
        return output_dct["dist-tags"]["dev"]

    def _download_npm_package(
        self, npm_repo: str, version_constraint: str, output_dir: str
    ) -> str:
        cmd = ["npm", "pack", f"@{npm_repo}@{version_constraint}"]
        pkg_file_name = (
            util.subprocess_log(
                subprocess.check_output, cmd, logger=LOGGER, cwd=output_dir
            )
            .decode("utf-8")
            .strip()
        )
        return self._extract_version_from_pkg_file(npm_repo, pkg_file_name)

    def _extract_version_from_pkg_file(self, npm_repo: str, pkg_file_name: str) -> str:
        pattern = f"{npm_repo.replace('/', '-')}-(.*)\\.tgz"
        match: Optional[re.Match] = re.search(pattern, pkg_file_name)
        if match is None:
            raise Exception(f"Couldn't extract version from filename {pkg_file_name}")
        return match[1]


def build_rpm(
    product_git_url: str,
    branch: str,
    build_type: BuildType,
    centos_version: int,
    output_dir: str,
    token: Optional[str],
):
    # Create output dir
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    if os.listdir(output_dir):
        raise Exception(f"output directory {output_dir} is not empty")

    # Clone product repo
    product_directory = os.path.join(output_dir, "product")
    util.clone_repo(product_git_url, product_directory, branch, token)
    path_spec_file = os.path.join(product_directory, "inmanta.spec")
    if not os.path.isfile(path_spec_file):
        raise Exception(f"No spec file found at {path_spec_file}")
    source_dir = os.path.join(output_dir, "sources")

    product_config: ProductConfig = ProductProject(
        product_directory
    ).get_project_config()
    python_version_rpm_venv = product_config.build.rpm.python_version

    defines = {}

    # Download the product pypi package
    sdist = get_product_pypi_package_from_repo(
        product_directory, build_type, source_dir, python_version_rpm_venv
    )
    python_package_spec = PythonPackageSpec(product_directory, os.path.basename(sdist))
    defines["release"] = str(build_type.get_rpm_release_number())
    defines["version"] = python_package_spec.short_version
    defines["buildid"] = python_package_spec.rpm_build_tag
    defines["buildid_egg"] = python_package_spec.build_tag
    defines["python_version"] = python_version_rpm_venv.get_version_number()

    # Add dependencies.tar.gz to sources directory
    dependencies_tar = os.path.join(source_dir, "dependencies.tar.gz")

    product_lock_file = os.path.join(product_directory, "requirements.txt")
    lock_file_repo_clone_dir = os.path.join(output_dir, "lock_file_repos")
    additional_lock_files = product_config.clone_additional_lock_file_repos(
        lock_file_repo_clone_dir, branch, token
    )
    all_lock_files = [product_lock_file] + additional_lock_files

    package_dependencies_multi(
        product_directory,
        all_lock_files,
        dependencies_tar,
        allow_pre_releases_inmanta_pkgs=build_type.is_dev_release(),
        python_version=python_version_rpm_venv,
    )

    # Download NPM packages
    npm_repo_connector = NPMRepoConnectorGitHub(token)
    for current_dep in product_config.dependencies.npm:
        npm_dependency = product_config.dependencies.npm[current_dep]
        git_repo_url = npm_dependency.repo
        version_constraint = npm_dependency.version
        version_npm_package = npm_repo_connector.download_npm_package(
            git_repo_url, version_constraint, build_type, output_dir=source_dir
        )
        repo_name = util.get_git_repo_name_for_url(git_repo_url)
        defines[f"{repo_name.replace('-', '_')}_version"] = version_npm_package

    # Get enable_rpm_repos
    enable_repo_config = product_config.build.rpm.enable_repo
    if f"el{centos_version}" in enable_repo_config:
        enable_rpm_repos = enable_repo_config[f"el{centos_version}"]
    else:
        enable_rpm_repos = []

    # Build RPM files
    rpms_dir = os.path.join(output_dir, "rpms")
    os.mkdir(rpms_dir)
    mock_srpm_and_rpm(
        chroot_config=f"inmanta-and-epel-{centos_version}-x86_64",
        spec_file=path_spec_file,
        sources=source_dir,
        out_dir=rpms_dir,
        enable_rpm_repos=enable_rpm_repos,
        defines=defines,
    )


def get_product_pypi_package_from_repo(
    product_directory: str,
    build_type: BuildType,
    source_dir: str,
    python_version: PythonVersion,
) -> str:
    package_name = util.get_name_python_project(product_directory)
    version_constraint = release.get_version_constraint_on_product(
        product_directory, build_type
    )
    with tempfile.NamedTemporaryFile() as fp:
        fp.write(version_constraint.encode())
        fp.flush()
        download_dependencies(
            source_dir,
            [package_name],
            constraint_file=fp.name,
            allow_pre_releases=build_type != BuildType.stable,
            python_version=python_version,
        )
    sdist = glob.glob(os.path.join(source_dir, "*.tar.gz"))
    if len(sdist) == 0:
        raise Exception(f"No sdist found in {source_dir}")
    if len(sdist) > 1:
        raise Exception(f"More than one sdist found in {source_dir}")
    return sdist[0]


def mock_srpm_and_rpm(
    chroot_config: str,
    spec_file: str,
    sources: str,
    out_dir: str,
    enable_rpm_repos: List[str] = [],
    defines: Dict[str, str] = {},
) -> List[str]:
    LOGGER.info(
        "Running mock_srpm_and_rpm (chroot_config: %s, spec_file: %s, sources: %s, "
        "out_dir: %s, enable_rpm_repos: %s, defines: %s",
        chroot_config,
        spec_file,
        sources,
        out_dir,
        enable_rpm_repos,
        defines,
    )
    path_srpm_file: str = mock_srpm(
        chroot_config, spec_file, sources, out_dir, enable_rpm_repos, defines
    )
    return mock_rpm(
        chroot_config,
        path_srpm_file,
        out_dir,
        defines,
        enable_rpm_repos,
    )


def mock_srpm(
    chroot_config: str,
    spec_file: str,
    sources: str,
    out_dir: str,
    enable_rpm_repos: List[str] = [],
    defines: Dict[str, str] = {},
) -> str:
    if os.listdir(out_dir):
        raise Exception(f"Output directory {out_dir} is not empty")
    cmd = [
        "mock",
        "--no-bootstrap-chroot",
        "--dnf",
        "-r",
        chroot_config,
        "--buildsrpm",
        "--spec",
        spec_file,
        "--sources",
        sources,
        "--resultdir",
        out_dir,
    ]
    if enable_rpm_repos:
        repos_joined = ",".join(enable_rpm_repos)
        cmd.extend([f"--enablerepo={repos_joined}"])
    for key, value in defines.items():
        if not value:
            cmd.extend(["-D", f"{key} %{{nil}}"])
        else:
            cmd.extend(["-D", f"{key} {value}"])

    LOGGER.debug("Running mock for srpm: %s", " ".join(cmd))
    util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)

    srpm = glob.glob(os.path.join(out_dir, "*.src.rpm"))
    if not srpm:
        click.echo(
            f"No *.src.rpm file found in output directory {out_dir}",
            err=True,
        )
        sys.exit(1)
    if len(srpm) != 1:
        click.echo(
            "Build srpm generated %d *.src.rpm files, confused, quitting" % len(srpm),
            err=True,
        )
        sys.exit(1)

    return srpm[0]


def mock_rpm(
    chroot_config: str,
    srpm_file: str,
    out_dir: str,
    defines: Dict[str, str] = {},
    enable_rpm_repos: List[str] = [],
) -> List[str]:
    if not os.path.isfile(srpm_file):
        raise Exception(f"srpm file {srpm_file} not found")
    cmd = [
        "mock",
        "--no-bootstrap-chroot",
        "--dnf",
        "-r",
        chroot_config,
        "--rebuild",
        srpm_file,
        "--resultdir",
        out_dir,
    ]
    if enable_rpm_repos:
        repos_joined = ",".join(enable_rpm_repos)
        cmd.extend([f"--enablerepo={repos_joined}"])
    for key, value in defines.items():
        if not value:
            cmd.extend(["-D", f"{key} %{{nil}}"])
        else:
            cmd.extend(["-D", f"{key} {value}"])

    LOGGER.debug("Running mock for rpm: %s", " ".join(cmd))
    util.subprocess_log(subprocess.check_call, cmd, logger=LOGGER)

    rpms = glob.glob(os.path.join(out_dir, "*.rpm"))
    return [r for r in rpms if r.endswith(".src.rpm")]


def package_dependencies(
    package_dir: str,
    constraint_file: str,
    destination: str,
    allow_pre_releases_inmanta_pkgs: bool,
):
    package_dependencies_multi(
        package_dir,
        [constraint_file],
        destination,
        allow_pre_releases_inmanta_pkgs,
    )


def package_dependencies_multi(
    package_dir: str,
    constraint_files: List[str],
    destination: str,
    allow_pre_releases_inmanta_pkgs: bool,
    python_version: PythonVersion = PythonVersion.PYTHON_3,
):
    """
    :param python_version: Package dependencies that work using this version of python.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        _package_dependencies_multi(
            tmp_dir,
            package_dir,
            constraint_files,
            destination,
            allow_pre_releases_inmanta_pkgs,
            python_version=python_version,
        )


def _package_dependencies_multi(
    tmp_dir: str,
    package_dir: str,
    constraint_files: List[str],
    destination: str,
    allow_pre_releases_inmanta_pkgs: bool,
    python_version: PythonVersion = PythonVersion.PYTHON_3,
):
    """
    Package dependencies for a list of constraint files.
    """
    freeze_file_with_all_dependencies = os.path.join(tmp_dir, "requirements.txt")
    freeze_file_generator = FreezeFileGenerator(
        project_dir=package_dir,
        min_c_constraint_files=constraint_files,
        min_r_constraint_files=constraint_files,
        python_version=python_version,
    )
    freeze_file_generator.write_freeze_file_with_all_dependencies(
        output_file=freeze_file_with_all_dependencies,
        allow_pre_releases_inmanta_pkgs=allow_pre_releases_inmanta_pkgs,
    )
    dep_packages = get_package_names_from_freeze_file(freeze_file_with_all_dependencies)

    # Create dependencies directory
    deps_dir = os.path.join(tmp_dir, "dependencies")
    util.ensure_dir(deps_dir)

    # Download packages
    download_dependencies(
        deps_dir,
        dep_packages,
        constraint_file=freeze_file_with_all_dependencies,
        python_version=python_version,
    )

    # Package dependencies dir
    with tarfile.open(destination, "w:gz") as tar:
        tar.add(deps_dir, os.path.basename(deps_dir))


def get_package_names_from_freeze_file(requirements_file: str) -> List[str]:
    result = []
    with open(requirements_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(line.split("==")[0])
    return result


def create_spec_file(build_context, spec_file_template):
    with open(spec_file_template, "r") as fd:
        spec = fd.read()

    spec = re.sub("%define version.*", "%define version " + build_context.version, spec)
    if not build_context.release:
        spec = re.sub("%define release.*", "%define release 0", spec)
        spec = "%define buildid " + build_context.build_id + "\n" + spec

    with open(
        os.path.join(
            build_context.destination_dir, os.path.basename(spec_file_template)
        ),
        "w+",
    ) as fd:
        fd.write(spec)


def download_dependencies(
    deps_dir: str,
    pkgs: List[str],
    constraint_file: Optional[str] = None,
    allow_pre_releases=False,
    python_version: PythonVersion = PythonVersion.PYTHON_3,
):
    """This command will download each dependency listed in the requirements file as source packages. It does
    some tricks to speed up the process. By default pip download will create an isolated build environment in
    which it installs all build dependencies. This is a really slow process, because of the no-binary because
    it will have to install everything from source.

    To bypass this we create a virtual env that contains the dependencies that make the process slow
    (40 minutes vs < 1m). This list has to be maintained and might change in the future. Then it disables
    the build isolation.

    :param python_version: Download the dependencies that can be installed using this version of Python.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        python_path = util.ensure_tmp_env(
            tmp_dir, python_binary=python_version.get_name_python_binary()
        )
        python_path_pkgs = ["wheel", "pip", "setuptools", "setuptools_rust"]
        util.pip_install(
            python_path,
            python_path_pkgs,
            update=True,
            constraint_files=[constraint_file] if constraint_file is not None else [],
        )
        for pkg in pkgs:
            _download_dependencies(
                python_path,
                deps_dir,
                pkg,
                constraint_file=constraint_file,
                allow_pre_releases=allow_pre_releases,
            )


def _download_dependencies(
    python_path: str, deps_dir, pkg, constraint_file=None, allow_pre_releases=False
):
    LOGGER.info("Downloading dependency: %s", pkg)
    cmd = [python_path, "-m", "pip", "download", "--no-build-isolation"]
    if allow_pre_releases:
        cmd.append("--pre")
    if constraint_file is not None:
        cmd.extend(["-c", constraint_file])
    cmd.extend(["-d", deps_dir, "--no-deps"])

    pkg_downloaded = False
    exc = None
    # Download source package
    try:
        util.subprocess_log(
            subprocess.check_output,
            cmd + ["--no-binary", ":all:", pkg],
            logger=LOGGER,
            stderr=subprocess.STDOUT,
        )
        pkg_downloaded = True
    except subprocess.CalledProcessError:
        LOGGER.debug("Could not download '%s' as a source package.", pkg)

    # Download universal wheel
    try:
        util.subprocess_log(
            subprocess.check_output,
            cmd + ["--platform", "any", "--only-binary", ":all:", pkg],
            logger=LOGGER,
            stderr=subprocess.STDOUT,
        )
        pkg_downloaded = True
    except subprocess.CalledProcessError as e:
        exc = e
        LOGGER.debug("Could not download '%s' as a wheel.", pkg)

    if pkg_downloaded:
        return
    elif not pkg.startswith("inmanta"):
        print(exc.output)
        raise Exception(f"Failed to download package {pkg}") from exc
    else:
        # Inmanta packages can use binary wheels
        try:
            util.subprocess_log(
                subprocess.check_output,
                cmd + ["--platform", "linux_x86_64", pkg],
                logger=LOGGER,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise e


def publish_rpm(
    product_repo: str,
    branch: str,
    rpm_directory: str,
    build_type: BuildType,
    git_token: Optional[str],
    cloudsmith_api_key: str,
):
    config: ProductConfig = ProductProject.get_project_config_from_git_repo(
        product_repo, branch, git_token
    )
    if config.publish.rpm.rpm_repo_name_prefix is None:
        raise Exception(
            "Field `rpm_repo_name_prefix` missing in section [tool.irt.publish.rpm]"
        )
    rpm_files = glob.glob(os.path.join(rpm_directory, "*.x86_64.rpm"))
    rpm_repo_connector = CloudsmithRPMPublisher(
        config.publish.rpm, build_type, cloudsmith_api_key
    )
    rpm_repo_connector.publish_and_promote_rpms(rpm_files)


class CloudsmithPackageFormat(enum.Enum):
    """
    The format of a package stored Cloudsmith.
    """

    RPM = "rpm"
    PYTHON = "python"


@dataclass(init=True, frozen=True)
class CloudsmithPackage:
    """
    Data object that contains information about a package stored
    on a Cloudsmith repository:

    :param filename: The filename of the artifact.
    :param identifier_perm: A unique ID for the package.
    :param version: The version of the artifact.
    """

    filename: str
    identifier_perm: str
    version: str


T = TypeVar("T")


class Cloudsmith(PythonRepositoryConnector):
    """
    Class that provides the logic to interact with a Cloudsmith repository.
    """

    def __init__(self, repository: str, cloudsmith_api_key: str) -> None:
        """
        :param repository: The specific repository on cloudsmith that should be considered
                           by the new instance. This string should follow the pattern
                           <OWNER>/<REPO_NAME> (example: inmanta/oss-dev).
        :param cloudsmith_api_key: API key to authenticate the requests sent to Cloudsmith.
        """
        self.repository = repository
        self.cloudsmith_api_key = cloudsmith_api_key

    def publish_rpms(self, rpm_files: List[str]) -> None:
        """
        Publish the given list of RPMs to cloudsmith.
        """
        for rpm in rpm_files:
            cmd = [
                sys.executable,
                "-m",
                "cloudsmith_cli",
                "push",
                "rpm",
                self._get_rpm_repo_push_path(rpm),
                rpm,
            ]
            self._execute_command(subprocess.check_call, cmd)

    def publish_python_package(self, path_to_package: str) -> None:
        """
        Publish the given Python package to cloudsmith.
        """
        cmd = [
            sys.executable,
            "-m",
            "cloudsmith_cli",
            "push",
            "python",
            self.repository,
            path_to_package,
        ]
        self._execute_command(subprocess.check_call, cmd)

    def _get_rpm_repo_push_path(self, rpm_file: str) -> str:
        """
        Return the fully qualified path to the RPM repository for the given RPM file.
        The returned path contains: <OWNER>/<REPOSITORY>/el/<CENTOS-VERSION>
        """
        match = re.fullmatch(r".*\.el(\d+)\.x86_64\.rpm", rpm_file)
        if match is None:
            raise Exception(
                f"Couldn't extract centos version from RPM filename ({rpm_file})"
            )
        centos_version = match[1]
        return f"{self.repository}/el/{centos_version}"

    def list_packages(
        self,
        pkg_name: Optional[str] = None,
        pkg_format: Optional[CloudsmithPackageFormat] = None,
    ) -> List[CloudsmithPackage]:
        """
        Returns a list of CloudsmithPackages that match the given name and
        package format. When the `pkg_format` argument is None, it is ignored.
        """
        list_cmd = [
            sys.executable,
            "-m",
            "cloudsmith_cli",
            "list",
            "packages",
            self.repository,
            "-F",
            "json",
        ]
        query = []
        if pkg_name:
            query.append(f"name:^{pkg_name}$")
        if pkg_format:
            query.append(f"format:{pkg_format.value}")
        if query:
            list_cmd.extend(["--query", " ".join(query)])
        output_raw = self._execute_command(subprocess.check_output, list_cmd).decode(
            "utf-8"
        )
        output = json.loads(output_raw)
        return [
            CloudsmithPackage(
                filename=pkg_spec["filename"],
                identifier_perm=pkg_spec["identifier_perm"],
                version=pkg_spec["version"],
            )
            for pkg_spec in output["data"]
        ]

    def copy_package(self, identifier_perm: str, destination_repo: str) -> None:
        """
        Copy the package identified by `identifier_perm` to the given destination repository.

        :param identifier_perm: Unique identifier of a package as returned by the Cloudsmith API.
        :param destination_repo: The name of the destination repo not prefixed with the owner.
                                 Example: oss-stable (and not inmanta/oss-stable).
        """
        pkg_path = f"{self.repository}/{identifier_perm}"
        copy_cmd = [
            sys.executable,
            "-m",
            "cloudsmith_cli",
            "copy",
            pkg_path,
            destination_repo,
        ]
        self._execute_command(subprocess.check_call, copy_cmd)

    def _execute_command(self, subprocess_f: Callable[..., T], cmd: List[str]) -> T:
        """
        Execute a command. This method ensures that:
            * The CLOUDSMITH_API_KEY environment is provided to the command
            * The output to the command is logged.
        """
        return util.subprocess_log(
            subprocess_f,
            cmd,
            logger=LOGGER,
            env=self._get_env_vars_for_cloudsmith_cli(),
        )

    def _get_env_vars_for_cloudsmith_cli(self) -> Dict[str, str]:
        """
        Return the current set of environment variables extended with the
        CLOUDSMITH_API_KEY environment variable. This environment variable
        is required to cloudsmith_cli command.
        """
        env_vars = os.environ.copy()
        env_vars["CLOUDSMITH_API_KEY"] = self.cloudsmith_api_key
        return env_vars

    def do_get_versions_for_package(self, package_name: str) -> Set[Version]:
        """
        Return all the versions of the given package that are available in the
        Python package repository.
        """
        result = self.list_packages(package_name)
        return set(Version(pkg.version) for pkg in result)


class CloudsmithRPMPublisher:
    """
    A class that encapsulates the logic to publish RPMs to a cloudsmith repository.
    Packages published to a stable repository will get staged first on a staging repository.
    """

    def __init__(
        self,
        rpm_publish_config: ProjectConfigPublishRPM,
        build_type: BuildType,
        cloudsmith_api_key: str,
    ) -> None:
        self.publish_repo: Cloudsmith = self._create_cloudsmith_instance(
            rpm_publish_config,
            build_type,
            cloudsmith_api_key,
            use_staging_repo=build_type == BuildType.stable,
        )

        self.promotion_repo: Optional[Cloudsmith]
        if build_type == BuildType.stable:
            self.promotion_repo = self._create_cloudsmith_instance(
                rpm_publish_config,
                build_type,
                cloudsmith_api_key,
                use_staging_repo=False,
            )
        else:
            self.promotion_repo = None

    def publish_and_promote_rpms(self, rpm_files: List[str]) -> None:
        self.publish_repo.publish_rpms(rpm_files)
        if self.promotion_repo:
            self._promote_rpms(rpm_files)

    def _promote_rpms(self, rpm_files: List[str]) -> None:
        # List packages and filter out relevant rpm files
        packages: List[CloudsmithPackage] = self.publish_repo.list_packages(
            pkg_format=CloudsmithPackageFormat.RPM
        )
        rpm_files_basenames = [os.path.basename(f) for f in rpm_files]
        packages = [pkg for pkg in packages if pkg.filename in rpm_files_basenames]
        # Get promotion repo
        assert self.promotion_repo is not None  # make mypy happy
        promotion_repo = self.promotion_repo.repository.split("/")[
            1
        ]  # Remove owner part from the path
        for pkg in packages:
            self.promotion_repo.copy_package(pkg.identifier_perm, promotion_repo)

    def _create_cloudsmith_instance(
        self,
        rpm_publish_config: ProjectConfigPublishRPM,
        build_type: BuildType,
        cloudsmith_api_key: str,
        use_staging_repo: bool,
    ) -> Cloudsmith:
        """
        Return the Cloudsmith instance required to publish the package.
        """
        if build_type == BuildType.stable and use_staging_repo:
            repo_path = f"{rpm_publish_config.rpm_repo_name_prefix}-stable-staging"
        else:
            repo_path = f"{rpm_publish_config.rpm_repo_name_prefix}-{build_type.value}"
        return Cloudsmith(repo_path, cloudsmith_api_key)


def create_product_freeze_file(
    product_dir: str,
    build_type: BuildType,
    output_file: str,
    github_token: Optional[str],
) -> None:
    product_config = ProductProject(product_dir).get_project_config()
    # Use the python_version defined in the rpm build config
    # as such that RPMs can be build using this freeze file.
    # The python package build config can contain multiple
    # python versions.
    python_version = product_config.build.rpm.python_version
    if not python_version:
        # Ensure backwards-compatibility. Before the introduction of the
        # `build.rpm.python_version` config option, all RPMs were built
        # using python3.6
        python_version = PythonVersion.PYTHON_36

    with tempfile.TemporaryDirectory() as working_dir:
        # Resolve additional lock files
        additional_lock_files_dir: str = os.path.join(
            working_dir, "additional_lock_files"
        )
        os.mkdir(additional_lock_files_dir)
        paths_additional_lock_files: List[str]
        paths_additional_lock_files = product_config.clone_additional_lock_file_repos(
            clone_dir=additional_lock_files_dir,
            branch=util.get_branch(product_dir),
            git_token=github_token,
        )
        # Resolve the dependencies of the product
        dependencies_dir: str = os.path.join(working_dir, "dependencies")
        os.mkdir(dependencies_dir)
        paths_components: List[str]
        paths_components = product_config.dependencies.clone_all_python_dependencies(
            clone_dir=dependencies_dir,
            branch=util.get_branch(product_dir),
            token=github_token,
        )
        freeze_file_generator = FreezeFileGenerator(
            project_dir=product_dir,
            component_dirs=paths_components,
            build_type=build_type,
            min_c_constraint_files=paths_additional_lock_files,
            pip_index_url=build_type.get_pip_index_url(),
            python_version=python_version,
        )
        freeze_file_generator.write_freeze_file_with_external_dependencies(output_file)


class FreezeFileGenerator:
    def __init__(
        self,
        project_dir: str,
        component_dirs: Optional[List[str]] = None,
        build_type: Optional[BuildType] = None,
        min_c_constraint_files: List[str] = [],
        min_r_constraint_files: List[str] = [],
        pip_index_url: Optional[str] = None,
        python_version: PythonVersion = PythonVersion.PYTHON_3,
    ) -> None:
        """
        :param project_dir: The directory containing the product repository for which the freeze file has to
                            be generated.
        :param component_dirs: A list of directories that contains the checked out code for each component
                               of the product (core + extensions). If provided, the components will be built
                               from source. If omitted, the components will be downloaded via a pypi repository.
        :param build_type: When `component_dirs` is set, this argument indicates the build type with which the
                           components have to be built.
        :param min_c_constraint_files: The generated freeze file should be compliant with the constraints
                                       mentioned in these files.
        :param min_r_constraint_files: The generated freeze file has to contain the packages mentioned
                                       in these constraint files.
        :param pip_index_url: Use this pip_index_url while installing the project into a venv.
                              When not provided, the index URL from the PIP_INDEX_URL environment
                              variable is used. If non of both is set, the default pip index url
                              from pip is used.
        :param python_version: Use this version of Python to generate the freeze file.
        """
        if component_dirs and not build_type:
            raise Exception(
                "The `build_type` arguments has to be provided when `component_dirs` is set."
            )
        self._project_dir = os.path.abspath(project_dir)
        self._component_dirs = (
            [os.path.abspath(component_dir) for component_dir in component_dirs]
            if component_dirs is not None
            else None
        )
        self._build_type = build_type
        self._min_c_constraint_files = [
            os.path.abspath(file) for file in min_c_constraint_files
        ]
        self._min_r_constraint_files = [
            os.path.abspath(file) for file in min_r_constraint_files
        ]
        self._pip_index_url = pip_index_url
        self._python_version = python_version

    @classmethod
    def _remove_dependencies_containing(
        cls, contains: str, freeze_file_content: str
    ) -> str:
        """
        Remove all constraints from `freeze_file_content` that contain `contains`.
        """
        lines = [
            line.strip()
            for line in freeze_file_content.strip().splitlines()
            if line.strip() and contains not in line
        ]
        return "\n".join(lines)

    def _remove_this_package(self, freeze_file_content: str) -> str:
        """
        Remove the product Python package from the freeze file, because
        pip includes it in the freeze file in the following way:
        `<pkg-name> @ file://<path-to-package-dir>`.
        Pip download cannot handle this kind of constraints.
        """
        package_name = util.get_name_python_project(self._project_dir)
        return FreezeFileGenerator._remove_dependencies_containing(
            contains=f"{package_name} @ ", freeze_file_content=freeze_file_content
        )

    def write_freeze_file_with_external_dependencies(self, output_file: str) -> str:
        """
        Generate a freeze file that only contains the external dependencies.
        """
        freeze_file_content = self._get_freeze_file_content(allow_pre_releases=False)
        freeze_file_content = self._remove_this_package(freeze_file_content)
        freeze_file_content = FreezeFileGenerator._remove_dependencies_containing(
            contains="inmanta", freeze_file_content=freeze_file_content
        )
        with open(output_file, "w") as f:
            f.write(freeze_file_content)

    def write_freeze_file_with_all_dependencies(
        self,
        output_file: str,
        allow_pre_releases_inmanta_pkgs: bool = False,
    ) -> None:
        """
        Generate a freeze file that contains all dependencies (internal + external dependencies).

        :param allow_pre_releases_inmanta_pkgs: Whether the internal dependencies can be pinned using pre-release versions.
        """
        freeze_file_content = self._get_freeze_file_content(allow_pre_releases=False)
        freeze_file_content = self._remove_this_package(freeze_file_content)
        if allow_pre_releases_inmanta_pkgs:
            # Replace inmanta dependencies with pre-releases
            freeze_file_content = FreezeFileGenerator._remove_dependencies_containing(
                contains="inmanta", freeze_file_content=freeze_file_content
            )
            with open(output_file, "w+") as f:
                f.write(freeze_file_content)
            freeze_file_content = self._get_freeze_file_content(
                min_c_constraint_files=[output_file],
                min_r_constraint_files=[output_file],
                allow_pre_releases=True,
            )
            # Only keep dependencies not the package itself
            freeze_file_content = self._remove_this_package(freeze_file_content)

        with open(output_file, "w") as f:
            f.write(freeze_file_content)

    def _get_freeze_file_content(
        self,
        min_c_constraint_files: Optional[List[str]] = None,
        min_r_constraint_files: Optional[List[str]] = None,
        allow_pre_releases: bool = False,
    ) -> str:
        env_vars = os.environ.copy()
        if self._pip_index_url is not None:
            env_vars["PIP_INDEX_URL"] = self._pip_index_url
        with tempfile.TemporaryDirectory() as tmp_dir:
            dist_dir = None
            if self._component_dirs:
                dist_dir = os.path.join(tmp_dir, PYTHON_DISTS_DIR)
                self._build_components(dist_dir)
            return util.subprocess_log(
                subprocess.check_output,
                self._get_freeze_command(
                    dist_dir,
                    min_c_constraint_files,
                    min_r_constraint_files,
                    allow_pre_releases,
                ),
                logger=LOGGER,
                shell=True,
                cwd=tmp_dir,
                env=env_vars,
                encoding="utf-8",
            )

    def _build_components(self, destination_dir: str) -> None:
        for component_dir in self._component_dirs:
            build_python(
                project_dir=component_dir,
                build_type=self._build_type,
                output_dir=destination_dir,
            )

    def _get_freeze_command(
        self,
        dist_dir: Optional[str] = None,
        min_c_constraint_files: Optional[List[str]] = None,
        min_r_constraint_files: Optional[List[str]] = None,
        allow_pre_releases: bool = False,
    ):
        if min_c_constraint_files is None:
            min_c_constraint_files = list(self._min_c_constraint_files)
        if min_r_constraint_files is None:
            min_r_constraint_files = list(self._min_r_constraint_files)
        min_c_constraints = " ".join([f"-c {f}" for f in min_c_constraint_files])
        min_r_constraints = " ".join([f"-r {f}" for f in min_r_constraint_files])
        if min_r_constraints:
            install_dependencies_in_min_r_files = (
                f"env/bin/pip install -qqq  {min_r_constraints} &&"
            )
        else:
            install_dependencies_in_min_r_files = ""
        find_links_argument = f"--find-links {dist_dir}" if dist_dir else ""
        pre_argument = "--pre" if allow_pre_releases else ""
        return f"""
            {self._python_version.get_name_python_binary()} -m venv env && \
            env/bin/pip install -qqq -U {min_c_constraints} wheel setuptools pip setuptools_scm && \
            {install_dependencies_in_min_r_files} \
            env/bin/pip install -qqq {pre_argument} {find_links_argument} {min_c_constraints} {self._project_dir} && \
            env/bin/pip freeze --all
        """
