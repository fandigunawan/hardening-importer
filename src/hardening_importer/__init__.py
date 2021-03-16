"""Hardening Importer - Import IronBank Hardening Manifests for builds.

This package handles importing of IronBank Hardening Manifest YAML files and
producing useful things for build environments. Primarily, this means
downloading and validating resources required to build the images and
generating command lines for building the images with Kaniko as part of a
container-based CI system.
"""
