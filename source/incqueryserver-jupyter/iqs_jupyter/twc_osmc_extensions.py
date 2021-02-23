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
from ipywidgets.widgets.widget import Widget
from builtins import super

'''
Created on 2019. máj. 24.

@author: Gabor Bergmann
'''

from typing import Dict, Tuple, Any, Hashable, List

import ipywidgets as widgets
from IPython.display import display


import iqs_jupyter.config_defaults as defaults
import iqs_jupyter.abstract_widgets as abstract_widgets


class OSMCConnectorWidget:
    def __init__(
        self,
        initial_address = defaults.default_twc_osmc_address,
        initial_user    = defaults.default_twc_osmc_username,
        initial_pw      = defaults.default_twc_osmc_password,
        address_label='Address:',
        user_label='User:',
        pw_label='Password:',
        label_text="OSMC API Access Point",
        auto_display=True
    ):
        self.address_widget = widgets.Text    (value=initial_address, description=address_label)
        self.user_widget    = widgets.Text    (value=initial_user,    description=user_label)
        self.pw_widget      = widgets.Password(value=initial_pw,      description=pw_label)
        self.box=widgets.HBox([
            widgets.VBox([widgets.Label(value=label_text), widgets.Label(value=""), widgets.Label(value="")]),
            widgets.VBox([self.address_widget,             self.user_widget,        self.pw_widget])
        ])
        if auto_display: self.display()
            
    def display(self):
        display(self.box)
        
    def _repr_html_(self):
        self.display()    
          
    def connect(self, cache_locally = True):
        return OSMCClient(self.address_widget.value, (self.user_widget.value, self.pw_widget.value), cache_locally)


class OSMCClient:
    def __init__(
        self,
        access_point_prefix,
        auth,
        cache_locally = True
    ):
        if (access_point_prefix.endswith('/')):
            self.access_point_prefix = access_point_prefix
        else:
            self.access_point_prefix = access_point_prefix + '/'
        self.auth = auth
        self.cache_locally = cache_locally
        
    def element_api_link(self, element_descriptor):
        return "{}workspaces/{}/resources/{}/branches/{}/revisions/{}/elements/{}".format(
            self.access_point_prefix,
            element_descriptor.workspace_id,
            element_descriptor.resource_id,
            element_descriptor.branch_id,
            element_descriptor.revision_number,        
            element_descriptor.element_id
        )
        
    def element_batch_api_link(self, revision_descriptor):
        return "{}workspaces/{}/resources/{}/branches/{}/revisions/{}/elements".format(
            self.access_point_prefix,
            revision_descriptor.workspace_id,
            revision_descriptor.resource_id,
            revision_descriptor.branch_id,
            revision_descriptor.revision_number
        )
        
    def as_url_provider(self):
        def url_provider(element_descriptor):
            return self.element_api_link(element_descriptor)
        return url_provider
        
    def retrieve(self, element_descriptor):
        if hasattr(element_descriptor, 'raw_container_content') and hasattr(element_descriptor, 'raw_element_content'):
            return element_descriptor.raw_container_content, element_descriptor.raw_element_content
        else:
            return self.force_retrieve(element_descriptor)

    def force_retrieve(self, element_descriptor):
        raw_container_content, raw_element_content = self._retrieve_single(element_descriptor)
        if self.cache_locally:
            element_descriptor.raw_container_content = raw_container_content
            element_descriptor.raw_element_content = raw_element_content
        return raw_container_content, raw_element_content

    def _retrieve_single(self, element_descriptor):
        import requests
        req_url = self.element_api_link(element_descriptor)

        session = requests.session()
        osmc_response = session.get(req_url, auth=self.auth)
        osmc_response.raise_for_status()
        logout_response = session.get(f'{self.access_point_prefix}logout')
        logout_response.raise_for_status()

        raw_container_content, raw_element_content = osmc_response.json()
        return raw_container_content, raw_element_content
        
    def retrieve_batch(self, element_descriptor_list):
        if self.cache_locally:
            action_needed = [
                element_descriptor 
                for element_descriptor in element_descriptor_list 
                if not (hasattr(element_descriptor, 'raw_container_content') and hasattr(element_descriptor, 'raw_element_content'))
            ]
            if action_needed:
                self.force_retrieve_batch(action_needed)

    def force_retrieve_batch(self, element_descriptor_list):
        from itertools import groupby
        grouping = groupby(element_descriptor_list, lambda element_descriptor: element_descriptor.get_containing_revision())
        for revision_descriptor, group_with_same_descriptor in grouping:
            raw_content_dict = self._retrieve_batch(revision_descriptor, group_with_same_descriptor)
            if self.cache_locally:
                for element_descriptor in element_descriptor_list:
                    element_result_dict = raw_content_dict[element_descriptor.element_id]
                    if element_result_dict["status"] == 200: 
                        raw_container_content, raw_element_content = element_result_dict["data"]
                        element_descriptor.raw_container_content = raw_container_content
                        element_descriptor.raw_element_content = raw_element_content

    def _retrieve_batch(self, revision_descriptor, element_descriptor_list):
        element_id_set = set([element_descriptor.element_id for element_descriptor in element_descriptor_list])
        import requests
        req_url = self.element_batch_api_link(revision_descriptor)
        req_body = ','.join(element_id_set)

        session = requests.session()
        osmc_response = session.post(req_url, data=req_body, auth=self.auth)
        osmc_response.raise_for_status()
        logout_response = session.get(f'{self.access_point_prefix}logout')
        logout_response.raise_for_status()

        return osmc_response.json()

    def element_short_string(self, element_descriptor):
        raw_container_content, raw_element_content = self.retrieve(element_descriptor)
        return _twc_element_short_string(raw_container_content, raw_element_content)
        
    def show_element_info_widget(self, element_descriptor, **kwargs):
        return TWCElementInfoWidget(osmc=self, initial_element=element_descriptor, **kwargs)

