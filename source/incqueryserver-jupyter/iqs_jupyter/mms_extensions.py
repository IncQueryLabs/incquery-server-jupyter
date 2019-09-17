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

import ipywidgets as widgets
from IPython.display import display

import iqs_client

import iqs_jupyter.config_defaults as defaults
import iqs_jupyter.tool_extension_point as ext_point


class MMCCommitSelectorWidget:

    def __init__(
            self,
            iqs,
            initial_org     = defaults.default_mms_org,
            initial_project = defaults.default_mms_project,
            initial_ref     = defaults.default_mms_ref,
            initial_commit  = defaults.default_mms_commit,
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
                label, _id = owner.options[new_idx]  # @UnusedVariable
                org = self.org_map[_id]
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
                label, _id = self.project_widget.options[new_idx]  # @UnusedVariable
                project = self.project_map[_id]
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
                label, _id = self.ref_widget.options[new_idx]  # @UnusedVariable
                ref = self.ref_map[_id]
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
        org_list_sorted = sorted(org_list, key=lambda org: org.name)
        self.org_map = collections.OrderedDict(
            [(org.org_id, org) for org in org_list_sorted])
        self.org_widget.options = [('---- Select org', None)] + [
            (
                "{} (ID: {})".format(org.name, _id),
                _id
            )
            for _id, org in self.org_map.items()
        ]
        self.org_widget.index = 0
        self.org_widget.disabled = False

    # self._reset_project()

    def _setup_project(self, project_list):
        import collections
        project_list_sorted = sorted(project_list, key=lambda project: project.name)
        self.project_map = collections.OrderedDict([(project.project_id, project) for project in project_list_sorted])
        self.project_widget.options = [('---- Select project', None)] + [
            (
                "{} (ID: {})".format(project.name, _id),
                _id
            )
            for _id, project in self.project_map.items()
        ]
        self.project_widget.index = 0
        self.project_widget.disabled = False

    # self._reset_ref()

    def _setup_ref(self, ref_list):
        import collections
        ref_list_sorted = sorted(ref_list, key=lambda ref: ref.name)
        self.ref_map = collections.OrderedDict([(ref.ref_id, ref) for ref in ref_list_sorted])
        self.ref_widget.options = [('---- Select ref', None)] + [
            (
                "{} (ID: {})".format(ref.name, _id),
                _id
            )
            for _id, ref in self.ref_map.items()
        ]
        self.ref_widget.index = 0
        self.ref_widget.disabled = False

    # self._reset_commit()

    def _setup_commit(self, commit_list):
        import collections
        commit_list_sorted = sorted(commit_list, key=lambda commit: commit['name'], reverse=True)
        self.commit_map = collections.OrderedDict([(commit['commitId'], commit) for commit in commit_list_sorted])
        self.commit_widget.options = [('---- Select commit', None)] + [
            (
                "{} (ID: {})".format(commit['name'], _id),
                _id
            )
            for _id, commit in self.commit_map.items()
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
            return iqs_client.MMSCommitDescriptor.from_fields(
                name=self.commit_map[self.commit_widget.value]['name'],
                commit_id=self.commit_widget.value,
                ref_id=self.ref_widget.value,
                project_id=self.project_widget.value,
                org_id=self.org_widget.value
            )
        else:
            return None

    def value_as_model_compartment(self):
        value = self.value()
        if value:
            return value.to_model_compartment()
        else:
            return None

# monkey patch section


def _monkey_patch_static_mms_commit_descriptor_from_compartment_uri_or_none(compartment_uri):
    segments = compartment_uri.split('/')
    if (
        9 != len(segments) or
        segments[0] != "mms-index:" or
        segments[1] != "orgs"       or
        segments[3] != "projects"   or
        segments[5] != "refs"       or
        segments[7] != "commits"    
    ):
        return None
    
    return iqs_client.MMSCommitDescriptor(
        org_id          = segments[2], 
        project_id      = segments[4], 
        ref_id          = segments[6], 
        commit_id       = segments[8],
        compartment_uri = compartment_uri
    )
    
def _monkey_patch_mms_commit_to_compartment_uri(self):
    return "mms-index:/orgs/{}/projects/{}/refs/{}/commits/{}".format(
        self.org_id,
        self.project_id,
        self.ref_id,
        self.commit_id
    )
def _mms_compartment_uri(org_id, project_id, ref_id, commit_id):
    return "mms-index:/orgs/{}/projects/{}/refs/{}/commits/{}".format(
        org_id,
        project_id,
        ref_id,
        commit_id
    )
def _monkey_patch_static_mms_commit_descriptor_from_fields(org_id, project_id, ref_id, commit_id, name = None):
    return iqs_client.MMSCommitDescriptor(
        name=name,
        commit_id=commit_id,
        ref_id=ref_id,
        project_id=project_id,
        org_id=org_id,
        compartment_uri=_mms_compartment_uri(org_id, project_id, ref_id, commit_id)
    )

def _monkey_patch_mms_commit_to_model_compartment(self):
    return iqs_client.ModelCompartment(compartment_uri=self.to_compartment_uri())


def _monkey_patch_jupytertools_mms_commit_selector_widget(self, **kwargs):
    return MMCCommitSelectorWidget(iqs=self._iqs, **kwargs)

def _do_monkey_patching():
    iqs_client.MMSCommitDescriptor.from_compartment_uri_or_none = staticmethod(_monkey_patch_static_mms_commit_descriptor_from_compartment_uri_or_none)
    iqs_client.MMSCommitDescriptor.from_fields = staticmethod(_monkey_patch_static_mms_commit_descriptor_from_fields)
    iqs_client.MMSCommitDescriptor.to_compartment_uri = _monkey_patch_mms_commit_to_compartment_uri
    iqs_client.MMSCommitDescriptor.to_model_compartment = _monkey_patch_mms_commit_to_model_compartment
    
    ext_point.IQSJupyterTools.mms_commit_selector_widget = _monkey_patch_jupytertools_mms_commit_selector_widget

_do_monkey_patching()
