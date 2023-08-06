#!/usr/bin/env python
# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import

from setuptools import find_packages, setup

try:
    from clusterondemand._version import version as __version__
except ImportError:
    from setuptools_scm import get_version
    __version__ = get_version(
        root="..",
        relative_to="__file__",
        write_to="cluster-on-demand/clusterondemand/_version.py"
    )

with open("README.md", "r") as file_in:
    readme = file_in.read()

setup(
    name="cm-cluster-on-demand",
    version=__version__,
    description="Bright Cluster on Demand Utility",
    author="Cloudteam",
    author_email="cloudteam@brightcomputing.com",
    url="https://www.brightcomputing.com/",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Clustering",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration"
    ],
    packages=find_packages(),
    package_data={"clusterondemand": ["license-bright-rhel.txt", "version-info.yaml"]},
    tests_require=["pytest", "pycoverage"],
    entry_points={
        "console_scripts": [
            "cm-cod = clusterondemand.cli:cli_main",
        ]
    },
    python_requires=">=3.7",
    install_requires=[
        "setuptools_scm>=4.1.2",
        "paramiko>=2.0",
        "netaddr>=0.7.18",
        "pytz>=2012d",
        "python_dateutil>=1.5",
        "PyYAML>=3.12",
        "prettytable~=0.7.2",
        "requests",
        "filelock>=2.0.8",
        "cm-cluster-on-demand-config==" + __version__
    ],
    setup_requires=["setuptools_scm>=4.1.2"]
)
