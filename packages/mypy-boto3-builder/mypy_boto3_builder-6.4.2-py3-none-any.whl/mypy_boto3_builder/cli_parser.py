"""
CLI parser.
"""
import argparse
import logging
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import pkg_resources

from mypy_boto3_builder.constants import PACKAGE_NAME, PROG_NAME


def get_absolute_path(path: str) -> Path:
    """
    Get absolute path from a string.

    Arguments:
        path -- String containing path.

    Returns:
        Absolute path.
    """
    return Path(path).absolute()


@dataclass
class Namespace:
    """
    CLI arguments namespace.
    """

    log_level: int
    output_path: Path
    service_names: list[str]
    build_version: str
    installed: bool
    skip_master: bool
    skip_services: bool
    builder_version: str
    generate_docs: bool
    list_services: bool
    partial_overload: bool
    skip_published: bool


def parse_args(args: Sequence[str]) -> Namespace:
    """
    Main CLI parser for builder.

    Returns:
        Argument parser.
    """
    try:
        version = pkg_resources.get_distribution(PACKAGE_NAME).version
    except pkg_resources.DistributionNotFound:
        version = "0.0.0"

    parser = argparse.ArgumentParser(PROG_NAME, description="Builder for mypy-boto3.")
    parser.add_argument("-d", "--debug", action="store_true", help="Show debug messages")
    parser.add_argument(
        "-b",
        "--build-version",
        help="Set custom output version, otherwise smart versioning is used.",
    )
    parser.add_argument("-V", "--version", action="version", version=version)
    parser.add_argument(
        "--skip-master",
        action="store_true",
        help="Whether to skip master and stubs modules",
    )
    parser.add_argument(
        "--skip-services", action="store_true", help="Whether to skip service modules"
    )
    parser.add_argument(
        "--skip-published", action="store_true", help="Skip packages that are already on PyPI"
    )
    parser.add_argument("--docs", action="store_true", help="Generate docs for modules")
    parser.add_argument(
        "--panic",
        action="store_true",
        help="Raise exception on logger warning and above",
    )
    parser.add_argument(
        "output_path", metavar="OUTPUT_PATH", help="Output path", type=get_absolute_path
    )
    parser.add_argument(
        "-s",
        "--services",
        dest="service_names",
        nargs="*",
        metavar="SERVICE_NAME",
        help=(
            "List of AWS services, by default all services are used."
            " Use `updated` to build only services updated in the release."
            " Use `all` to build all services."
        ),
        default=["all"],
    )
    parser.add_argument(
        "--partial-overload",
        action="store_true",
        help="Build boto3-stubs client/service overload only for selected services",
    )
    parser.add_argument(
        "--installed",
        action="store_true",
        help="Generate already installed packages for typings folder.",
    )
    parser.add_argument(
        "--list-services",
        action="store_true",
        help="List supported boto3 service names.",
    )
    result = parser.parse_args(args)
    result.builder_version = version
    return Namespace(
        log_level=logging.DEBUG if result.debug else logging.INFO,
        output_path=result.output_path,
        service_names=result.service_names,
        skip_master=result.skip_master,
        skip_services=result.skip_services,
        build_version=result.build_version,
        installed=result.installed,
        builder_version=result.builder_version,
        generate_docs=result.docs,
        list_services=result.list_services,
        partial_overload=result.partial_overload,
        skip_published=result.skip_published,
    )