def _twc_element_short_string(raw_container_content, raw_element_content):
    # nsUri = raw_element_content["kerml:nsURI"]
    qualified_type = raw_element_content.get("@type", "(untyped)")#.split(':')
    #meta_package = qualified_type[0]
    #type = qualified_type[1]
    name = raw_element_content.get("kerml:name", None)
    _id = raw_element_content.get("kerml:esiID", '<unknown ID>')
    if name:
        return "'{}' ({}) #{}".format(name, qualified_type, _id)
    else:
        return "<unnamed> ({}) #{}".format(qualified_type, _id)



class TWCElementInfoWidget(abstract_widgets.AbstractElementInfoWidget):
    def __init__(
        self,
        osmc,
        initial_element,
        **kwargs
    ):
        self.osmc = osmc
        self.initial_element = initial_element
        self.element_id_to_descriptor = {}
        super().__init__(self, **kwargs)
        self.show_element_pane(initial_element)
    
    def _unpack_element(self, element) -> Tuple[str, Dict[str, Any]]:
        raw_container_content, raw_element_content = self.osmc.retrieve(element)
        header = _twc_element_short_string(raw_container_content, raw_element_content)
        field_values = raw_element_content.get('kerml:esiData', {})
        return header, field_values
    
    def _do_retrieve_batch(self, element, field_values):
        self.osmc.retrieve_batch([element_descriptor
            for field,value in field_values.items()
            if (value)
            for element_descriptor in self._value_element_descriptor_list(value)
        ])
    def _value_element_descriptor_list(self, value):
        import collections
        if isinstance(value, str):
            return []
        elif isinstance(value, collections.abc.Sequence): # test string-ness before this
            flat_list_descriptors = [ descriptor
                for item in value 
                for descriptor in self._value_element_descriptor_list(item)
            ]
            return flat_list_descriptors
        elif isinstance(value, dict) and '@id' in value:
            referred_element = self._element_descriptor_for_id(value['@id'])
            return [referred_element]
        else:
            return []

    def _to_hashable_identifier(self, element) -> Hashable:
        return element.element_id

    def _to_field_display_name(self, element, field) -> str:
        return field

    def _value_widget_list(self, element, field, value) -> List[Widget]:
        import collections
        if isinstance(value, str):
            return [self._create_value_widget_attribute(value)]#'"{}"'.format(value))
        elif isinstance(value, collections.abc.Sequence): # test string-ness before this
            flat_list_widgets = [ widget
                for item in value 
                for widget in self._value_widget_list(element, field, item)
            ]
            return flat_list_widgets
        elif isinstance(value, dict) and '@id' in value:
            referred_element = self._element_descriptor_for_id(value['@id'])
            short_text = self.osmc.element_short_string(referred_element)
            long_text = 'Click to open pane for element {} found at {}'.format(short_text, referred_element.to_descriptor_str())
            return [self._create_value_widget_reference(referred_element, short_text, long_text)]
        else:
            return [self._create_value_widget_attribute(value)]

    def _element_descriptor_for_id(self, element_id):
        if element_id not in self.element_id_to_descriptor:
            self.element_id_to_descriptor[element_id] = self.initial_element.resolve_reference(element_id)
        return self.element_id_to_descriptor[element_id]

