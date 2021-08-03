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
    IncQuery Server Client Extensions for Jupyter and Python

    Requires [IncQuery Server](https://incquery.io) to operate.


Created on 2019-05-17

@author: Gábor Bergmann
'''

# coding: utf-8
from iqs_jupyter.about import __version__

# end-user modules
from iqs_jupyter.core_extensions import *
from iqs_jupyter.authentication import *

if 'MmsRepositoryApi' in dir(iqs_client):
    from iqs_jupyter.mms_extensions import *
    from iqs_jupyter.mms_direct_extensions import *
    
if 'RepositoryApi' in dir(iqs_client):
    from iqs_jupyter.twc_extensions import *
    from iqs_jupyter.twc_osmc_extensions import *

if 'AnalysisApi' in dir(iqs_client):
    from iqs_jupyter.analysis_extensions import *

# namespace shortcut for API request/response classes
from iqs_client import models as schema


