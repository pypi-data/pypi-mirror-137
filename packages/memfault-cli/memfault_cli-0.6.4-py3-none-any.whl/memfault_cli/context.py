import json
import logging
from typing import Any, Dict, List, Optional, Set, Union

import click

from .authenticator import Authenticator
from .functools_ext import cached_property

LOG = logging.getLogger(__name__)


class PackageInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, name: str, version_name: str, version_code: str):
        self.name = name
        self.version_name = version_name
        self.version_code = version_code


class FullReleaseVersion:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, software_version: str):
        self.software_version = software_version

    def to_json_representable(self):
        return self.software_version


class DeltaReleaseVersion:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, delta_from: str, delta_to: str):
        self.delta_from = delta_from
        self.delta_to = delta_to

    def to_json_representable(self):
        return [self.delta_from, self.delta_to]


class SoftwareInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(
        self,
        software_type: str,
        version: Union[FullReleaseVersion, DeltaReleaseVersion],
        revision: Optional[str] = None,
    ):
        self.software_type = software_type
        self.version = version
        self.revision = revision


CustomMetricReadingValueType = Union[int, float, str, bool, None]


class Attribute:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, string_key: str, value: CustomMetricReadingValueType) -> None:
        self.string_key = string_key
        self.value = value

    @staticmethod
    def from_cli_args(key: str, cli_value: str):
        return Attribute(string_key=key, value=Attribute._convert_value(cli_value))

    @staticmethod
    def _convert_value(cli_value: str) -> CustomMetricReadingValueType:
        if cli_value == "":
            return None
        try:
            value = json.loads(cli_value)
        except json.decoder.JSONDecodeError:
            value = cli_value
        if value is not None and not isinstance(value, (int, float, str, bool)):
            LOG.warning(
                "Only boolean, number, string or null types are allowed! Treating passed value as a string."
            )
            return cli_value
        return value


class XedInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(self, device_serial: str, hardware_version: str):
        self.device_serial = device_serial
        self.hardware_version = hardware_version


class MarInfo:  # noqa: B903 - no data classes in Python 3.6
    def __init__(
        self, device_serial: str, hardware_version: str, software_type: str, software_version: str
    ):
        self.device_serial = device_serial
        self.hardware_version = hardware_version
        self.software_type = software_type
        self.software_version = software_version


