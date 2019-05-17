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



import ipywidgets as widgets
import iqs_client


## TODO separate TWC-specific, MMS-specific and core parts into separate files if possible (re-export of core?)
## TODO refactor: pull up TWC-independent parts of (a) revision selector widget (retrofit mms commit selector) and (b) OSMC element info widget


## monkey patch section

def _monkey_patch_element_in_compartment_descriptor_repr_html(self):
    import html
    if hasattr(self, 'url'):
        return '<a href="{}" title="{}">element #{}</a>'.format(html.escape(self.url), html.escape(self),
                                                                html.escape(self.relative_element_id))
    else:
        return '<span title="{}">element #{}</span>'.format(html.escape(self.to_str()),
                                                            html.escape(self.relative_element_id))


def _monkey_patch_mms_commit_to_compartment_uri(self):
    return "mms-index:/orgs/{}/projects/{}/refs/{}/commits/{}".format(
        self.org_id,
        self.project_id,
        self.ref_id,
        self.commit_id
    )


def _monkey_patch_mms_commit_to_model_compartment(self):
    return iqs_client.ModelCompartment(compartment_uri=self.to_compartment_uri())


def _monkey_patch_model_compartment_get_element_in_compartment_by_id(self, relative_element_id):
    return iqs_client.ElementInCompartmentDescriptor(
        compartment_uri=self.compartment_uri,
        relative_element_id=relative_element_id
    )

def _monkey_patch_element_descriptor_to_str(self):
    return 'element #{} at {}'.format(self.element_id, self.to_descriptor_str())
    
def _monkey_patch_element_descriptor_to_descriptor_str(self):
    import pprint
    return pprint.pformat(self.to_dict())

def _monkey_patch_element_descriptor_repr_html(self):
    import html
    if hasattr(self, 'url'):
        return '<a href="{}" title="{}">element #{}</a>'.format(html.escape(self.url), html.escape(self), html.escape(self.element_id))
    else:
        return '<span title="{}">element #{}</span>'.format(html.escape(self.to_str()), html.escape(self.element_id))

def _monkey_patch_element_descriptor_resolve_reference(self, target_element_id):
    return iqs_client.ElementDescriptor(
        revision_number = self.revision_number,
        branch_id       = self.branch_id,
        resource_id     = self.resource_id,
        workspace_id    = self.workspace_id,
        element_id      = target_element_id
    )
    
def _monkey_patch_element_descriptor_get_containing_revision(self):
    return iqs_client.RevisionDescriptor(
        revision_number = self.revision_number,
        branch_id       = self.branch_id,
        resource_id     = self.resource_id,
        workspace_id    = self.workspace_id
    )
    
def _monkey_patch_revision_descriptor_get_element_descriptor_by_id(self, element_id):
    return iqs_client.ElementDescriptor(
        revision_number = self.revision_number,
        branch_id       = self.branch_id,
        resource_id     = self.resource_id,
        workspace_id    = self.workspace_id,
        element_id      = element_id
    )
    
def _monkey_patch_revision_descriptor_to_compartment_uri(self):
    return "twc-index:/workspaces/{}/resources/{}/branches/{}/revisions/{}".format(
        self.workspace_id, self.resource_id, self.branch_id, self.revision_number
    )


def _monkey_patch_revision_descriptor_to_model_compartment(self):
    return iqs_client.ModelCompartment(compartment_uri=self.to_compartment_uri())

def _monkey_patch_query_execution_response_to_data_frame(self, url_provider=None):
    import pandas as pd
    return pd.DataFrame(self.to_list_of_matches(url_provider))

def _monkey_patch_query_execution_response_to_list_of_matches(self, url_provider=None):
    return [dict((arg.parameter, _dict_to_element(arg.value, url_provider)) for arg in match.arguments) for match in
            self.matches]


