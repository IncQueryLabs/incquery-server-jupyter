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

from typing import Optional
import ipywidgets as widgets
from IPython.display import display

import iqs_client

import iqs_jupyter.config_defaults as defaults
import iqs_jupyter.tool_extension_point as ext_point



class TWCRevisionInputWidget:
    def __init__(
        self,
        initial_workspace = defaults.default_twc_workspace,
        initial_resource  = defaults.default_twc_resource,
        initial_branch    = defaults.default_twc_branch,
        initial_revision  = defaults.default_twc_revision,
        auto_display=True
    ):
        self.workspace_widget = widgets.Text(value=initial_workspace,   description='ID:')
        self.resource_widget  = widgets.Text(value=initial_resource,    description='ID:')
        self.branch_widget    = widgets.Text(value=initial_branch,      description='ID:')
        self.revision_widget  = widgets.IntText(value=initial_revision, description='Number:')
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


class TWCRevisionSelectorWidget:
    
    def __init__(
        self,
        iqs,
        initial_workspace = defaults.default_twc_workspace,
        initial_resource  = defaults.default_twc_resource,
        initial_branch    = defaults.default_twc_branch,
        initial_revision  = defaults.default_twc_revision,
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
                label, _id = owner.options[new_idx]  # @UnusedVariable
                workspace = self.workspace_map[_id]
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
                label, _id = self.resource_widget.options[new_idx]  # @UnusedVariable
                resource = self.resource_map[_id]
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
                label, _id = self.branch_widget.options[new_idx]  # @UnusedVariable
                branch = self.branch_map[_id]
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
                    "{} (ID: {})".format(workspace.title, _id),
                    _id
                ) 
                for _id,workspace in self.workspace_map.items()
            ]
        self.workspace_widget.index=0
        self.workspace_widget.disabled = False
        #self._reset_resource()
        
    def _setup_resource(self, resource_list):
        import collections
        self.resource_map = collections.OrderedDict([(resource.resource_id, resource) for resource in resource_list])
        self.resource_widget.options=[('---- Select resource', None)] + [
                (
                    "{} (ID: {})".format(resource.title, _id),
                    _id
                ) 
                for _id,resource in self.resource_map.items()
            ]
        self.resource_widget.index=0
        self.resource_widget.disabled = False
        #self._reset_branch()
        
    def _setup_branch(self, branch_list):
        import collections
        self.branch_map = collections.OrderedDict([(branch.branch_id, branch) for branch in branch_list])
        self.branch_widget.options=[('---- Select branch', None)] + [
                (
                    "{} (ID: {})".format(branch.title, _id),
                    _id
                ) 
                for _id,branch in self.branch_map.items()
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



# recognizing element descriptors in match results

def _recognize_element_descriptor(dict_of_element : dict) -> Optional[iqs_client.ElementDescriptor]:
    if "workspaceId" in dict_of_element:
        return iqs_client.ElementDescriptor(
            **dict(
                (py_name, dict_of_element[json_name]) 
                for py_name, json_name in iqs_client.ElementDescriptor.attribute_map.items()
            )
        )
    else:
        return None
        
ext_point.element_dict_recognizers.append(_recognize_element_descriptor)


# monkey patch section

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

def _monkey_patch_list_dependencies_response_repr_html(self):
    import html
    return '''
    <div>
        <ul style="list-style: none; padding-left: 0">{}
        </ul>
    </div>
    '''.format("".join(['''
            <li>Dependee MDObject ID: {}<ul style="list-style: none;">{}</ul>
            </li>'''.format(html.escape(dependeeId), "".join(['''
                <li>Workspace: {}<ul style="list-style: none;">{}</ul>
                </li>'''.format(html.escape(workspace.title), "".join(['''
                    <li>Resource: {}<ul style="list-style: none;">{}</ul>
                    </li>'''.format(html.escape(resource.title), "".join(['''
                        <li>Branch: {}<ul style="list-style: none;">{}</ul>
                        </li>'''.format(html.escape(branch.title), "".join(['''
                            <li>#{}
                                <table border="1" width="100%">
                                    <thead>
                                        <tr style="text-align: right;">
                                            <th>Name</th>
                                            <th>ElementId</th>
                                            <th>Reference</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {}
                                    </tbody>
                                </table>
                            </li>'''.format(html.escape(str(revision["revisionNumber"])), "\n".join([
                                "<tr><td><a href='{}'>{}</a></td><td>{}</td><td>{}</td></tr>".format(
                                    html.escape(reference["elements"][0]["osmcLink"]),
                                    html.escape(reference["elements"][0]["name"]),
                                    html.escape(reference["elements"][0]["elementId"]),
                                    html.escape(reference["reference"])
                                ) for reference in revision["references"]
                            ])) for revision in branch.revisions
                        ])) for branch in resource.branches
                    ])) for resource in workspace.resources
                ])) for workspace in dependee.workspaces
            ]) if 0<dependee.result_size else "<li><i>No dependencies found.</i></li>"
            ) for dependeeId, dependee in self.results.items()
        ])
    )

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

def _monkey_patch_jupytertools_twc_revision_selector_widget(self, **kwargs):
    return TWCRevisionSelectorWidget(iqs=self._iqs, **kwargs)

def _do_monkey_patching():
    iqs_client.ElementDescriptor.to_str = _monkey_patch_element_descriptor_to_str
    iqs_client.ElementDescriptor.to_descriptor_str = _monkey_patch_element_descriptor_to_descriptor_str
    iqs_client.ElementDescriptor._repr_html_ = _monkey_patch_element_descriptor_repr_html
    iqs_client.ElementDescriptor.resolve_reference = _monkey_patch_element_descriptor_resolve_reference
    iqs_client.ElementDescriptor.get_containing_revision = _monkey_patch_element_descriptor_get_containing_revision
    iqs_client.RevisionDescriptor.get_element_descriptor_by_id = _monkey_patch_revision_descriptor_get_element_descriptor_by_id
    iqs_client.RevisionDescriptor.to_compartment_uri = _monkey_patch_revision_descriptor_to_compartment_uri
    iqs_client.RevisionDescriptor.to_model_compartment = _monkey_patch_revision_descriptor_to_model_compartment
    iqs_client.ListDependenciesResponse._repr_html_ = _monkey_patch_list_dependencies_response_repr_html
    
    ext_point.IQSJupyterTools.twc_revision_selector_widget = _monkey_patch_jupytertools_twc_revision_selector_widget

_do_monkey_patching()
