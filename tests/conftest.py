"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This module contains test configuration for pytest.
"""

import os

example_dir = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '../examples'
))

VALID_MANIFESTS = [
    f'{example_dir}/example_hardening_manifest.yaml'
]
INVALID_MANIFESTS = [
]
