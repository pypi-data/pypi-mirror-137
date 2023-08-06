"""Setup for package shapsplain
"""

import pkg_resources

from os import path
from setuptools import setup, find_packages

from shapsplain import __version__

here = path.abspath(path.dirname(__file__))

deps = [
    "numpy>=1.19,<1.20",
    "scikit-learn>=1.0,<1.1",
    "tensorflow>=2.7,<2.8",
    "numba>=0.55,<0.56",
]

# The installation of `tensorflow-gpu` should be specific to canonical
# docker images distributed by the Tensorflow team.  If they've
# installed tensorflow-gpu, we shouldn't try to install tensorflow on
# top of them.
if any(pkg.key == "tensorflow-gpu" for pkg in pkg_resources.working_set):
    deps = list(filter(lambda d: not d.startswith("tensorflow>="), deps))

# Get the long description from the relevant file
with open(path.join(here, "README.md"), "r") as f:
    long_description = f.read()

setup(
    name="shapsplain",
    version=__version__,
    author="BigML Team",
    author_email="team@bigml.com",
    url="http://bigml.com/",
    description="Wrapper for shapley explanations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests", "tests.*"]),
    test_suite="nose.collector",
    install_requires=deps,
)