class MemfaultCliClickContext(object):
    """
    A context passed around between the memfault cli sub-commands.


    If the top level CLI has any "required" it's not possible to display
    any help info about the subcommands using "--help" without providing them.
    By passing around this context, subcommand help messages can be displayed
    and errors can be raised in a uniform way
    """

    def __init__(self) -> None:
        self.obj: Dict[str, Any] = {}

    def _format_as_option(self, property_name: str) -> str:
        return f"--{property_name.replace('_', '-')}"

    def _find_obj_or_raise(self, name):
        value = self.obj.get(name)
        if value is None:
            raise click.exceptions.UsageError(f"Missing option {self._format_as_option(name)!r}.")
        return value

    def check_required_cli_args(self, *, authenticator: Authenticator):
        required_args = authenticator.required_args()

        for arg in required_args:
            self._find_obj_or_raise(arg)

    def _format_arg_set(self, arg_set: Set[str]) -> str:
        return ", ".join([f"{self._format_as_option(arg)!r}" for arg in sorted(arg_set)])

    def check_required_either(self, *args: Set[str], mutually_exclusive=False):
        """Check that any full set of args is present"""
        valid_arg_sets = []
        passed_arg_sets = []

        for arg_set in args:
            args_present = [self.obj.get(arg, None) is not None for arg in arg_set]
            if any(args_present):
                passed_arg_sets.append(arg_set)
            if all(args_present):
                valid_arg_sets.append(arg_set)

        if mutually_exclusive and len(passed_arg_sets) > 1:
            formatted_passed_args = [self._format_arg_set(arg_set) for arg_set in passed_arg_sets]
            raise click.exceptions.UsageError(
                f"Parameters {' and '.join(sorted(formatted_passed_args))} may not be used together."
            )

        if len(valid_arg_sets) == 0:
            formatted_required_args = [self._format_arg_set(arg_set) for arg_set in args]
            raise click.exceptions.UsageError(
                f"Please pass either {' or '.join(sorted(formatted_required_args))}."
            )

    @cached_property
    def authenticator(self) -> Authenticator:
        return Authenticator.create_authenticator_given_context_or_raise(self)

    @property
    def org(self):
        return self._find_obj_or_raise("org")

    @property
    def org_token(self) -> str:
        return self._find_obj_or_raise("org_token")

    @property
    def project(self):
        return self._find_obj_or_raise("project")

    @property
    def email(self):
        return self._find_obj_or_raise("email")

    @property
    def password(self):
        return self._find_obj_or_raise("password")

    @property
    def project_key(self):
        return self._find_obj_or_raise("project_key")

    @property
    def concurrency(self):
        return self._find_obj_or_raise("concurrency")

    @property
    def software_info(self) -> Optional[SoftwareInfo]:
        sw_type = self.obj.get("software_type")
        sw_ver = self.obj.get("software_version")
        revision = self.obj.get("revision")
        delta_from = self.obj.get("delta_from")
        delta_to = self.obj.get("delta_to")

        version: Union[DeltaReleaseVersion, FullReleaseVersion, None]
        if delta_from and delta_to:
            version = DeltaReleaseVersion(delta_from, delta_to)
        elif sw_ver:
            version = FullReleaseVersion(sw_ver)
        else:
            version = None

        if revision and (version is None or sw_type is None):
            raise click.exceptions.UsageError(
                "A version ('--software-version' or '--delta-{{from,to}}') and '--software-type' must be specified when using '--revision'"
            )

        if sw_type is None and version is None:
            return None

        if sw_type is None or version is None:
            raise click.exceptions.UsageError(
                "Version ('--software-version' or '--delta-{{from,to}}') and '--software-type' must be specified together"
            )

        return SoftwareInfo(
            software_type=sw_type,
            version=version,
            revision=revision,
        )

    @property
    def attributes(self) -> List[Attribute]:
        return [Attribute.from_cli_args(*cli_args) for cli_args in self.obj.get("attribute", [])]

    @property
    def xed_info(self) -> XedInfo:
        device_serial = self._find_obj_or_raise("device_serial")
        hardware_version = self._find_obj_or_raise("hardware_version")
        return XedInfo(
            device_serial=device_serial,
            hardware_version=hardware_version,
        )

    @property
    def mar_info(self) -> MarInfo:
        device_serial = self._find_obj_or_raise("device_serial")
        hardware_version = self._find_obj_or_raise("hardware_version")
        software_type = self._find_obj_or_raise("software_type")
        software_version = self._find_obj_or_raise("software_version")
        return MarInfo(
            device_serial=device_serial,
            hardware_version=hardware_version,
            software_type=software_type,
            software_version=software_version,
        )

    @property
    def file_url(self) -> str:
        url = self.obj.get("url")
        if url is None:
            return "https://files.memfault.com"
        return url

    @property
    def app_url(self) -> str:
        url = self.obj.get("url")
        if url is None:
            return "https://app.memfault.com"
        return url

    @property
    def chunks_url(self) -> str:
        url = self.obj.get("url")
        if url is None:
            return "https://chunks.memfault.com"
        return url

    @property
    def api_url(self) -> str:
        url = self.obj.get("url")
        if url is None:
            return "https://api.memfault.com"
        return url

    @property
    def hardware_version(self):
        return self.obj.get("hardware_version", None)

    @property
    def device_serial(self):
        return self._find_obj_or_raise("device_serial")

    @property
    def build_variant(self):
        return self._find_obj_or_raise("build_variant")

    @property
    def must_pass_through(self):
        return self._find_obj_or_raise("must_pass_through")

    @property
    def notes(self):
        # release notes for an OTA package
        return self._find_obj_or_raise("notes")

    @property
    def android_package_info(self) -> Optional[PackageInfo]:
        package = self.obj.get("package")
        version_name = self.obj.get("version_name")
        version_code = self.obj.get("version_code")
        if package is None and version_name is None and version_code is None:
            return None
        if package is None or version_name is None or version_code is None:
            raise click.exceptions.UsageError(
                '"--package, --version-name" and "--version-code" must be specified together'
            )

        return PackageInfo(package, version_name, version_code)

    @property
    def android_mapping_txt(self) -> Optional[str]:
        return self.obj.get("mapping_txt")

    @property
    def verbose(self) -> bool:
        return self.obj.get("verbose", False)
