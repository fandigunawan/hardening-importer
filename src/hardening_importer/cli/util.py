"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains the utility CLI functions like reusable argument
definitions.
"""

import click


def verbose_opt(func):
    """Wrap the function in a click.option for verbosity."""
    return click.option(
        "-v", "--verbose", count=True,
        help="Increase verbosity (specify multiple times for more)."
    )(func)
