"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the basic model instantiation.
"""

import pytest

from hardening_importer.models import HardeningManifest
from hardening_importer.exceptions import ChecksumValidationError
from .conftest import VALID_MANIFESTS, INVALID_MANIFESTS


def test_resource_download(caplog, new_folder):
    """Test downloading and validating known-good resources."""
    # Force verbose logging during tests
    for manifest_file in VALID_MANIFESTS:
        manifest = HardeningManifest.from_yaml(manifest_file)
        manifest.download_resources()
        assert "Writing file to" in caplog.text


def test_resource_validation_error(new_folder):
    """Test downloading and failing validation on known-bad resources."""
    # Force verbose logging during tests
    for manifest_file in INVALID_MANIFESTS:
        if "bad_hash" in manifest_file:
            manifest = HardeningManifest.from_yaml(manifest_file)
            with pytest.raises(ChecksumValidationError,
                               match="did not match the expected"):
                manifest.download_resources()
