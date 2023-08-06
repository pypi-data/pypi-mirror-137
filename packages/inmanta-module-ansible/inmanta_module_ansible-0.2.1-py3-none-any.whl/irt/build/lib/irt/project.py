"""
    :copyright 2021 Inmanta
    :contact: code@inmanta.com
"""
import enum
import logging
import os
import tempfile
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Tuple

import toml
from pydantic import BaseModel, Field, root_validator, validator
from toml.encoder import TomlEncoder

from irt import release, util, version

LOGGER = logging.getLogger(__name__)


class ProjectConfigHooks(BaseModel):
    pre: Optional[str] = None


class DistType(Enum):
    sdist: str = "sdist"
    bdist_wheel: str = "bdist_wheel"


class ProjectConfigBuildPythonSubprojects(BaseModel):
    """
    Allows specifying subprojects in this project's repo that should be built and published as well.
    Sub projects have no separate config file and thus follow their parent's build config.
    """

    directory: str


class PythonVersion(Enum):
    PYTHON_3 = "python3"
    PYTHON_36 = "python3.6"
    PYTHON_37 = "python3.7"
    PYTHON_38 = "python3.8"
    PYTHON_39 = "python3.9"
    PYTHON_310 = "python3.10"
    PYTHON_311 = "python3.11"

    def get_name_python_binary(self) -> str:
        return self.value

    def get_version_number(self) -> str:
        # Remove 'python' from value
        return self.value[6:]


class ProjectConfigBuildPython(BaseModel):
    """
    :param python_versions: Build python packages for these versions of Python.
    """

    env: Dict[str, str] = {}
    hooks: ProjectConfigHooks = ProjectConfigHooks()
    dists: List[DistType] = list(iter(DistType))
    subprojects: Dict[str, ProjectConfigBuildPythonSubprojects] = {}
    python_versions: List[PythonVersion] = [PythonVersion.PYTHON_3]


class ProjectConfigBuildRPM(BaseModel):
    """
    :param python_version: The venv included in the RPM should use this version of Python.
    """

    centos_versions: List[int] = []
    # Set the default value to None, because this config is shared between product repos and non-product repos.
    # Non-product repos don't require this option to be set.
    python_version: Optional[PythonVersion] = None
    enable_repo: Dict[str, List[str]] = {}

    @validator("python_version")
    @classmethod
    def validate_python_version(cls, value: PythonVersion) -> PythonVersion:
        if value and value is PythonVersion.PYTHON_3:
            raise ValueError(
                "`build.rpm.python_version` should contain a specific python version. "
                "For example: `python3.9`. `python3` is not allowed."
            )
        return value


class ProjectConfigBuild(BaseModel):
    python: ProjectConfigBuildPython = ProjectConfigBuildPython()
    rpm: ProjectConfigBuildRPM = ProjectConfigBuildRPM()


class ProjectConfigPublishRPM(BaseModel):
    rpm_repo_name_prefix: Optional[str] = None


class ProjectConfigPublishPython(BaseModel):
    public: bool = False


class ProjectConfigPublish(BaseModel):
    python: ProjectConfigPublishPython = ProjectConfigPublishPython()
    rpm: ProjectConfigPublishRPM = ProjectConfigPublishRPM()


@enum.unique
class VersionBumpTool(Enum):
    BUMPVERSION: str = "bumpversion"
    YARN: str = "yarn"

    def get_tool(self, project_path: str) -> version.VersionBumpTool:
        if self == VersionBumpTool.BUMPVERSION:
            return version.Bumpversion(project_path)
        elif self == VersionBumpTool.YARN:
            return version.Yarn(project_path)
        raise Exception("Got unknown version bump tool %s" % self)


class ProjectConfigVersionBump(BaseModel):
    tool: VersionBumpTool = VersionBumpTool.BUMPVERSION


