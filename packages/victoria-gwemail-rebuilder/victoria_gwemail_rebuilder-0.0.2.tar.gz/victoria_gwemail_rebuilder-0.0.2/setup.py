"""setup.py

Used for creation and DESTRUCTION of Glasswall Email environments

Author:
    Josh Moulder <jmoulder@glasswallsolutions.com>
"""
from setuptools import setup, find_packages


def repo_file_as_string(file_path: str) -> str:
    with open(file_path, "r") as repo_file:
        return repo_file.read()


setup(
    dependency_links=[],
    install_requires=[
        "click", "marshmallow", "pyyaml", "requests", "azure-devops",
        "victoria"
    ],
    name="victoria_gwemail_rebuilder",
    version="0.0.2",
    description=
    "Victoria Plugin that allows the creation and DESTRUCTION of Glasswall Email on the cloud.",
    long_description=repo_file_as_string("README.md"),
    long_description_content_type="text/markdown",
    author="Josh Moulder",
    packages=find_packages(),
)