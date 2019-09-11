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
from typing import Any, Dict, Tuple, Hashable, List
from ipywidgets.widgets.widget import Widget
'''
Created on 2019. júl. 4.

@author: Gabor Bergmann
'''

import mms_python_client as mms_python_client

import iqs_client

import iqs_jupyter.config_defaults as defaults
from iqs_jupyter import abstract_widgets



_mms_client_api_classes = {
    'artifact'   : 'ArtifactApi',     
    'element'    : 'ElementApi',      
    'org'        : 'OrgApi',          
    'other'      : 'OtherApi',        
    'project'    : 'ProjectApi',      
    'ref'        : 'RefApi',          
    'ticket'     : 'TicketApi'        
}


class MMSClient:
    def __init__(
        self, 
        address  = defaults.default_mms_address,
        user     = defaults.default_mms_username,
        password = defaults.default_mms_password,
        cache_element_details_locally = True
    ):
        if (address.endswith('/')):
            self.address = address
        else:
            self.address = address + '/'

        configuration = mms_python_client.Configuration( )
        configuration.host=address 
        configuration.username=user
        configuration.password=password
        
        core_api_client_mms = mms_python_client.ApiClient(configuration)
        for api_field_name, api_class_name in _mms_client_api_classes.items():
            if api_class_name in dir(mms_python_client): # there might be api classes presently missing / disabled
                api_class = getattr(mms_python_client, api_class_name)
                api_object = api_class(core_api_client_mms)
                setattr(self, api_field_name, api_object)
        # get_elements_in_batch
        
        self.helpers = MMSHelpers(self, cache_element_details_locally)
        
        
class MMSHelpers:
    RAW_ELEMENT_CONTENT='_raw_element_content'
    
    # not to be treated as in-model cross-references
    META_REF_FIELDS={'_commitId','_elasticId','_refId','_inRefIds','_projectId','mountedElementId','mountedElementProjectId','mountedRefId'} 
    
    def __init__(
        self, 
        mms,
        cache_locally = True
    ):
        self.mms = mms
        self.cache_locally = cache_locally
        
    def retrieve(self, element):
        if hasattr(element, MMSHelpers.RAW_ELEMENT_CONTENT):
            return getattr(element, MMSHelpers.RAW_ELEMENT_CONTENT)
        else:
            return self.force_retrieve(element)

    def force_retrieve(self, element):
        raw_element_content = self._retrieve_single(element)
        if self.cache_locally:
            setattr(element, MMSHelpers.RAW_ELEMENT_CONTENT, raw_element_content)
        return raw_element_content

    def _retrieve_single(self, element):
        commit = iqs_client.MMSCommitDescriptor.from_compartment_uri_or_none(element.compartment_uri)
        if not commit:
            return None
            
        try:
            elements_response = self.mms.element.get_element(
                project_id=commit.project_id, 
                ref_id=commit.ref_id, 
                commit_id=commit.commit_id,
                element_id=element.relative_element_id,    
            )
            if (elements_response.elements):
                return elements_response.elements[0].to_dict()
            else:
                return None
        except:
            return None
    
        
    def retrieve_batch(self, element_in_compartment_list):
        if self.cache_locally:
            action_needed = [
                element 
                for element in element_in_compartment_list 
                if not (hasattr(element, MMSHelpers.RAW_ELEMENT_CONTENT))
            ]
            if action_needed:
                self.force_retrieve_batch(action_needed)

    def force_retrieve_batch(self, element_in_compartment_list):
        from itertools import groupby
        grouping = groupby(element_in_compartment_list, lambda element: element.compartment_uri)
        for compartment_uri, group_with_same_compartment in grouping:
            raw_content_dict = self._retrieve_batch(compartment_uri, group_with_same_compartment)
            if self.cache_locally:
                for element in element_in_compartment_list:
                    if element.relative_element_id in raw_content_dict:
                        raw_element_content = raw_content_dict[element.relative_element_id]
                        setattr(element, MMSHelpers.RAW_ELEMENT_CONTENT, raw_element_content)

    def _retrieve_batch(self, compartment_uri, element_in_compartment_list):
        commit = iqs_client.MMSCommitDescriptor.from_compartment_uri_or_none(compartment_uri)
        if not commit:
            return {}
            
        rejectable_elements_response = self.mms.element.get_elements_in_batch(
            project_id=commit.project_id, 
            ref_id=commit.ref_id, 
            commit_id=commit.commit_id,
            body={'elements':[
                {'id': element.relative_element_id}
                for element in element_in_compartment_list
            ]},    
        )
        return {
            raw_element.id: raw_element.to_dict()
            for raw_element in rejectable_elements_response.elements
        }
        
    def element_short_string(self, element):
        raw_element_content = self.retrieve(element)
        return _mms_element_short_string(element, raw_element_content)
        
    def show_element_info_widget(self, 
                                 element, #element_id or element_in_compartment
                                 org_id=None,
                                 project_id=None,
                                 ref_id=None,
                                 commit_id=None, 
                                 **kwargs):
        if (org_id and project_id and ref_id and commit_id):
            commit = iqs_client.MMSCommitDescriptor.from_fields(
                org_id=org_id, project_id=project_id, ref_id=ref_id, commit_id=commit_id
            )
            element = iqs_client.ElementInCompartmentDescriptor(
                compartment_uri = commit.to_compartment_uri(),
                relative_element_id = element  # assume `element` is relative element id
            )            
        
        return MMSElementInfoWidget(mms_helper=self, initial_element=element, **kwargs)
        