class ProjectConfig(BaseModel):
    """
    Structured representation of the config in the tool.irt section of the pyproject.toml file for an inmanta project.
    Supports the following config:

    The field `tool.irt.publish.rpm.enable-repo` indicates which additional RPM repositories have to be enabled
    to build RPMs for a specific centos version.

    The field `tool.irt.publish.rpm.rpm_repo_name_prefix` indicates the name of the RPM repository
    on cloudsmith with the -dev/-next/-stable part omitted. The placeholder `<major-version>`
    can be used when the major version of the product is part of the name of the RPM repository.

    ```
    [tool.irt.build.python]
    # declare environment variable values for the build stage
    env = { "MY_CUSTOM_ENV_VAR" = "some_value", "ANOTHER_ONE" = "42" }
    # prebuild script is executed before building the Python package
    hooks = { "pre" = "prebuild.sh" }
    # if dists is specified, only build the specified dist artifacts
    dists = ["bdist_wheel"]

    [tool.irt.publish.python]
    # if public, stable artifacts will be published to public repositories
    public = True

    [tool.irt.publish.rpm]
    rpm_repo_name_prefix = "inmanta/inmanta-service-orchestrator-<major-version>"

    [tool.irt.build.rpm]
    enable_repo = {"el7" = ["epel"], "el8" = []}`
    ```
    """

    build: ProjectConfigBuild = ProjectConfigBuild()
    publish: ProjectConfigPublish = ProjectConfigPublish()
    version_bump: ProjectConfigVersionBump = Field(
        default=ProjectConfigVersionBump(), alias="version-bump"
    )


class ProductDependenciesNpm(BaseModel):
    repo: str
    version: str


