# Copyright 2021 IncQuery Labs Ltd.
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
from IPython.display import display
from iqs_client import ApiClient

import iqs_jupyter.config_defaults as defaults
import iqs_jupyter.tool_extension_point as ext_point
from iqs_jupyter import api_composition
from iqs_client_extension import ApiClientWithOIDC


def connect(
        address=defaults.default_IQS_address,
        user=defaults.default_IQS_username,
        password=defaults.default_IQS_password,
        token=defaults.default_IQS_token,
        auth_with_user_pw=defaults.default_use_password,
        use_oidc=defaults.default_use_oidc
):
    configuration = iqs_client.Configuration()
    configuration.host = address
    configuration.access_token = None
    if auth_with_user_pw:
        configuration.username = user
        configuration.password = password
    else:
        configuration.access_token = token
    return IQSClient(configuration, use_oidc)


class IQSClient:
    def __init__(
            self,
            root_configuration,
            use_oicd
    ):
        if use_oicd:
            api_composition.decorate_iqs_client(self, root_configuration, ApiClientWithOIDC)
        else:
            api_composition.decorate_iqs_client(self, root_configuration, ApiClient)
        self.jupyter_tools = ext_point.IQSJupyterTools(self)


class IQSConnectorWidget:
    def __init__(
            self,
            ask_for_user_pw=defaults.default_use_password,
            initial_address=defaults.default_IQS_address,
            initial_user=defaults.default_IQS_username,
            initial_password=defaults.default_IQS_password,
            use_oidc=defaults.default_use_oidc,
            token=defaults.default_IQS_token,
            address_label='Address:',
            user_label='User:',
            oicd_checkbox_label='Use OpenID Connect',
            password_label='Password:',
            label_text="IQS API Access Point",
            login_button=True,
            auto_display=defaults.default_auto_display
    ):
        self.ask_for_user_pw = ask_for_user_pw
        self.token = token

        self.address_field = widgets.Text(value=initial_address, description=address_label)
        self.user_field = widgets.Text(value=initial_user, description=user_label)
        self.password_field = widgets.Password(value=initial_password, description=password_label)
        self.oicd_checkbox = widgets.Checkbox(value=use_oidc, description=oicd_checkbox_label)

        self.iqs_client = None

        if ask_for_user_pw:
            fields = [self.address_field, self.user_field, self.password_field, self.oicd_checkbox]
        else:
            fields = [self.address_field]

        btn_connect = widgets.Button(
            description="Test Connection",
            disabled=False
        )
        connection_label = widgets.Label("")

        def test_connection(_):
            try:
                self.iqs_client = self.connect()
                server_status = self.iqs_client.server_management.get_server_status_with_http_info()

                if server_status[1] == 200:
                    if server_status[0].component_statuses["SERVER"] == "UP":
                        connection_label.value = "Connected! IQS is ready to use."
                else:
                    raise Exception("Error during operation.",
                                    "{}: {}".format(server_status.status_code, server_status.reason))

            except Exception as error:
                connection_label.value = f"Connection failed: {error}"

        btn_connect.on_click(test_connection)

        if login_button:
            fields.append(btn_connect)
            fields.append(connection_label)

        self.box = widgets.HBox([widgets.Label(value=label_text), widgets.VBox(fields)])
        if auto_display:
            self.display()

    def display(self):
        display(tuple([self.box]))

    def _repr_html_(self):
        self.display()

    def api_client_configuration(self):
        configuration = iqs_client.Configuration()
        configuration.host = self.address_field.value
        if self.ask_for_user_pw:
            configuration.username = self.user_field.value
            configuration.password = self.password_field.value
        return configuration

    def connect(self):
        return connect(
            address=self.address_field.value,
            user=self.user_field.value,
            password=self.password_field.value,
            token=self.token,
            auth_with_user_pw=self.ask_for_user_pw,
            use_oidc=self.oicd_checkbox.value
        )
