#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2021 Gabriele Orlando
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from setuptools import setup

#with open("README.md", "r") as fh:

#    long_description = fh.read()
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
     name='pyuul',
     include_package_data=True,
     version='0.3.2',

     author="Gabriele Orlando",

     author_email="orlando.gabriele89@gmail.com",

     description="A library to convert biological structures in completely differentiable tensorial representations, such as point clouds or voxelized grids . Everything is deep learning ready",

     #long_description=long_description,

     #long_description_content_type="text/markdown",

     url="https://bitbucket.org/grogdrinker/pyuul",
     
     packages=['pyuul','pyuul.sources'],
     package_dir={'pyuul': 'pyuul/','pyuul.sources':'pyuul/sources'},
     package_data={'pyuul': ['pyuul/parameters/**']},
     install_requires=["numpy","scipy","torch","torchvision"],


     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",

         "Operating System :: OS Independent",

     ],

 )