class ProductDependencies(BaseModel):
    """
    :param additional_python_dependencies: Contains the python dependencies which are not extensions. The total set
                                           of python dependencies is the union of the `extensions` and the
                                           `additional_python_dependencies`. This field is deprecated.
    :param core_component: Contains URL to the core-component of this product.
    """

    core_component: Optional[str] = Field(default=None, alias="core-component")
    additional_python_dependencies: Dict[str, str] = Field(
        default={}, alias="additional-python-dependencies"
    )
    npm: Dict[str, ProductDependenciesNpm] = {}
    extensions: Dict[str, str] = {}

    # deprecated: used by iso3
    core_component_name: Optional[str] = Field(
        default=None, alias="core-component-name"
    )

    @root_validator(skip_on_failure=True)
    @classmethod
    def check_cross_field_constraints(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensure that either the core_component field or the additional_python_dependencies
        field is set, but never both at the same time.
        """
        core_component = values.get("core_component", None)
        additional_python_dependencies = values.get("additional_python_dependencies")
        if core_component is not None and additional_python_dependencies:
            raise ValueError(
                "The tool.irt.dependencies.additional-python-dependencies field and "
                "the tool.irt.dependencies.core_component field cannot be set at the same time."
            )
        if core_component is None and not additional_python_dependencies:
            raise ValueError(
                "Either the tool.irt.dependencies.additional-python-dependencies field or "
                "the tool.irt.dependencies.core_component field should be set."
            )
        return values

    def get_core_component(self) -> Tuple[str, str]:
        """
        This methods makes abstraction of the core_component and the additional_python_dependencies field,
        since the latter is deprecated in favor of the former.
        :returns:  repo_name, repo_url
        """
        if self.core_component is not None:
            return (
                self.core_component_name
                if self.core_component_name is not None
                else util.get_git_repo_name_for_url(self.core_component),
                self.core_component,
            )
        else:
            LOGGER.warning(
                "The field tool.irt.dependencies.additional-python-dependencies is deprecated "
                "use tool.irt.dependencies.core_component field instead."
            )
            assert len(self.additional_python_dependencies) == 1
            return dict(self.additional_python_dependencies).popitem()

    def get_all_python_component_repos(self) -> Dict[str, str]:
        return {**self.extensions, **dict([self.get_core_component()])}

    def get_all_npm_component_repos(self) -> Dict[str, str]:
        return {name: npm.repo for name, npm in self.npm.items()}

    def get_all_component_repos(self) -> Dict[str, str]:
        return {
            **self.get_all_python_component_repos(),
            **self.get_all_npm_component_repos(),
        }

    def clone_all_python_dependencies(
        self,
        clone_dir: str,
        branch: str = "master",
        token: Optional[str] = None,
    ) -> List[str]:
        result = []
        for name, url in self.get_all_python_component_repos().items():
            clone_dir_dep = os.path.join(clone_dir, name)
            util.clone_repo(
                url=url, directory=clone_dir_dep, branch=branch, token=token
            )
            result.append(clone_dir_dep)
        return result


class ProductDocumentationPublishConfig(BaseModel):
    """
    :param username: Username to use to SSH into the machine where to documentation has to be published.
    :param hostname: Hostname/IP address of the machine on which the documentation has to be published.
    :param dev_release_path: The path on `hostname` where the dev releases should be published.
    :param next_release_path: The path on `hostname` where the next releases should be published.
    :param stable_release_path: The path on `hostname` where the stable releases should be published.
    :param post_publish_hook_remote: Script present on `hostname` that should be executed after the documentation
                                     has been published. Two parameters will be passed to this script. The first
                                     parameters indicates the publish_path and the second parameter the build type.
    """

    username: str = "docs"
    hostname: str = "devil.inmanta.com"
    dev_release_path: str
    next_release_path: Optional[str] = None
    stable_release_path: str
    post_publish_hook_remote: Optional[str] = None

    def get_release_path(self, build_type: release.BuildType) -> str:
        if build_type == release.BuildType.dev:
            return self.dev_release_path
        elif build_type == release.BuildType.next:
            if self.next_release_path is None:
                raise Exception(
                    "tool.irt.documentation.publish-config.next_release_path not defined on pyproject.toml"
                )
            return self.next_release_path
        elif build_type == release.BuildType.stable:
            return self.stable_release_path
        else:
            raise Exception(f"Unknown build_type provided: {build_type}")


class ProductDocumentation(BaseModel):
    """
    :param documentation_base_repo: When `documentation_repo` contains the changes with respect to the documentation on
                                    another Git repository, this parameter point to the latter Git repository.
    :param documentation_repo: Git repository containing the documentation for this product or the diff
                               with respect to `documentation_base_repo` when `documentation_base_repo` is set.
    """

    documentation_base_repo: Optional[str] = None
    documentation_repo: str
    publish: ProductDocumentationPublishConfig


class ProductModuleSet(BaseModel):
    """
    :param repository: Repository containing the module set definition file.
    :param path: The path to the module set definition file on `repository`.
    :param publish_repo: The Git repository on which the module set has to be published.
                         This is a Git URL without the last part containing the module name.
                         For example: modules@modules.inmanta.com:inmanta-service-orchestrator/3
    """

    repository: str = "https://github.com/inmanta/irt.git"
    path: str
    publish_repo: Optional[str]

    def clone_module_set_repo(
        self,
        clone_dir: str,
        branch: str = "master",
        token: Optional[str] = None,
        module_set_def_file_path: Optional[str] = None,
    ) -> str:
        """
        Clone of Git repository containing the module set definition file and return the path to the module
        definition file on disk.

        :param module_set_def_file_path: If set, use this module set definition path instead of self.path
        """
        util.clone_repo(self.repository, clone_dir, branch, token)
        if module_set_def_file_path:
            module_set_file = os.path.join(clone_dir, module_set_def_file_path)
        else:
            module_set_file = os.path.join(clone_dir, self.path)
        if not os.path.isfile(module_set_file):
            raise Exception(
                f"Module set file {module_set_def_file_path if module_set_def_file_path else self.path } not found in"
                f" {self.repository} (branch={branch})"
            )
        return module_set_file


class RequirementsLockFile(BaseModel):
    repo: str
    files: List[str] = []


class ProductConfig(ProjectConfig):
    """
    Structured representation of the config in the tool.irt section of the pyproject.toml file for an inmanta product.
    Extends the configuration for an inmanta project with:

    The requirements.txt file, present in the root of the product repository, is always taken into account when
    building RPMs. The section `[tool.irt.additional-lock-files]` in the pyproject.toml file can be used to
    add additional lock files. By default no additional lock files are used.

    ```
    [tool.irt.dependencies.additional-python-dependencies]
    dummy-inmanta-extension-a = "https://github.com/inmanta/dummy-inmanta-extension-a

    [tool.irt.dependencies.npm]
    dashboard = { "repo" = "https://github.com/inmanta/inmanta-dashboard", "version" = "master" }

    [tool.irt.additional-lock-files]
    inmanta-core = {"repo" = "https://github.com/inmanta/inmanta-core", "files" = ["requirements.txt"]}
    ```
    """

    dependencies: ProductDependencies
    documentation: ProductDocumentation
    module_set: ProductModuleSet
    additional_lock_files: Dict[str, RequirementsLockFile] = Field(
        default={}, alias="additional-lock-files"
    )

    def clone_additional_lock_file_repos(
        self, clone_dir: str, branch: str, git_token: Optional[str]
    ) -> List[str]:
        """
        :param clone_dir: Directory in which the lock file repos will be cloned.
        :param branch: Clone this branch on each lock file repo.
        :param git_token: Token used to clone the repositories.
        :result: A list of paths to the additional lock files.
        """
        os.makedirs(clone_dir, exist_ok=True)
        all_lock_files = []
        for name, additional_lock_file in self.additional_lock_files.items():
            lock_file_repo_clone_dir = os.path.join(clone_dir, name)
            util.clone_repo(
                additional_lock_file.repo, lock_file_repo_clone_dir, branch, git_token
            )
            for current_file in additional_lock_file.files:
                lock_file_path = os.path.join(lock_file_repo_clone_dir, current_file)
                all_lock_files.append(lock_file_path)
        for current_lock_file in all_lock_files:
            if not os.path.isfile(current_lock_file):
                raise Exception(f"No lock file file found at {current_lock_file}")
        return all_lock_files


class Project:
    """
    An Inmanta project.
    """

    def __init__(self, directory: str) -> None:
        """
        :param directory: The directory the project resides in.
        """
        if not os.path.isdir(directory):
            raise Exception(f"project root {directory} is not a directory")
        self.root: str = directory
        self.config_file: str = os.path.join(self.root, "pyproject.toml")

    def _load_toml_irt(self) -> Optional[Mapping[str, object]]:
        toml_content: Mapping[str, object]
        try:
            toml_content = toml.load(self.config_file)
        except FileNotFoundError:
            return None
        try:
            return toml_content["tool"]["irt"]  # type: ignore
        except KeyError:
            return None

    def get_project_config(self) -> ProjectConfig:
        """
        Returns the project config as specified in the [tool.irt] section of the project's pyproject.toml.
        """
        toml_content: Optional[Mapping[str, object]] = self._load_toml_irt()
        return (
            ProjectConfig() if toml_content is None else ProjectConfig(**toml_content)
        )

    def write_project_config(self, config: ProjectConfig) -> None:
        """
        Write the given project config to this project's config file. Any placeholders present when the config was parsed will
        have been filled with their appropriate values. Do not use this method if you want to preserve placeholders.
        """
        plain_config: Dict[str, object] = config.dict(
            by_alias=True, exclude_defaults=True
        )
        toml_content: Mapping[str, object] = toml.load(self.config_file)
        toml_content["tool"]["irt"] = plain_config  # type: ignore

        class CustomTomlEncoder(TomlEncoder):
            """
            This encoder ensures that the enum values are correctly serialized
            into their value.
            """

            def dump_value(self, v):
                if isinstance(v, Enum):
                    return f'"{v.value}"'
                return super(CustomTomlEncoder, self).dump_value(v)

        text: str = toml.dumps(toml_content, encoder=CustomTomlEncoder())
        with open(self.config_file, "w") as f:
            f.write(text)


class ProductProject(Project):
    """
    An Inmanta product project, like inmanta-oss or inmanta-service-orchestrator.
    """

    def get_project_config(self, fill_placeholders: bool = True) -> ProductConfig:
        toml_content: Optional[Mapping[str, object]] = self._load_toml_irt()
        if toml_content is None:
            raise Exception(
                "Product root should contain pyproject.toml with [tool.irt] section"
            )
        product_config = ProductConfig(**toml_content)
        if fill_placeholders:
            self._fill_in_placeholders(product_config)
        return product_config

    def _fill_in_placeholders(self, product_config: ProductConfig) -> None:
        version = util.get_version_python_project(self.root)
        major_version = version.split(".", maxsplit=1)[0]
        kwargs = {"version": version, "major_version": major_version}
        # Fill in placeholder in `publish.rpm.rpm_repo_name_prefix`
        rpm_build_config = product_config.publish.rpm
        if rpm_build_config.rpm_repo_name_prefix is not None:
            rpm_build_config.rpm_repo_name_prefix = (
                rpm_build_config.rpm_repo_name_prefix.format(**kwargs)
            )
        # Fill in placeholder in `documentation.publish.*_release_path`
        publish_config = product_config.documentation.publish
        publish_config.dev_release_path = publish_config.dev_release_path.format(
            **kwargs
        )
        if publish_config.next_release_path is not None:
            publish_config.next_release_path = publish_config.next_release_path.format(
                **kwargs
            )
        publish_config.stable_release_path = publish_config.stable_release_path.format(
            **kwargs
        )
        # Fill in placeholder in `module_set.path`
        module_set_config = product_config.module_set
        module_set_config.path = module_set_config.path.format(**kwargs)
        # Fill in placeholder in `module_set.publish_repo`
        if product_config.module_set.publish_repo is not None:
            module_set_config.publish_repo = module_set_config.publish_repo.format(
                **kwargs
            )

    def install(
        self,
        python_path: str,
        working_dir: str,
        branch: str,
        build_type: release.BuildType,
        token: Optional[str] = None,
    ) -> None:
        """
        Install this product in a Python environment.

        :param python_path: The path to the Python executable for the environment to install the product in.
        :param working_dir: The working directory. Additional files might be stored here.
        """
        product_lock_file = os.path.join(self.root, "requirements.txt")
        product_dev_requires = os.path.join(self.root, "requirements.dev.txt")
        lock_file_repo_clone_dir = os.path.join(working_dir, "lock_file_repos")
        additional_lock_files = (
            self.get_project_config().clone_additional_lock_file_repos(
                lock_file_repo_clone_dir, branch, token
            )
        )
        all_product_lock_files = [product_lock_file] + additional_lock_files

        # Create venv + Install product
        pip = build_type.get_pip(python_path)
        pip.set_env_vars()
        pip.install(
            pkg=self.root,
            requires_files=(
                [product_dev_requires] if os.path.isfile(product_dev_requires) else []
            ),
            constraint_files=all_product_lock_files,
        )

    @classmethod
    def get_project_config_from_git_repo(
        cls, product_repo: str, branch: str, token: Optional[str]
    ) -> ProductConfig:
        with tempfile.TemporaryDirectory() as tmp_dir:
            clone_dir = os.path.join(tmp_dir, "clone_dir")
            util.clone_repo(product_repo, clone_dir, branch, token)
            return ProductProject(clone_dir).get_project_config()

    def get_major_version_number(self) -> int:
        version = util.get_version_python_project(self.root)
        splitted_version = version.split(".")
        return int(splitted_version[0])
