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
Created on 2019. nov. 26.

@author: Gabor Bergmann
'''

import html

import iqs_client
from iqs_jupyter.helpers import cell_to_html as _cell_to_html
from iqs_jupyter.helpers import dict_to_element as _dict_to_element
from iqs_jupyter.core_extensions import validation_color_scale


def _monkey_patch_analysis_results_repr_html(self: iqs_client.AnalysisResults):
    escaped_id = html.escape(self.configuration.configuration_id)
    header_report = '''
        <h3>Results for model analysis <b>"{}"</b></h3>
        <span title="{}">Analysis configuration id: {} <i>(see hover for details)</i></span>
    '''.format(
        html.escape(self.configuration.configuration_name),
        html.escape(self.to_str()),
        escaped_id
    )

    kpi_rows = "\n".join([
        "<tr><th>{}</th><td>{}</td></tr>".format(
            html.escape(kpi.name),
            html.escape(str(kpi.value))
        )
        for kpi in self.kpi_values
    ])
    kpi_report = '''
        <h4> KPIs</h4>
        <table border="1">
            <thead>
                <tr style="text-align: right;">
                    <th>KPI</th>
                    <th>Value</th>
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
    '''.format(
        kpi_rows
    )

    toc_rows = "\n".join([
        '''
            <li>{} by rule "<b>{}</b>"</li>
        '''.format(
            _marker_count_report(self.analysis_results[result_index]),
            # escaped_id, str(result_index),
            html.escape(self.analysis_results[result_index].configuration_rule.name)
        )
        for result_index in range(len(self.analysis_results))
    ])
    toc_report = '''
        <h4>Individual analysis rules</h4>
        <ul>
            {}
        </ul>
    '''.format(
        toc_rows
    )

    individual_result_tables = "\n".join([
        '''
            <div>
            {}
            </div>
        '''.format(
            self.analysis_results[result_index]._repr_html_("h4")
        )
        for result_index in range(len(self.analysis_results))
    ])

    style = ""
    return '''
        {}
        <div>
        {}
        {}
        {}
        {}
        </div>
    '''.format(header_report, style, kpi_report, toc_report, individual_result_tables)


def _marker_count_report(analysis_result: iqs_client.AnalysisResult) -> str:
    marker_color = validation_color_scale.get(analysis_result.configuration_rule.severity.lower(), None)
    marker_style_string = 'style="background-color:{}; color: bisque;"'.format(marker_color) if marker_color else ""
    return '{} <span {}>{}</span> marker{}'.format(
        str(len(analysis_result.matches)),
        marker_style_string,
        html.escape(analysis_result.configuration_rule.severity),
        "s" if 1 != len(analysis_result.matches) else ""
    )


def _monkey_patch_analysis_result_repr_html(self: iqs_client.AnalysisResult, heading_lvl: str = 'h4',
                                            anchor: str = None):
    anchor_tag = '<a name="{}"/>'.format(anchor) if anchor else ""
    anchor_href = '<a href="#{}">#</a> '.format(anchor) if anchor else ""
    subheader_report = '{}<span title="{}">{} via "{}" <i>(see hover for details)</i></span>'.format(
        anchor_href,
        html.escape(self.to_str()),
        _marker_count_report(self),
        html.escape(self.configuration_rule.query_fqn)
    )
    header_report = '''
        {}
        <{}>Results of rule <b>"{}"</b></{}>
        {}
    '''.format(
        anchor_tag,
        heading_lvl,
        html.escape(self.configuration_rule.name),
        heading_lvl,
        subheader_report
    )
    if not self.matches:
        return header_report

    # we can assume at least one match
    pattern_params = [
        argument_value.parameter
        for argument_value in self.matches[0].matching_elements
    ]

    param_headers = " ".join(["<th>{}</th> ".format(html.escape(param)) for param in pattern_params])
    match_rows = "\n".join([
        "<tr><th>{}</th><td>{}</td>{}</tr>\n".format(row_index, self.matches[row_index].message, " ".join([
            " <td>{}</td>".format(_cell_to_html(_dict_to_element(argument_value.value)))
            for argument_value in self.matches[row_index].matching_elements
        ])) for row_index in range(len(self.matches))
    ])

    style = ""
    return '''
        {}
        <div>
        {}
        <table border="1">
            <thead>
                <tr style="text-align: right;">
                    <th></th>
                    <th>(Message)</th>
                    {}
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
        </div>
    '''.format(header_report, style, param_headers, match_rows)


class ConfigSelector:

    def __init__(
            self,
            iqs: IQSClient,
            initial_config: Union[AnalysisConfigurationIdentifier, str] = defaults.default_auto_display,
            auto_display=defaults.default_auto_display):
        self.dropdown = widgets.Dropdown(description='')
        self.box = widgets.HBox([widgets.Label(value="Configuration"), self.dropdown])
        config_list = iqs.analysis.list_model_analysis_configurations()
        configs = config_list.model_analysis_configuration_identifiers
        options = [("---- Select model analysis configuration", None)]
        for config in configs:
            additional = (f"{config.configuration_name} (ID: {config.configuration_id})", config)
            options.append(additional)
        self.dropdown.options = options
        if initial_config:
            if isinstance(initial_config, str):
                for config in configs:
                    if config.configuration_id == initial_config:
                        self.dropdown.value = config
            elif isinstance(initial_config, AnalysisConfigurationIdentifier):
                self.dropdown.value = initial_config
        if auto_display:
            display(self.box)

    def value(self) -> AnalysisConfigurationIdentifier:
        return self.dropdown.value

    def _repr_html_(self):
        display(self.box)


def _get_analysis_configuration_selector_widget(
        self: ext_point.IQSJupyterTools,
        initial_config: Union[AnalysisConfigurationIdentifier, str] = None,
        auto_display=True):
    return ConfigSelector(self._iqs, initial_config, auto_display)


def _update_configuration(self: AnalysisApi, path: str):
    with open(path, "r") as file:
        conf = json.load(file)
    on_server = self.list_model_analysis_configurations().model_analysis_configuration_identifiers
    for old in on_server:
        if old.configuration_name == conf["name"]:
            self.delete_model_analysis_configuration(analysis_configuration_identifier=old)
    self.register_model_analysis_configuration(analysis_configuration=conf)


def _do_monkey_patching():
    iqs_client.AnalysisResults._repr_html_ = _monkey_patch_analysis_results_repr_html
    iqs_client.AnalysisResult._repr_html_ = _monkey_patch_analysis_result_repr_html
    ext_point.IQSJupyterTools.analysis_configuration_selector_widget = _get_analysis_configuration_selector_widget
    AnalysisApi.update_model_analysis_configuration = _update_configuration


_do_monkey_patching()
