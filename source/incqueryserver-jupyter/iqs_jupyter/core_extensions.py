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
Created on 2019-04-09

@author: Gábor Bergmann
'''

from typing import Optional
import html
import collections

import ipywidgets as widgets
from IPython.display import display

import iqs_client

## TODO separate TWC-specific, MMS-specific and core parts into separate files if possible (re-export of core?)
## TODO refactor: pull up TWC-independent parts of (a) revision selector widget (retrofit mms commit selector) and (b) OSMC element info widget

import iqs_jupyter.config_defaults as defaults
import iqs_jupyter.tool_extension_point as ext_point

# recognizing element-in-compartment descriptors in match results

def _recognize_element_in_compartment_descriptor(
        dict_of_element : dict
) -> Optional[iqs_client.ElementInCompartmentDescriptor]:
    if "relativeElementID" in dict_of_element:
        return iqs_client.ElementInCompartmentDescriptor(
            **dict(
                (py_name, dict_of_element[json_name]) 
                for py_name, json_name in iqs_client.ElementInCompartmentDescriptor.attribute_map.items()
            )
        )
    else:
        return None
        
ext_point.element_dict_recognizers.append(_recognize_element_in_compartment_descriptor)


def _dict_to_element(dict_or_attribute_value, url_provider=None):
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


## monkey patch section

def _monkey_patch_element_in_compartment_descriptor_repr_html(self):
    if hasattr(self, 'url'):
        return '<a href="{}" title="{}">element #{}</a>'.format(html.escape(self.url), html.escape(self),
                                                                html.escape(self.relative_element_id))
    else:
        return '<span title="{}">element #{}</span>'.format(html.escape(self.to_str()),
                                                            html.escape(self.relative_element_id))




def _monkey_patch_model_compartment_get_element_in_compartment_by_id(self, relative_element_id):
    return iqs_client.ElementInCompartmentDescriptor(
        compartment_uri=self.compartment_uri,
        relative_element_id=relative_element_id
    )

def _monkey_patch_model_compartment_is_loaded_by_server(self, iqs):
    in_memory_compartments_response = iqs.in_memory_index.list_inmemory_model_compartments()
    return self in in_memory_compartments_response.inmemory_model_compartments


def _monkey_patch_query_execution_response_to_data_frame(self, url_provider=None):
    import pandas as pd
    return pd.DataFrame(self.to_list_of_matches(url_provider))

def _monkey_patch_query_execution_response_to_list_of_matches(self, url_provider=None):
    return [dict((arg.parameter, _dict_to_element(arg.value, url_provider)) for arg in match.arguments) for match in
            self.matches]

#****
    
def _monkey_patch_typed_element_in_compartment_repr_html(self):
    type_html = html.escape(self.type if self.type else "<untyped>")
    element_html = self.element._repr_html_()
    if self.name:
        return "'{}' ({}) {}".format(html.escape(self.name), type_html, element_html)
    elif self.type:
        return "<unnamed> ({}) {}".format(type_html, element_html)
    else:
        return element_html

def _monkey_patch_generic_validation_rule_repr_html(self):
    return '<span title="{}">{} occurrences of "{}" <i>(see hover for details)</i></span> {}'.format(
        html.escape(self.to_str()),
        len(self.matching_elements),
        html.escape(self.message),
        "<ul>{}</ul>".format(
            "\n".join([
                "<li>{}</li>".format(
                    typed_diag_element.element._repr_html_()
                )
                for typed_diag_element in self.matching_elements
            ])
        )
    )
    
    
def _monkey_patch_generic_validation_results_to_data_frame(self):
    import pandas as pd
    return pd.DataFrame([item._asdict() for item in self.to_list_of_diagnostic_items()])


def _monkey_patch_generic_validation_results_to_list_of_diagnostic_items(self):
    return [
        ValidationDiagnosticItem(
            rule.constraint.type, rule.constraint.name, rule.constraint.element.relative_element_id, rule.constraint.element,
            rule.severity, rule.message,
            typed_diag_element.type, typed_diag_element.name, typed_diag_element.element.relative_element_id, typed_diag_element.element
        )
        for rule in self.rules
        for typed_diag_element in rule.matching_elements
    ]
    
def _monkey_patch_generic_validation_results_repr_html(self):
    diag_entries = self.to_list_of_diagnostic_items()
    table_html = "" if not diag_entries else '''
        <div>
            <table border="1">
                <thead>
                    <tr style="text-align: right;">
                        <th>Severity</th>
                        <th>Rule name</th>
                        <th>Message</th>
                        <th>Element type</th>
                        <th>Element name</th>
                        <th>Element</th>
                    </tr>
                </thead>
                <tbody>
                    {}
                </tbody>
            </table>
        </div>
    '''.format(
        "\n".join([
            "<tr>{}</tr>".format(
                " ".join([
                    "<td>{}</td>".format(field)
                    for field in [
                        html.escape(diag_entry.severity),
                        html.escape(diag_entry.constraint_element_name), 
                        html.escape(diag_entry.message), 
                        html.escape(diag_entry.matching_element_type), 
                        html.escape(diag_entry.matching_element_name), 
                        diag_entry.matching_element._repr_html_()
                    ]
                ])
            )
            for diag_entry in diag_entries
        ])
    )
    return '<span title="{}">Validation results: {} diagnostic items <i>(see hover for details)</i></span> {}'.format(
        html.escape(self.to_str()),
        len(diag_entries),
        table_html
    )
#     return '<span title="{}">Validation results <i>(see hover for details)</i></span> <ul>{}</ul>'.format(
#         html.escape(self.to_str()),
#         "\n".join([
#             "<li>{} ({}) {}</li>".format(
#                 html.escape(diag_type), 
#                 str(diag_count),
#                 "" if not diag_count else "<ul>{}</ul>".format(
#                     "\n".join([
#                         '<li>{}</li>'.format(
#                             rule._repr_html_()
#                         )
#                         for rule in self.rules
#                         if rule.severity == diag_type and rule.matching_elements
#                     ])
#                 )
#             )
#             for diag_type, diag_count in self.diagnostics.to_dict().items()
#         ])
#     )
    
def _monkey_patch_generic_response_message_repr_html_(self):
    return '<span title="{}">{} <i>(see hover for details)</i></span>'.format(html.escape(self.to_str()), html.escape(self.message))

def _monkey_patch_query_fqn_list_repr_html_(self):
    ns_list = self.query_fq_ns
    if ns_list:
        list_body = "\n".join([
            "<li>{}</li>".format(html.escape(query_fqn)) for query_fqn in ns_list
        ])
        return '<span title="{}">Listing {} queri(es): <i>(see hover for details)</i></span> <ul>{}</ul>'.format(
            html.escape(self.to_str()), str(len(ns_list)), list_body)
    return '<span title="{}">No queries <i>(see hover for details)</i></span>'.format(html.escape(self.to_str()))

def _cell_to_html(cell):
    if hasattr(cell, '_repr_html_'):
        return cell._repr_html_()
    elif isinstance(cell, str):
        return html.escape(cell)
    else:
        return str(cell)

def _monkey_patch_query_execution_response_to_html(self):
    count_report = '<span title="{}">{} match(es) of query{}{} <i>(see hover for details)</i></span>'.format(
        html.escape(self.to_str()), 
        html.escape(str(self.match_set_size)),
        " '{}'".format(html.escape(self.query_fqn)) if self.query_fqn else "",
        " with bound parameter(s) '{}'".format(", ".join([html.escape(binding.parameter) for binding in self.binding])) if self.binding else ""
    )
    match_list = self.to_list_of_matches()
    
    if not match_list:
        return count_report
    
    pattern_params = match_list[0].keys()
    
    param_headers = " ".join(["<th>{}</th> ".format(html.escape(param)) for param in pattern_params])
    match_rows = "\n".join([
        "<tr><th>{}</th>{}</tr>\n".format(row_index," ".join([
            " <td>{}</td>".format(_cell_to_html(match_list[row_index][param])) for param in pattern_params
        ])) for row_index in range(len(match_list))
    ])
    
    param_bindings = " ".join([
        "<td>{}</td> ".format(" ".join([ # 0 or 1
            _cell_to_html(_dict_to_element(binding.value))
            for binding in self.binding
            if binding.parameter == param
        ]))
        for param in pattern_params
    ])
    param_bindings_row = '''
        <tr>
            <th></th>
            {}
        </tr>    
    '''.format(param_bindings)
    
    style = ""
    return '''
        {}
        <div>
        {}
        <table border="1">
            <thead>
                <tr style="text-align: right;">
                    <th></th>
                    {}
                </tr>
                {}
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
        </div>
    '''.format(count_report, style, param_headers, param_bindings_row, match_rows)

        

def _do_monkey_patching():
    iqs_client.ElementInCompartmentDescriptor._repr_html_ = _monkey_patch_element_in_compartment_descriptor_repr_html
    iqs_client.ModelCompartment.get_element_in_compartment_by_id = _monkey_patch_model_compartment_get_element_in_compartment_by_id
    iqs_client.ModelCompartment.is_loaded_by_server = _monkey_patch_model_compartment_is_loaded_by_server
    
    iqs_client.QueryExecutionResponse.to_list_of_matches = _monkey_patch_query_execution_response_to_list_of_matches
    iqs_client.QueryExecutionResponse.to_data_frame = _monkey_patch_query_execution_response_to_data_frame
    iqs_client.QueryExecutionResponse.to_data_frame = _monkey_patch_query_execution_response_to_data_frame
    iqs_client.QueryExecutionResponse._repr_html_ = _monkey_patch_query_execution_response_to_html  
    iqs_client.IndexMessage._repr_html_ = _monkey_patch_generic_response_message_repr_html_
    iqs_client.SimpleMessage._repr_html_ = _monkey_patch_generic_response_message_repr_html_
    iqs_client.QueryFQNList._repr_html_ = _monkey_patch_query_fqn_list_repr_html_
    
    # TODO TWC-specific version missing, as well as additional features
    iqs_client.GenericValidationResults.to_list_of_diagnostic_items = _monkey_patch_generic_validation_results_to_list_of_diagnostic_items
    iqs_client.GenericValidationResults.to_data_frame = _monkey_patch_generic_validation_results_to_data_frame
    iqs_client.GenericValidationResults._repr_html_ = _monkey_patch_generic_validation_results_repr_html
    iqs_client.GenericValidationRule._repr_html_ = _monkey_patch_generic_validation_rule_repr_html
    iqs_client.TypedElementInCompartmentDescriptor._repr_html_ = _monkey_patch_typed_element_in_compartment_repr_html

_do_monkey_patching()


## global utility functions

def binding(**kwargs):
    return [
        {"parameter": param_name, "value": param_value} 
        for param_name, param_value in kwargs.items()
    ]

def connect(
    address  = defaults.default_IQS_address,
    user     = defaults.default_IQS_username,
    password = defaults.default_IQS_password,
    auth_with_user_pw  = True    
):
    configuration = iqs_client.Configuration()
    configuration.host=address 
    if auth_with_user_pw:
        configuration.username=user
        configuration.password=password
    return IQSClient(configuration)


## useful widgets and clients

class IQSConnectorWidget:
    def __init__(
        self,
        ask_for_user_pw  = True,
        initial_address  = defaults.default_IQS_address,
        initial_user     = defaults.default_IQS_username,
        initial_password = defaults.default_IQS_password,
        address_label    = 'Address:',
        user_label       = 'User:',
        password_label   = 'Password:',
        labelText="IQS API Access Point",
        auto_display=True
    ):
        self.ask_for_user_pw = ask_for_user_pw
        
        self.address_field  = widgets.Text    (value=initial_address,  description=address_label)
        self.user_field     = widgets.Text    (value=initial_user,     description=user_label)
        self.password_field = widgets.Password(value=initial_password, description=password_label)
        
        if ask_for_user_pw:
            fields = [self.address_field, self.user_field, self.password_field]
        else:
            fields = [self.address_field]
        
        self.box=widgets.HBox([widgets.Label(value=labelText), widgets.VBox(fields)])
        if auto_display: self.display()
            
    def display(self):
        display(self.box)
        
    def _repr_html_(self):
        self.display()
        
    def api_client_configuration(self):
        configuration = iqs_client.Configuration()
        configuration.host=self.address_field.value 
        if self.ask_for_user_pw:
            configuration.username=self.user_field.value
            configuration.password=self.password_field.value
        return configuration
    
    def connect(self):
        return connect(
            address           = self.address_field.value,
            user              = self.user_field.value,
            password          = self.password_field.value,
            auth_with_user_pw = self.ask_for_user_pw
        )





# def _iqs_core_api_initilizer(iqs):
#     self.impact_analysis = iqs_client.ImpactAnalysisApi(core_api_client_iqs)
#     self.in_memory_index = iqs_client.InMemoryIndexApi(core_api_client_iqs)
#     self.persistent_index = iqs_client.PersistentIndexApi(core_api_client_iqs)
#     self.queries = iqs_client.QueriesApi(core_api_client_iqs)
#     self.query_execution = iqs_client.QueryExecutionApi(core_api_client_iqs)
#     self.repository = iqs_client.RepositoryApi(core_api_client_iqs)
#     self.server_management = iqs_client.ServerManagementApi(core_api_client_iqs)
#     self.validation = iqs_client.ValidationApi(core_api_client_iqs)    
#     self.integration = iqs_client.IntegrationApi(core_api_client_iqs)
#     self.mms_repository = iqs_client.MmsRepositoryApi(core_api_client_iqs)
#     self.experimental = iqs_client.ExperimentalApi(core_api_client_iqs)

# TODO auto-generate from dir(iqs_client.api) ? 
_iqs_client_api_classes = {
    'impact_analysis'   : "ImpactAnalysisApi",
    'in_memory_index'   : "InMemoryIndexApi",
    'persistent_index'  : "PersistentIndexApi",
    'queries'           : "QueriesApi",
    'query_execution'   : "QueryExecutionApi",
    'repository'        : "RepositoryApi",
    'server_management' : "ServerManagementApi",
    'validation'        : "ValidationApi",    
    'integration'       : "IntegrationApi",
    'mms_repository'    : "MmsRepositoryApi",
    'experimental'      : "ExperimentalApi"
}

class IQSClient:
    def __init__(
        self,
        configuration
    ):
        core_api_client_iqs = iqs_client.ApiClient(configuration)
        for api_field_name, api_class_name in _iqs_client_api_classes.items():
            if api_class_name in dir(iqs_client): # there might be api classes presently missing / disabled
                api_class = getattr(iqs_client, api_class_name)
                api_object = api_class(core_api_client_iqs)
                setattr(self, api_field_name, api_object)
        
        self.jupyter_tools = ext_point.IQSJupyterTools(self)



# custom validation result datatype 

ValidationDiagnosticItem = collections.namedtuple(
    "ValidationDiagnosticItem", 
    ['constraint_element_type', 'constraint_element_name', 'constraint_element_relative_id', 'constraint_element',
     'severity', 'message', 
     'matching_element_type', 'matching_element_name', 'matching_element_relative_id', 'matching_element']
)

