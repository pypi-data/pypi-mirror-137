"""
apthesaurus
"""

import codecs
import os.path
from pathlib import Path

from setuptools import find_packages, setup


def read(rel_path):
    """
    read
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as f_p:
        return f_p.read()


def get_version(rel_path):
    """
    get_version
    """
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


# read the contents of your README file
DIR = Path(__file__).parent
LONG_DESCRIPTION = (DIR / "README.md").read_text()

setup(
    name="apthesaurus",
    author="Stefan Heitmüller",
    author_email="stefan.heitmueller@root360.de",
    license="MIT",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    python_requires="~=3.8",
    packages=find_packages(),
    version=get_version("apthesaurus/version/__init__.py"),
    install_requires=[
        "sanic==21.12.1",
        "sanic-ext==22.1.2",
    ],
    entry_points={
        "console_scripts": [
            "apthesaurus=apthesaurus:run"
        ],
    },
    include_package_data=True,
)
