#!/usr/bin/env python3

# Copyright 2017-2021, Schlumberger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import setuptools, os

with open("README.md", "r") as fh:
    long_description = fh.read()

version   = "0.2." + (os.getenv("AZURE_BUILDID", "dev0") or "dev0")

setuptools.setup(
    name="OpenZGY",
    license='Apache',
    version=version,
    #use_scm_version={"root": "..", "relative_to": __file__},
    author="Paal Kvamme",
    author_email="somebody@slb.com", # TODO-High: Change!
    description="Library to access Schlumberger ZGY files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://openzgy.paalsinehoner.net",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    install_requires=['numpy>=1.17', 'matplotlib<3.4', 'pillow', 'zfpy==0.5.5'],
    setup_requires=['setuptools', 'setuptools_scm'],
    # TODO-Low, rename scripts to match command names or vice versa.
    entry_points={
        "console_scripts": [
            "zgydump = openzgy.tools.zgydump:Main",
            "zgycopy = openzgy.tools.copy:Main",
        ],
        "gui_scripts": [
            "zgygui  = openzgy.tools.gui_copy:Main",
        ]
    }
)
