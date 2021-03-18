"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the command line client.
"""

from click.testing import CliRunner
import os
from pathlib import Path
import shlex

from hardening_importer.cli import main as cli
from hardening_importer.util import get_logger
from hardening_importer.models import HardeningManifest

from .conftest import VALID_MANIFESTS


def test_help():
    """Test invocation of hardening help page."""
    runner = CliRunner()
    args = shlex.split('--help')

    result = runner.invoke(cli, args)
    assert result.exit_code == 0


def test_verbosity():
    """Test the hardening command with a verbosity flag."""
    runner = CliRunner()
    args = shlex.split('-vvv import .')
    logger = get_logger()
    logger.handlers.clear()

    result = runner.invoke(cli, args)
    # This won't work because we provided no paths
    assert result.exception
    # But we're really testing the logger
    assert int(logger.handlers[0].level) == 10


def test_version():
    """Test the hardening command version output."""
    runner = CliRunner()
    args = shlex.split('--version')
    result = runner.invoke(cli, args)
    assert result.exit_code == 0


def test_import(new_folder):
    """Test importing a hardening manifest with default options."""
    # Make dummy dockerfile
    Path('Dockerfile').touch()
    for manifest_file in VALID_MANIFESTS:
        manifest = HardeningManifest.from_yaml(manifest_file)
        runner = CliRunner()
        args = shlex.split(f'import --manifest-path="{manifest_file}" .')
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
        for resource in manifest.resources:
            assert os.path.exists(resource.filename)
        assert f'--context {new_folder}' in result.output
        assert manifest.name in result.output


def test_no_dockerfile(new_folder):
    """Test importing a hardening manifest with no Dockerfile present."""
    for manifest_file in VALID_MANIFESTS:
        runner = CliRunner()
        args = shlex.split(f'import --manifest-path="{manifest_file}" .')
        result = runner.invoke(cli, args)
        assert result.exception
        assert 'Could not open' in result.output


def test_bad_executor(new_folder):
    """Test importing a hardening manifest but providing a bad executor."""
    # Make dummy dockerfile
    Path('Dockerfile').touch()
    for manifest_file in VALID_MANIFESTS:
        runner = CliRunner()
        args = shlex.split((f'import --manifest-path="{manifest_file}" '
                            f'--build-executor=docker .'))
        result = runner.invoke(cli, args)
        assert result.exception
        assert "Invalid value for '--build-executor'" in result.output
