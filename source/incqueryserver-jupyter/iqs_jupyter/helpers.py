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
Created on 2019. nov. 27.

@author: Gabor Bergmann
'''

import html

import iqs_jupyter.tool_extension_point as ext_point


def cell_to_html(cell):
    if hasattr(cell, '_repr_html_'):
        return cell._repr_html_()
    elif isinstance(cell, str):
        return html.escape(cell)
    else:
        return str(cell)

def dict_to_element(dict_or_attribute_value, url_provider=None):
    if isinstance(dict_or_attribute_value, dict):
        for recognizer in ext_point.element_dict_recognizers:
            recognized = recognizer(dict_or_attribute_value)
            if recognized:
                if url_provider is not None:
                    recognized.url = url_provider(recognized)
                return recognized
        # not recognized as an element, treated as raw dict    
        return dict_or_attribute_value
    else:
        return dict_or_attribute_value

