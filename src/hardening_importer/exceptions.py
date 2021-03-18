"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains exceptions for use in the Hardening Importer.
"""


class ChecksumValidationError(Exception):
    """Raised when checksum validation of a file fails."""

    pass