def _mms_element_short_string(element, raw_element_content):
    if not raw_element_content:
        return "<missing element> #{}".format(element.relative_element_id)

    # nsUri = raw_element_content["kerml:nsURI"]
    qualified_type = raw_element_content.get("type", "<untyped>")#.split(':')
    #meta_package = qualified_type[0]
    #type = qualified_type[1]
    name = raw_element_content.get("name", None)
    _id = element.relative_element_id #raw_element_content.get("id", '<unknown ID>')
    if name:
        return "'{}' ({}) #{}".format(name, qualified_type, _id)
    else:
        return "<unnamed> ({}) #{}".format(qualified_type, _id)

class MMSElementInfoWidget(abstract_widgets.AbstractElementInfoWidget):
    def __init__(
        self,
        mms_helper,
        initial_element,
        **kwargs
    ):
        self.mms_helper = mms_helper
        self.initial_element = initial_element
        self.element_id_to_element = {}
        super().__init__(self, **kwargs)
        self.show_element_pane(initial_element)
    
    def _unpack_element(self, element) -> Tuple[str, Dict[str, Any]]:
        raw_element_content = self.mms_helper.retrieve(element)
        header = _mms_element_short_string(element, raw_element_content)
        field_values = raw_element_content if raw_element_content else {}
        return header, field_values
    
    def _do_retrieve_batch(self, element, field_values):
        self.mms_helper.retrieve_batch([element_ref
            for field,value in field_values.items()
            if (value)
            for element_ref in self._value_element_ref_list(element, field, value)
        ])
    def _value_element_ref_list(self, element, field, value):
        if field.endswith("Id") and not field in MMSHelpers.META_REF_FIELDS:
            return [self._element_for_id(value)]
        elif field.endswith("Ids") and not field in MMSHelpers.META_REF_FIELDS:
            return [
                self._element_for_id(item)
                for item in value
            ]
        #elif isinstance(value, dict) and 'id' in value:
        #    referred_element = self._element_for_id(value['id'])
        #    return [referred_element]
        else:
            return []

    def _to_hashable_identifier(self, element) -> Hashable:
        return element.relative_element_id

    def _to_field_display_name(self, element, field) -> str:
        if field.endswith("Id"):
            return field[:-2]
        elif field.endswith("Ids"):
            return field[:-3]
        else:
            return field
        
    def _value_widget_list(self, element, field, value) -> List[Widget]:
        import collections
        if field.endswith("Id") and not field in MMSHelpers.META_REF_FIELDS:
            return [self._ref_widget(element, value)]
        elif field.endswith("Ids") and not field in MMSHelpers.META_REF_FIELDS:
            return [
                self._ref_widget(element, item)
                for item in value
            ]
        elif isinstance(value, str):
            return [self._create_value_widget_attribute(value)]#'"{}"'.format(value))
        elif isinstance(value, collections.abc.Sequence): # test string-ness before this
            return [
                self._ref_or_attrib_widget(element, item) 
                for item in value 
            ]
        else:
            return [self._ref_or_attrib_widget(element, value)]
        
    def _ref_widget(self, src_element, value):
        referred_element = self._element_for_id(value)
        short_text = self.mms_helper.element_short_string(referred_element)
        long_text = 'Click to open pane for element {}'.format(short_text)
        return self._create_value_widget_reference(referred_element, short_text, long_text)

    def _ref_or_attrib_widget(self, element, value):
        if isinstance(value, dict) and 'id' in value:
            _id = value['id']
            referred_element = self._element_for_id(_id)
            if not hasattr(referred_element, MMSHelpers.RAW_ELEMENT_CONTENT):
                setattr(referred_element, MMSHelpers.RAW_ELEMENT_CONTENT, value)
            return self._ref_widget(element, _id)
        else:
            return self._create_value_widget_attribute(value)
    
    

    def _element_for_id(self, element_id):
        if element_id not in self.element_id_to_element:
            self.element_id_to_element[element_id] = self.initial_element.resolve_reference(element_id)
        return self.element_id_to_element[element_id]

