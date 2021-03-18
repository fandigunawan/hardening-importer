"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the models building argument strings for build
executors.
"""

import pytest

from hardening_importer.models import HardeningManifest

from .conftest import VALID_MANIFESTS


def test_build_args():
    """Test valid manifests with good build arguments."""
    for manifest_file in VALID_MANIFESTS:
        manifest = HardeningManifest.from_yaml(manifest_file)
        assert manifest.name in ' '.join(manifest.build_args(context_dir='.'))
        assert 'docker.io' in ' '.join(manifest.build_args(
            context_dir='.', registry='docker.io'
        ))
        assert './Containerfile' in ' '.join(manifest.build_args(
                context_dir='.', dockerfile='Containerfile'
        ))
        for tag in manifest.tags:
            assert tag in ' '.join(manifest.build_args(context_dir='.'))


def test_invalid_build_args():
    """Test valid manifests with bad arguments."""
    for manifest_file in VALID_MANIFESTS:
        manifest = HardeningManifest.from_yaml(manifest_file)
        with pytest.raises(RuntimeError, match='Unable to prepare'):
            manifest.build_args(context_dir='.', executor='docker')
