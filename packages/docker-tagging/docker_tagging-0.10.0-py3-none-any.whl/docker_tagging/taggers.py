# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from datetime import datetime
import logging
from .git_helper import GitHelper
from .docker_runner import DockerRunner


logger = logging.getLogger(__name__)


def get_program_version(container, program: str) -> str:
    return DockerRunner.run_simple_command(container, cmd=f"{program} --version")


def get_env_variable(container, variable: str) -> str:
    env = DockerRunner.run_simple_command(
        container,
        cmd="env",
        print_result=False,
    ).split()
    for env_entry in env:
        if env_entry.startswith(variable):
            return env_entry[len(variable) + 1:]
    raise KeyError(variable)


def get_pip_package_version(container, package: str) -> str:
    version_prefix = "Version: "
    package_info = DockerRunner.run_simple_command(
        container,
        cmd=f"pip show {package}",
        print_result=False,
    )
    version_lines = package_info.split("\n")
    for version_line in version_lines:
        if version_line.startswith(version_prefix):
            break
    else:
        raise ValueError(f"prefix {version_prefix} does not exist")
    return version_line[len(version_prefix):]


class TaggerInterface:
    """Common interface for all taggers"""

    @staticmethod
    def tag_value(container) -> str:
        raise NotImplementedError


class SHATagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return GitHelper.commit_hash_tag()


class DateTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        return datetime.utcnow().strftime("%Y-%m-%d")


class UbuntuVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        os_release = DockerRunner.run_simple_command(
            container,
            "cat /etc/os-release",
        ).split("\n")
        for line in os_release:
            if line.startswith("VERSION_ID"):
                return "ubuntu-" + line.split("=")[1].strip('"')


class PythonVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        error = None
        for py in ['python', 'python3', 'python2']:
            try:
                return "python-" + get_program_version(container, py).split()[1]
            except AssertionError as e:
                error = e
        else:
            raise error


class PythonProjectVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        pyproject = DockerRunner.run_simple_command(
            container,
            "cat pyproject.toml",
        ).split("\n")
        for line in pyproject:
            if line.startswith("version"):
                return line.split("=")[1].strip(' "')


class PythonProjectMinorMajorVersionTagger(TaggerInterface):
    @staticmethod
    def tag_value(container) -> str:
        pyproject = DockerRunner.run_simple_command(
            container,
            "cat pyproject.toml",
        ).split("\n")
        for line in pyproject:
            if line.startswith("version"):
                v = line.split("=")[1].strip(' "')
                return v[:v.rfind(".")]
