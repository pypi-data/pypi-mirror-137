#!/usr/bin/env python

from setuptools import setup

setup(
    name="kropotkin",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": "kropotkin/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    packages=["kropotkin"],
    description="Hooks for stateless Django apps",
    install_requires=["msgpack", "hhc"],
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    extras_require={
        "test": ["pytest", "hypothesis", "pytest-pikachu", "pytest-mypy"],
    },
)
