"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains the main CLI functions based on Click.
"""

from email.policy import default
import click
import os
import sys

from .. import __version__
from ..util import get_logger
from .util import verbose_opt
from ..models import HardeningManifest


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
@click.option('--manifest-path', '-m', default='hardening_manifest.yaml',
              type=click.Path(),
              help=('The path to a hardening manifest YAML file, relative to '
                    'PATH'))
@click.option('--dockerfile-path', '-d', default='Dockerfile',
              type=click.Path(),
              help='The path to the Dockerfile, relative to PATH')
@click.option('--build-executor', '-b', default='kaniko',
              type=click.Choice(['kaniko']),
              help=('The executor that a build argument list should be '
                    'prepared for.'))
@click.option('--registry', '-r', default='quay.io',
              help='The registry to which the image should be pushed.')
@click.option('--download-only', is_flag=True, help='Download only mode')
@click.argument('path', nargs=1, default='.',
                type=click.Path(
                    exists=True,
                    file_okay=False,
                    dir_okay=True,
                    resolve_path=True
                ))
def import_manifest(verbose, manifest_path, dockerfile_path, build_executor,
                    registry, path, download_only):
    """Import an Iron Bank Hardening Manifest for image builds."""
    logger = get_logger(verbose)
    logger.debug(sys.argv)
    logger.debug(f'verbose: {verbose}')
    if not (os.path.exists(manifest_path) and
            os.path.isfile(manifest_path)):
        raise click.FileError(manifest_path)

    manifest = HardeningManifest.from_yaml(manifest_path)
    manifest.download_resources()
    if not download_only:
        if not (os.path.exists(dockerfile_path) and
            os.path.isfile(dockerfile_path)):
            raise click.FileError(dockerfile_path)
        click.echo(' '.join(manifest.build_args(
            context_dir=path,
            dockerfile=dockerfile_path,
            registry=registry,
            executor=build_executor
        )))
