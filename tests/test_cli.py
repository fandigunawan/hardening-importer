"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the command line client.
"""

import shlex
from click.testing import CliRunner
from hardening_importer.cli import main as cli
from hardening_importer.util import get_logger


def test_help():
    """Test invocation of hardening help page."""
    runner = CliRunner()
    args = shlex.split('--help')

    result = runner.invoke(cli, args)
    assert result.exit_code == 0


def test_verbosity():
    """Test the hardening command with a verbosity flag."""
    runner = CliRunner()
    args = shlex.split('-vvv import')
    logger = get_logger()
    logger.handlers.clear()

    result = runner.invoke(cli, args)
    # Enable this when implemented
    # assert result.exit_code == 0

    # Remove this when implemented
    assert result.exception
    assert int(logger.handlers[0].level) == 10


def test_version():
    """Test the hardening command version output."""
    runner = CliRunner()
    args = shlex.split('--version')
    result = runner.invoke(cli, args)
    assert result.exit_code == 0
