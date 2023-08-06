"""Setup for package shapsplain
"""

import pkg_resources

from os import path
from setuptools import setup, find_packages

from shapsplain import __version__

here = path.abspath(path.dirname(__file__))

TF_VER = ">=2.8,<2.9"
M1 = "sys_platform=='Darwin' and platform_machine=='arm64'"
OTHER = "sys_platform!='Darwin' or platform_machine!='arm64'"

deps = [
    "numpy>=1.21,<1.22",
    "scikit-learn>=1.0,<1.1",
    "numba>=0.55,<0.56",
]

# The installation of `tensorflow-gpu` should be specific to canonical
# docker images distributed by the Tensorflow team.  If they've
# installed tensorflow-gpu, we shouldn't try to install tensorflow on
# top of them.
if not any(pkg.key == "tensorflow-gpu" for pkg in pkg_resources.working_set):
    deps += [
        # MacOS running on the M1 has a specific tensorflow build
        "tensorflow-macos%s;%s" % (TF_VER, M1),
        "tensorflow%s;%s" % (TF_VER, OTHER),
    ]

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
