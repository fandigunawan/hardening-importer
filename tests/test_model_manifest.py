"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module provides tests for the basic model instantiation.
"""

import pytest
from pprint import pprint
from pydantic import ValidationError

from hardening_importer.models import HardeningManifest
from hardening_importer.models.common import StrEnum
from .conftest import VALID_MANIFESTS, INVALID_MANIFESTS


def test_str_enum():
    """Test functionality of our StrEnum construct."""
    class TestStrEnum(StrEnum):
        """A construct to validate StrEnum functionality."""

        VAR_1 = 'Enum Variable 1'
        VAR_2 = 'Enum Variable 2'

    # Validate list classmethod
    assert TestStrEnum.list() == ['Enum Variable 1', 'Enum Variable 2']
    # Validate instantiation and string comparison
    testenum = TestStrEnum('Enum Variable 1')
    assert testenum == 'Enum Variable 1'
    # Validate Enum restrictions on value
    with pytest.raises(ValueError, match='is not a valid'):
        _ = TestStrEnum('Enum Variable 3')


def test_valid_manifest():
    """Test loading and dumping a valid manifest."""
    for manifest_file in VALID_MANIFESTS:
        print(manifest_file)
        manifest = HardeningManifest.from_yaml(manifest_file)
        pprint(manifest)


def test_invalid_config():
    """Test load invalid manifests."""
    for manifest_file in INVALID_MANIFESTS:
        if 'bad_hash' not in manifest_file:
            with pytest.raises(ValidationError):
                _ = HardeningManifest.from_yaml(manifest_file)
