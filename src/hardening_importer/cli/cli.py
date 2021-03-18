"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains the main CLI functions based on Click.
"""

import click
import sys

from .. import __version__
from ..util import get_logger
from .util import verbose_opt


@click.group()
@verbose_opt
@click.version_option(version=__version__)
def main(verbose):
    """Work with Iron Bank Hardening Manifests.

    This client is designed to consume downloaded/cloned repositories from
    Iron Bank that are used to build container images. These image repositories
    have been designed to utilize infrastructure and processes that exist only
    inside Platform One, but be independantly consumable and repeatable.
    """
    logger = get_logger(verbose)
    logger.debug(sys.argv)
    logger.debug(f'verbose: {verbose}')


@main.command('import')
@verbose_opt
def import_manifest(verbose):
    """Import an Iron Bank Hardening Manifest for image builds."""
    logger = get_logger(verbose)
    logger.debug(sys.argv)
    logger.debug(f'verbose: {verbose}')
    raise NotImplementedError('This work is TBD.')
