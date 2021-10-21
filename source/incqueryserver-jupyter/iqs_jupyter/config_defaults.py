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

"""
Created on 2019. máj. 21.

@author: Gabor Bergmann
"""

_prefix = "IQS_JUPYTER_"

default_auto_display: bool = True
default_use_oidc: bool = False
default_use_password: bool = True
default_use_auth_header: bool = False

default_IQS_address  : str = None
default_IQS_username : str = None
default_IQS_password : str = None
default_IQS_token: str = None
default_IQS_auth_header_name: str = None
default_IQS_auth_header_value: str = None

default_twc_workspace : str = None
default_twc_resource  : str = None
default_twc_branch    : str = None
default_twc_revision  : int = None

default_mms_org     : str = None
default_mms_project : str = None
default_mms_ref     : str = None
default_mms_commit  : str = None

default_twc_osmc_address  : str = None
default_twc_osmc_username : str = None
default_twc_osmc_password : str = None

default_mms_address  : str = None
default_mms_username : str = None
default_mms_password : str = None


# try to override from env variables

    
# for var_name, default in [ # copy to avoid concurrent iteration
#     (var_name, default) 
#     for var_name, default in globals().items()
#     if var_name.startswith("default_")
# ]:
for var_name, default in [ # copy to avoid concurrent modification
    (var_name, default) 
    for var_name, default in globals().items()
    if var_name.startswith("default_")
]:
    from os import environ
    from typing import get_type_hints
    from sys import modules
    value = environ.get(_prefix + var_name)
    hint = get_type_hints(modules[__name__]).get(var_name)
    if value is None:
        globals()[var_name] = default
    else: 
        if hint == int:
            globals()[var_name] = int(value)
        else:
            globals()[var_name] = value