def _dict_to_element(dict_or_attribute_value, url_provider=None):
    if isinstance(dict_or_attribute_value, dict):
        if "relativeElementID" in dict_or_attribute_value:
            descriptor = iqs_client.ElementInCompartmentDescriptor(**dict(
                (py_name, dict_or_attribute_value[json_name]) for py_name, json_name in
                iqs_client.ElementInCompartmentDescriptor.attribute_map.items()))
        elif "workspaceId" in dict_or_attribute_value:
            descriptor = iqs_client.ElementDescriptor(**dict(
                (py_name, dict_or_attribute_value[json_name]) for py_name, json_name in
                iqs_client.ElementDescriptor.attribute_map.items()))
        else:
            return dict_or_attribute_value
        if url_provider is not None:
            descriptor.url = url_provider(descriptor)
        return descriptor
    else:
        return dict_or_attribute_value
    
def _monkey_patch_generic_response_message_repr_html_(self):
    import html
    return '<span title="{}">{} <i>(see hover for details)</i></span>'.format(html.escape(self.to_str()), html.escape(self.message))

def _monkey_patch_query_fqn_list_repr_html_(self):
    import html
    ns_list = self.query_fq_ns
    if ns_list:
        list_body = "\n".join([
            "<li>{}</li>".format(html.escape(query_fqn)) for query_fqn in ns_list
        ])
        return '<span title="{}">Listing {} queri(es): <i>(see hover for details)</i></span> <ul>{}</ul>'.format(
            html.escape(self.to_str()), str(len(ns_list)), list_body)
    return '<span title="{}">No queries <i>(see hover for details)</i></span>'.format(html.escape(self.to_str()))

def _cell_to_html(cell):
    import html
    if hasattr(cell, '_repr_html_'):
        return cell._repr_html_()
    elif isinstance(cell, str):
        return html.escape(cell)
    else:
        return str(cell)

