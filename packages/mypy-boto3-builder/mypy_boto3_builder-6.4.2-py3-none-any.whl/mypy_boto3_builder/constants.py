"""
Constants and paths.
"""
from pathlib import Path

# Master module name
MODULE_NAME = "mypy_boto3"

# PyPI module name
PYPI_NAME = "mypy-boto3"

# Random region to initialize services
DUMMY_REGION = "us-west-2"

# Jinja2 templates for boto3-stubs
TEMPLATES_PATH = Path(__file__).parent / "templates"

# Static *.pyi files for boto3-stubs
BOTO3_STUBS_STATIC_PATH = Path(__file__).parent / "boto3_stubs_static"

# Static *.pyi files for botocore-stubs
BOTOCORE_STUBS_STATIC_PATH = Path(__file__).parent / "botocore_stubs_static"

# Boto3 stubs module name
BOTO3_STUBS_NAME = "boto3-stubs"

# Botocore stubs module name
BOTOCORE_STUBS_NAME = "botocore-stubs"

# Max line length for boto3 docs
LINE_LENGTH = 100

# type defs module name
TYPE_DEFS_NAME = "type_defs"

# Main logger name
LOGGER_NAME = "mypy_boto3_builder"

# builder CLI entrypoint name
PROG_NAME = "mypy_boto3_builder"

# builder package name
PACKAGE_NAME = "mypy-boto3-builder"
