# Copyright 2019 IncQuery Labs Ltd.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#  http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Created on 2019-05-17

@author: Gábor Bergmann
'''
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = ["incqueryserver-api-python-client"]

setuptools.setup(
    name="incqueryserver-jupyter",
    version="0.10.0",
    author="Gábor Bergmann",
    author_email="gabor.bergmann@incquerylabs.com",
    description="IncQuery Server Client Extensions for Jupyter and Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IncQueryLabs/incquery-server-jupyter",
    install_requires=REQUIRES,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
)