def _monkey_patch_query_execution_response_to_html(self):
    import html
    count_report = '<span title="{}">{} match(es) of query {}<i>(see hover for details)</i></span>'.format(
        html.escape(self.to_str()), 
        html.escape(str(self.match_set_size)),
        "with bound parameter(s) '{}' ".format(", ".join([html.escape(binding.parameter) for binding in self.binding])) if self.binding else ""
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

        
iqs_client.ElementDescriptor.to_str = _monkey_patch_element_descriptor_to_str
iqs_client.ElementDescriptor.to_descriptor_str = _monkey_patch_element_descriptor_to_descriptor_str
iqs_client.ElementDescriptor._repr_html_ = _monkey_patch_element_descriptor_repr_html
iqs_client.ElementDescriptor.resolve_reference = _monkey_patch_element_descriptor_resolve_reference
iqs_client.ElementDescriptor.get_containing_revision = _monkey_patch_element_descriptor_get_containing_revision
iqs_client.RevisionDescriptor.get_element_descriptor_by_id = _monkey_patch_revision_descriptor_get_element_descriptor_by_id
iqs_client.RevisionDescriptor.to_compartment_uri = _monkey_patch_revision_descriptor_to_compartment_uri
iqs_client.RevisionDescriptor.to_model_compartment = _monkey_patch_revision_descriptor_to_model_compartment

iqs_client.MMSCommitDescriptor.to_compartment_uri = _monkey_patch_mms_commit_to_compartment_uri
iqs_client.MMSCommitDescriptor.to_model_compartment = _monkey_patch_mms_commit_to_model_compartment

iqs_client.ElementInCompartmentDescriptor._repr_html_ = _monkey_patch_element_in_compartment_descriptor_repr_html
iqs_client.ModelCompartment.get_element_in_compartment_by_id = _monkey_patch_model_compartment_get_element_in_compartment_by_id

iqs_client.QueryExecutionResponse.to_list_of_matches = _monkey_patch_query_execution_response_to_list_of_matches
iqs_client.QueryExecutionResponse.to_data_frame = _monkey_patch_query_execution_response_to_data_frame
iqs_client.QueryExecutionResponse.to_data_frame = _monkey_patch_query_execution_response_to_data_frame
iqs_client.QueryExecutionResponse._repr_html_ = _monkey_patch_query_execution_response_to_html  
iqs_client.IndexMessage._repr_html_ = _monkey_patch_generic_response_message_repr_html_
iqs_client.SimpleMessage._repr_html_ = _monkey_patch_generic_response_message_repr_html_
iqs_client.QueryFQNList._repr_html_ = _monkey_patch_query_fqn_list_repr_html_

## global utility functions

def binding(**kwargs):
    return [
        {"parameter": param_name, "value": param_value} 
        for param_name, param_value in kwargs.items()
    ]


## useful widgets and clients

class IQSConnectorWidget:
    def __init__(
        self,
        defaultValue='127.0.0.1:47700/api',
        fieldLabel='Address:',
        labelText="IQS API Access Point",
        auto_display=True
    ):
        self.address_field=widgets.Text(value=defaultValue, description=fieldLabel)
        self.box=widgets.HBox([widgets.Label(value=labelText), self.address_field])
        if auto_display: self.display()
            
    def display(self):
        display(self.box)
        
    def _repr_html_(self):
        self.display()
        
    def api_client_configuration(self):
        configuration = iqs_client.Configuration()
        configuration.host=self.address_field.value        
        return configuration
    
    def connect(self):
        return IQSClient(self.api_client_configuration())


class TWCRevisionInputWidget:
    def __init__(
        self,
        defaultWorkspace='4d6ce495-1273-452c-a548-36fcd922184e',
        defaultResource= '34cc77c8-d3ef-40a6-9b91-65786117fe67',
        defaultBranch=   'bd03a239-7836-4d4c-9bcb-eba73b001b1e',
        defaultRevision='1',
        auto_display=True
    ):
        self.workspace_widget = widgets.Text(value=defaultWorkspace,   description='ID:')
        self.resource_widget  = widgets.Text(value=defaultResource,    description='ID:')
        self.branch_widget    = widgets.Text(value=defaultBranch,      description='ID:')
        self.revision_widget  = widgets.IntText(value=defaultRevision, description='Number:')
        self.box=widgets.HBox([
            widgets.VBox([widgets.Label(value="Workspace"), widgets.Label(value="Resource"), widgets.Label(value="Branch"), widgets.Label(value="Revision")]),
            widgets.VBox([self.workspace_widget,            self.resource_widget,            self.branch_widget,            self.revision_widget])
        ])
        if auto_display: self.display()
    
    def display(self):
        display(self.box)
        
    def _repr_html_(self):
        self.display()    
        
    def value(self):
        return iqs_client.RevisionDescriptor(
            revision_number = self.revision_widget.value,
            branch_id       = self.branch_widget.value,
            resource_id     = self.resource_widget.value,
            workspace_id    = self.workspace_widget.value
        )


class MMCCommitSelectorWidget:

    def __init__(
            self,
            iqs,
            initial_org=None,
            initial_project=None,
            initial_ref=None,
            initial_commit=None,
            auto_display=True
    ):
        self.iqs = iqs
        self.org_widget = widgets.Dropdown(description='')
        self.project_widget = widgets.Dropdown(description='')
        self.ref_widget = widgets.Dropdown(description='')
        self.commit_widget = widgets.Dropdown(description='')
        self.box = widgets.HBox([
            widgets.VBox([widgets.Label(value="org"), widgets.Label(value="project"), widgets.Label(value="ref"),
                          widgets.Label(value="commit")]),
            widgets.VBox([self.org_widget, self.project_widget, self.ref_widget, self.commit_widget])
        ])
        self.fetch_contents()

        def org_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_project()
            elif (owner.disabled):
                pass
            else:
                label, id = owner.options[new_idx]
                org = self.org_map[id]
                self._setup_project(org.projects)

        def project_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_ref()
            elif (owner.disabled):
                pass
            else:
                label, id = self.project_widget.options[new_idx]
                project = self.project_map[id]
                self._setup_ref(project.refs)

        def ref_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_commit()
            elif (owner.disabled):
                pass
            else:
                label, id = self.ref_widget.options[new_idx]
                ref = self.ref_map[id]
                self._setup_commit(ref.commits)

        self.org_widget.observe(names='index', handler=org_handler)
        self.project_widget.observe(names='index', handler=project_handler)
        self.ref_widget.observe(names='index', handler=ref_handler)

        if initial_org:
            self.org_widget.value = initial_org
            if initial_project:
                self.project_widget.value = initial_project
                if initial_ref:
                    self.ref_widget.value = initial_ref
                    if initial_commit:
                        self.commit_widget.value = initial_commit

        if auto_display: self.display()

    def _reset_project(self):
        self.project_map = None
        self.project_widget.disabled = True
        self.project_widget.options = [('', None)]
        self.project_widget.index = 0

    # self._reset_ref()

    def _reset_ref(self):
        self.ref_map = None
        self.ref_widget.disabled = True
        self.ref_widget.options = [('', None)]
        self.ref_widget.index = 0

    # self._reset_commit()

    def _reset_commit(self):
        self.commit_map = None
        self.commit_widget.disabled = True
        self.commit_widget.options = [('', None)]
        self.commit_widget.index = 0

    def _setup_org(self, org_list):
        import collections
        self.org_map = collections.OrderedDict(
            [(org.org_id, org) for org in org_list])
        self.org_widget.options = [('---- Select org', None)] + [
            (
                "{} (ID: {})".format(org.name, id),
                id
            )
            for id, org in self.org_map.items()
        ]
        self.org_widget.index = 0
        self.org_widget.disabled = False

    # self._reset_project()

    def _setup_project(self, project_list):
        import collections
        self.project_map = collections.OrderedDict([(project.project_id, project) for project in project_list])
        self.project_widget.options = [('---- Select project', None)] + [
            (
                "{} (ID: {})".format(project.name, id),
                id
            )
            for id, project in self.project_map.items()
        ]
        self.project_widget.index = 0
        self.project_widget.disabled = False

    # self._reset_ref()

    def _setup_ref(self, ref_list):
        import collections
        self.ref_map = collections.OrderedDict([(ref.ref_id, ref) for ref in ref_list])
        self.ref_widget.options = [('---- Select ref', None)] + [
            (
                "{} (ID: {})".format(ref.name, id),
                id
            )
            for id, ref in self.ref_map.items()
        ]
        self.ref_widget.index = 0
        self.ref_widget.disabled = False

    # self._reset_commit()

    def _setup_commit(self, commit_list):
        import collections
        self.commit_map = collections.OrderedDict([(commit['commitId'], commit) for commit in commit_list])
        self.commit_widget.options = [('---- Select commit', None)] + [
            (
                "{} (ID: {})".format(commit['name'], id),
                id
            )
            for id, commit in self.commit_map.items()
        ]
        self.commit_widget.index = 0
        self.commit_widget.disabled = False

    def fetch_contents(self):
        repo_info = self.iqs.mms_repository.get_mms_repository_info()
        org_list = repo_info.repository_structure.orgs
        self._setup_org(org_list)

    def display(self):
        display(self.box)

    def _repr_html_(self):
        self.display()

    def value(self):
        if (self.commit_widget.index != 0 and
                self.ref_widget.index != 0 and
                self.project_widget.index != 0 and
                self.org_widget.index != 0
        ):
            return iqs_client.MMSCommitDescriptor(
                name=self.commit_map[self.commit_widget.value]['name'],
                commit_id=self.commit_widget.value,
                ref_id=self.ref_widget.value,
                project_id=self.project_widget.value,
                org_id=self.org_widget.value
            )
        else:
            return None

        
        
class TWCRevisionSelectorWidget:
    
    def __init__(
        self,
        iqs,
        initial_workspace = None,
        initial_resource  = None,
        initial_branch    = None,
        initial_revision  = None,
        auto_display=True
    ):
        self.iqs = iqs
        self.workspace_widget = widgets.Dropdown(description='')
        self.resource_widget  = widgets.Dropdown(description='')
        self.branch_widget    = widgets.Dropdown(description='')
        self.revision_widget  = widgets.Dropdown(description='Number:')
        self.box=widgets.HBox([
            widgets.VBox([widgets.Label(value="Workspace"), widgets.Label(value="Resource"), widgets.Label(value="Branch"), widgets.Label(value="Revision")]),
            widgets.VBox([self.workspace_widget,            self.resource_widget,            self.branch_widget,            self.revision_widget])
        ])
        self.fetch_contents()
        
        def workspace_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_resource()
            elif (owner.disabled):
                pass
            else:
                label, id = owner.options[new_idx]
                workspace = self.workspace_map[id]
                self._setup_resource(workspace.resources)

        def resource_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_branch()
            elif (owner.disabled):
                pass
            else:
                label, id = self.resource_widget.options[new_idx]
                resource = self.resource_map[id]
                self._setup_branch(resource.branches)
                
        def branch_handler(change):
            new_idx = change['new']
            old_idx = change['old']
            owner = change['owner']
            if (new_idx == old_idx):
                pass
            elif (not new_idx):
                self._reset_revision()
            elif (owner.disabled):
                pass
            else:
                label, id = self.branch_widget.options[new_idx]
                branch = self.branch_map[id]
                self._setup_revision(branch.revisions)
                
        self.workspace_widget.observe(names='index', handler = workspace_handler)
        self.resource_widget.observe(names='index', handler = resource_handler)
        self.branch_widget.observe(names='index', handler = branch_handler)
        
        if initial_workspace:
            self.workspace_widget.value = initial_workspace
            if initial_resource:
                self.resource_widget.value = initial_resource
                if initial_branch:
                    self.branch_widget.value = initial_branch
                    if initial_revision:
                        self.revision_widget.value = initial_revision
        
        if auto_display: self.display()
    
    
    
    def _reset_resource(self):
        self.resource_map = None
        self.resource_widget.disabled = True
        self.resource_widget.options=[('', None)]
        self.resource_widget.index=0
        #self._reset_branch()
        
    def _reset_branch(self):
        self.branch_map = None
        self.branch_widget.disabled = True
        self.branch_widget.options=[('', None)]
        self.branch_widget.index=0
        #self._reset_revision()
        
    def _reset_revision(self):
        self.revision_map = None
        self.revision_widget.disabled = True
        self.revision_widget.options=[('', None)]
        self.revision_widget.index=0
        
    def _setup_workspace(self, workspace_list):
        import collections
        self.workspace_map = collections.OrderedDict(
            [(workspace.workspace_id, workspace) for workspace in workspace_list])
        self.workspace_widget.options=[('---- Select workspace', None)] + [
                (
                    "{} (ID: {})".format(workspace.title, id),
                    id
                ) 
                for id,workspace in self.workspace_map.items()
            ]
        self.workspace_widget.index=0
        self.workspace_widget.disabled = False
        #self._reset_resource()
        
    def _setup_resource(self, resource_list):
        import collections
        self.resource_map = collections.OrderedDict([(resource.resource_id, resource) for resource in resource_list])
        self.resource_widget.options=[('---- Select resource', None)] + [
                (
                    "{} (ID: {})".format(resource.title, id),
                    id
                ) 
                for id,resource in self.resource_map.items()
            ]
        self.resource_widget.index=0
        self.resource_widget.disabled = False
        #self._reset_branch()
        
    def _setup_branch(self, branch_list):
        import collections
        self.branch_map = collections.OrderedDict([(branch.branch_id, branch) for branch in branch_list])
        self.branch_widget.options=[('---- Select branch', None)] + [
                (
                    "{} (ID: {})".format(branch.title, id),
                    id
                ) 
                for id,branch in self.branch_map.items()
            ]
        self.branch_widget.index=0
        self.branch_widget.disabled = False
        #self._reset_revision()
        
    def _setup_revision(self, revision_list):
        import collections
        self.revision_map = collections.OrderedDict([ (revision['revisionNumber'], revision) for revision in revision_list ])
        self.revision_widget.options=[('---- Select revision', None)] + [
                (str(number), number)
                for number,revision in self.revision_map.items()
            ]
        self.revision_widget.index=0
        self.revision_widget.disabled = False
        
    def fetch_contents(self):
        repo_info = self.iqs.repository.get_repository_info()
        workspace_list = repo_info.repository_structure.workspaces
        self._setup_workspace(workspace_list)

    def display(self):
        display(self.box)
        
    def _repr_html_(self):
        self.display()    
        
    def value(self):
        if (self.revision_widget.index  != 0 and 
            self.branch_widget.index    != 0 and 
            self.resource_widget.index  != 0 and 
            self.workspace_widget.index != 0 
        ):
            return iqs_client.RevisionDescriptor(
                revision_number = self.revision_widget.value,
                branch_id       = self.branch_widget.value,
                resource_id     = self.resource_widget.value,
                workspace_id    = self.workspace_widget.value
            )
        else: 
            return None

class OSMCConnectorWidget:
    def __init__(
        self,
        default_address='https://twc.demo.iqs.beta.incquerylabs.com:8111/osmc',
        default_user='iqs-demo',
        default_pw='',
        address_label='Address:',
        user_label='User:',
        pw_label='Password:',
        label_text="OSMC API Access Point",
        auto_display=True
    ):
        self.address_widget = widgets.Text    (value=default_address, description=address_label)
        self.user_widget    = widgets.Text    (value=default_user,    description=user_label)
        self.pw_widget      = widgets.Password(value=default_pw,      description=pw_label)
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


class IQSClient:
    def __init__(
        self,
        configuration
    ):
        core_api_client_iqs = iqs_client.ApiClient(configuration)
        
        self.jupyter_tools = IQSJupyterTools(self)
        
        self.impact_analysis = iqs_client.ImpactAnalysisApi(core_api_client_iqs)
        self.in_memory_index = iqs_client.InMemoryIndexApi(core_api_client_iqs)
        self.persistent_index = iqs_client.PersistentIndexApi(core_api_client_iqs)
        self.queries = iqs_client.QueriesApi(core_api_client_iqs)
        self.query_execution = iqs_client.QueryExecutionApi(core_api_client_iqs)
        self.repository = iqs_client.RepositoryApi(core_api_client_iqs)
        self.server_management = iqs_client.ServerManagementApi(core_api_client_iqs)
        self.validation = iqs_client.ValidationApi(core_api_client_iqs)    
        self.integration = iqs_client.IntegrationApi(core_api_client_iqs)
        self.mms_repository = iqs_client.MmsRepositoryApi(core_api_client_iqs)
        self.experimental = iqs_client.ExperimentalApi(core_api_client_iqs)

class IQSJupyterTools:
    def __init__(
        self,
        iqs
    ):
        self.iqs = iqs
    
    def revision_selector_widget(self, **kwargs):
        return TWCRevisionSelectorWidget(iqs=self.iqs, **kwargs)

    def mms_commit_selector_widget(self, **kwargs):
        return MMCCommitSelectorWidget(iqs=self.iqs, **kwargs)

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
        osmc_response = requests.get(req_url, auth=self.auth)
        osmc_response.raise_for_status()
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
        osmc_response = requests.post(req_url, data=req_body, auth=self.auth)
        osmc_response.raise_for_status()
        return osmc_response.json()

    def element_short_string(self, element_descriptor):
        raw_container_content, raw_element_content = self.retrieve(element_descriptor)
        return element_short_string(raw_container_content, raw_element_content)
        
    def show_element_info_widget(self, element_descriptor, **kwargs):
        return ElementInfoWidget(osmc=self, initial_element=element_descriptor, **kwargs)

def element_short_string(raw_container_content, raw_element_content):
    # nsUri = raw_element_content["kerml:nsURI"]
    qualified_type = raw_element_content.get("@type", "(untyped)")#.split(':')
    #meta_package = qualified_type[0]
    #type = qualified_type[1]
    name = raw_element_content.get("kerml:name", None)
    id = raw_element_content.get("kerml:esiID", '<unknown ID>')
    if name:
        return "'{}' ({}) #{}".format(name, qualified_type, id)
    else:
        return "<unnamed> ({}) #{}".format(qualified_type, id)



class ElementInfoWidget:
    def __init__(
        self,
        osmc,
        initial_element,
        attempt_batch_prefetch = True,
        grid_container_layout = widgets.Layout(
            grid_template_columns = "25% 73%", 
            grid_gap="2%"),
        field_box_layout = widgets.Layout(
            overflow_x='auto', 
            justify_content='flex-end'),
        slot_item_layout = widgets.Layout(
            width='auto', 
            flex='0 0 auto'),
        slot_box_layout = widgets.Layout(
            overflow_x='auto',
            #border='solid',
            width='auto',
            height='',
            flex_flow='row',
            display='flex', 
            justify_content='flex-start')
    ):
        self.osmc = osmc
        self.attempt_batch_prefetch = attempt_batch_prefetch
        self.grid_container_layout = grid_container_layout
        self.field_box_layout = field_box_layout
        self.slot_item_layout = slot_item_layout
        self.slot_box_layout = slot_box_layout
        self.accordion = widgets.Accordion()
        self.element_list = []
        self.element_id_to_index = {}
        self.element_id_to_descriptor = {}
        self.initial_element = initial_element
        self.show_element_pane(initial_element)
        
    def _add_element_pane(self, element_descriptor):
        raw_container_content, raw_element_content = self.osmc.retrieve(element_descriptor)
        header = element_short_string(raw_container_content, raw_element_content)
        
        field_values = raw_element_content.get('kerml:esiData', {})
        field_value_pairs = [{'field':field, 'value':value} for field,value in field_values.items() if (value is not None) and not ([]==value)]
        grid_content_boxes = []

        if self.attempt_batch_prefetch:
            self.osmc.retrieve_batch([element_descriptor
                for field,value in field_values.items()
                if (value)
                for element_descriptor in self._value_element_descriptor_list(value)
            ])
        import html
        for field,value in field_values.items():
            if (value is not None) and not ([]==value):
                field_widget = widgets.HTML(value = "<b>{}</b>".format(html.escape(field)))
                field_box = widgets.Box(children=[field_widget], layout=self.field_box_layout)
                slot_widget_list = self._value_widget_list(value)
                slot_box = widgets.Box(children=slot_widget_list, layout=self.slot_box_layout)
                grid_content_boxes.extend([field_box, slot_box])
        content = widgets.GridBox(layout=self.grid_container_layout, children=grid_content_boxes)
        
        self.accordion.children = list(self.accordion.children) + [content]
        self.accordion.set_title(len(self.element_list), header)
        self.element_id_to_index[element_descriptor.element_id] = len(self.element_list)
        self.element_list.append(element_descriptor)

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

    def _value_widget_list(self, value):
        import collections
        if isinstance(value, str):
            return [widgets.Label(value=value, layout=self.slot_item_layout)]#'"{}"'.format(value))
        elif isinstance(value, collections.abc.Sequence): # test string-ness before this
            flat_list_widgets = [ widget
                for item in value 
                for widget in self._value_widget_list(item)
            ]
            return flat_list_widgets
        elif isinstance(value, dict) and '@id' in value:
            referred_element = self._element_descriptor_for_id(value['@id'])
            short_text = self.osmc.element_short_string(referred_element)
            button = widgets.Button(
                description=short_text,
                #disabled=False,
                button_style='info', # 'primary', 'success', 'info', 'warning', 'danger' or ''
                #icon='check',
                tooltip='Click to open pane for element {} found at {}'.format(short_text, referred_element.to_descriptor_str()),
                layout=self.slot_item_layout
            )
            button.on_click(lambda b: self.show_element_pane(referred_element))
            return [button]
        else:
            return [widgets.Label(value=value, layout=self.slot_item_layout)]

    def _element_descriptor_for_id(self, element_id):
        if element_id not in self.element_id_to_descriptor:
            self.element_id_to_descriptor[element_id] = self.initial_element.resolve_reference(element_id)
        return self.element_id_to_descriptor[element_id]

    def show_element_pane(self, element_descriptor, highlight=True):
        if element_descriptor.element_id not in self.element_id_to_index:
            self._add_element_pane(element_descriptor)
        if highlight:
            self.accordion.selected_index = self.element_id_to_index[element_descriptor.element_id]
        
    def selected_element(self):
        if self.accordion.selected_index is None:
            return None
        else:
            return self.element_list[self.accordion.selected_index]

    def _repr_html_(self):
        self.display()    
          
    def display(self):
        display(self.accordion)
