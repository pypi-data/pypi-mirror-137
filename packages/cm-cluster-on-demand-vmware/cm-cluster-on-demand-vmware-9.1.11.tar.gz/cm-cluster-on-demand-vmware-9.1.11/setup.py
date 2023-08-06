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

import subprocess

from setuptools import find_packages, setup
from setuptools.command.develop import develop
from setuptools.command.install import install

try:
    from clusterondemandvmware._version import version as __version__
except ImportError:
    from setuptools_scm import get_version
    __version__ = get_version(
        root="..",
        relative_to="__file__",
        write_to="cluster-on-demand-vmware/clusterondemandvmware/_version.py"
    )


class PostDevelopCommand(develop):
    def run(self):
        develop.run(self)
        install_vmware_dependencies()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        install_vmware_dependencies()


def install_vmware_dependencies():
    """
    Install the VMware Vsphere APIs from Github.

    VMware only publishes the vSphere automation SDK on Github. Pipy requires every required package to be
    hosted on Pipy, this means that we need to install the VMware dependencies in a post install step.
    """
    # When running tox we need to install the dependencies in the tox supplied virtual environment.
    # Since pip will automatically resolve to either the active virtualenv or the base Python we need
    # to ensure that we use the tox suplied pip which we inject via the _PEP environment variable.
    pip_install = ["pip", "install"]
    pip_install.append("vapi-runtime @ https://github.com/vmware/vsphere-automation-sdk-python/raw/7.0.0.1/lib/vapi-runtime/vapi_runtime-2.15.0-py2.py3-none-any.whl")  # noqa
    pip_install.append("vapi-client-bindings @ https://github.com/vmware/vsphere-automation-sdk-python/raw/7.0.0.1/lib/vapi-client-bindings/vapi_client_bindings-3.3.0-py2.py3-none-any.whl")  # noqa
    pip_install.append("vapi-common-client @ https://github.com/vmware/vsphere-automation-sdk-python/raw/7.0.0.1/lib/vapi-common-client/vapi_common_client-2.15.0-py2.py3-none-any.whl")  # noqa
    pip_install.append("nsx-policy-python-sdk   @ https://github.com/vmware/vsphere-automation-sdk-python/raw/7.0.0.1/lib/nsx-policy-python-sdk/nsx_policy_python_sdk-2.5.1.0.1.15419398-py2.py3-none-any.whl")  # noqa
    subprocess.run(pip_install, check=True)


with open("README.md", "r") as file_in:
    readme = file_in.read()

setup(
    name="cm-cluster-on-demand-vmware",
    version=__version__,
    description="Bright Cluster on Demand for VMWare",
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
    entry_points={
        "console_scripts": [
            "cm-cod-vmware = clusterondemandvmware.cli:cli_main"
        ]
    },
    tests_require=["pytest", "pycoverage"],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "setuptools_scm>=4.1.2",
        "tenacity>=6.2.0",
        "cm-cluster-on-demand==" + __version__,
        "cm-cluster-on-demand-config==" + __version__,
        "pyVmomi>=6.7",
    ],
    setup_requires=["setuptools_scm>=4.1.2"],
    cmdclass={
        "develop": PostDevelopCommand,
        "install": PostInstallCommand,
    }
)
