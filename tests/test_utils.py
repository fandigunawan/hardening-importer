"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the commun utilities like the logger.
"""

from hardening_importer.util import get_logger


def test_normal_logger():
    """Test that a normal logger works as expected."""
    logger = get_logger()
    logger2 = get_logger()
    assert logger == logger2
    logger.handlers.clear()


def test_new_verbose_logger():
    """Test that creating a verbose logger from nothing works as expected."""
    logger = get_logger(verbosity=3)
    assert int(logger.handlers[0].level) == 10
    logger.handlers.clear()


def test_verbose_logger():
    """Test that a verbose logger correctly overrides a normal one."""
    logger = get_logger()
    assert int(logger.handlers[0].level) == 40

    logger = get_logger(verbosity=3)
    assert int(logger.handlers[0].level) == 10

    logger2 = get_logger()
    assert logger == logger2
    logger.handlers.clear()
