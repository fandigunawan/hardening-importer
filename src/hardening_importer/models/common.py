"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module is for encapsulating common model resources.
"""


from enum import Enum


class StrEnum(str, Enum):
    """Represent a choice between a fixed set of strings.
    A mix-in of string and enum, representing itself as the string value.
    """

    @classmethod
    def list(cls) -> list:
        """Return a list of the available options in the Enum."""
        return [e.value for e in cls]
