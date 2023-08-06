from typing import Dict, List, Optional, TypedDict

from tomlkit import comment, loads, table
from tomlkit.items import Table
from tomlkit.toml_document import TOMLDocument

from andoya.core.toml import TOMLFile

DEFAULT_RUNTIME = "python3.8"
DEFAULT_REQUIREMENTS = "requirements.txt"
DEFAULT_CLI_TIMEOUT = 60
DEFAULT_HTTP_TIMEOUT = 28
DEFAULT_MEMORY_SIZE = 1024


class ProjectDict(TypedDict):
    id: int
    name: str


class Manifest:
    _file: Optional[TOMLFile]
    _data: TOMLDocument

    @classmethod
    def from_file(cls, file: TOMLFile) -> "Manifest":
        """
        Create a new manifest from a TOML file.

        :param file: The TOML file to read from.
        :return: The manifest.
        """
        config = cls()
        config._file = file
        config._data = file.read() if file.exists() else TOMLDocument()
        return config

    @classmethod
    def from_string(cls, contents: str) -> "Manifest":
        """
        Create a new manifest file from a string.

        :param contents: The contents of the manifest file.
        :return: The manifest file.
        """
        manifest = cls()
        manifest._data = loads(contents)
        return manifest

    @property
    def contents(self) -> str:
        return self._data.as_string()

    @property
    def id(self) -> int:
        return self._data["id"]

    @property
    def name(self) -> str:
        return self._data["name"]

    def exists(self) -> bool:
        """
        Whether the manifest exists.

        :return: Whether the manifest exists.
        """
        return self._file and self._file.exists()

    def requirements(self, environment: str) -> str:
        """
        Get the requirements for an environment.

        :param environment: The environment name.
        :return: The requirements.
        """
        return self._data["environments"][environment]["requirements"]

    def before_install_hook_commands(self, environment: str) -> List[str]:
        """
        Get the before-install hook commands for an environment, if any.

        :param environment: The environment name.
        :return: The before-install hooks.
        """
        return self._data["environments"][environment].get("before_install_hooks", [])

    def after_install_hook_commands(self, environment: str) -> List[str]:
        """
        Get the after-install hook commands for an environment, if any.

        :param environment: The environment name.
        :return: The after-install hooks.
        """
        return self._data["environments"][environment].get("after_install_hooks", [])

    def before_deployment_hook_commands(self, environment: str) -> List[str]:
        """
        Get the before-deployment hook commands for an environment, if any.

        :param environment: The environment name.
        :return: The before-deployment hooks.
        """
        return self._data["environments"][environment].get(
            "before_deployment_hooks", []
        )

    def cli_timeout(self, environment: str) -> int:
        """
        Get the CLI timeout (in seconds) for an environment.

        :param environment: The environment name.
        :return: The timeout in seconds.
        """
        return self._data["environments"][environment].get(
            "cli_timeout", DEFAULT_CLI_TIMEOUT
        )

    def cdn(self, environment: str) -> bool:
        """
        Get whether the environment should have a CDN (CloudFront).

        :param environment: The environment name.
        :return: Whether the environment should have a CDN.
        """
        return self._data["environments"][environment].get("cdn", False)

    def django_settings_module(self, environment: str) -> str:
        """
        Get the Django settings module for an environment.

        :param environment: The environment name.
        :return: The Django settings module.
        """
        return self._data["environments"][environment]["settings_module"]

    def memory_size(self, environment: str) -> int:
        """
        Get the memory size (in MB) for an environment.

        :param environment: The environment name.
        :return: The memory size in MB.
        """
        return self._data["environments"][environment].get(
            "memory_size", DEFAULT_MEMORY_SIZE
        )

    def runtime(self, environment: str) -> str:
        """
        Get the runtime for an environment.

        :param environment: The environment name.
        :return: The runtime.
        """
        return self._data["environments"][environment]["runtime"]

    def timeout(self, environment: str) -> int:
        """
        Get the HTTP timeout (in seconds) for an environment.

        :param environment: The environment name.
        :return: The timeout in seconds.
        """
        return self._data["environments"][environment].get(
            "http_timeout", DEFAULT_HTTP_TIMEOUT
        )

    def add_project(
        self, project: ProjectDict, environments: Dict[str, object]
    ) -> None:
        """
        Create a new manifest file.

        :param project: The project data.
        :param environments: The environments data.
        """
        self._data.clear()

        self._data.add(comment("This is your Andoya manifest file."))
        self._data.add(
            comment(
                "The id and name fields are managed by Andoya, so you should not edit them unless you know what you are doing."
            )
        )
        self._data.add("id", project["id"])
        self._data.add("name", project["name"])

        environments_table = table()
        environments_table.add(
            comment("The section below is where your environments are defined.")
        )
        environments_table.add(comment("You can add as many environments as you like."))
        environments_table.add(comment("See: https://docs.andoya.run/environments"))

        for k, v in environments.items():
            environment_table = self._environment_table(v["settings_module"])
            environments_table.add(k, environment_table)

        self._data.add("environments", environments_table)
        self._file.write(self._data)

    def _environment_table(self, settings_module: str) -> Table:
        """
        Create a TOML table for an environment.

        :param settings_module: The settings module.
        :return: The environment table.
        """
        environment_table = table()
        environment_table.add("requirements", DEFAULT_REQUIREMENTS)
        environment_table.add("runtime", DEFAULT_RUNTIME)
        environment_table.add("settings_module", settings_module)
        return environment_table
