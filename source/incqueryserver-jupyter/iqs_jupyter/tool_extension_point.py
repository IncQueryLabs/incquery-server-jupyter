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
Created on 2019. máj. 24.

@author: Gabor Bergmann
'''

from typing import Optional, Callable, List, Any  # @UnusedImport

# connector-specific extensions may add tools such as browser widgets here
class IQSJupyterTools:
    def __init__(
        self,
        iqs
    ):
        self._iqs = iqs


# connector-specific extensions may add custom ways to convert a dict to an element representation; 
#     parse a dict and return the constructed element or None if not the right format
#     default is ElementInCompartmentDescriptor 
element_dict_recognizers : List[Callable[[dict], Optional[Any]]] = []

