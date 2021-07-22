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

import json
from json import JSONDecodeError

import urllib3

from iqs_client.api_client import ApiClient
from iqs_client.configuration import Configuration


class OicdClient(ApiClient):

    def __init__(self, configuration: Configuration, token_path="/token"):
        super(OicdClient, self).__init__(configuration)
        self.token_path = token_path
        self.username = configuration.username
        configuration.username = None
        self.password = configuration.password
        configuration.password = None
        self._get_or_refresh_token()

    def _get_or_refresh_token(self, force_new=False):
        auth_url = self.configuration.host.replace("/api", "") + self.token_path
        if self.configuration.access_token:
            auth_req = {
                "accessToken": self.configuration.access_token
            }
        else:
            auth_req = {
                "username": self.username,
                "password": self.password,
                "forceNew": force_new
            }
        http = urllib3.PoolManager()
        r = http.request('POST', auth_url, body=json.dumps(auth_req).encode('utf-8'))
        try:
            token = json.loads(r.data.decode('utf-8'))
        except JSONDecodeError as error:
            raise Exception("Response isn't token.", f"{error.msg} For: {error.doc}")

        self.configuration.access_token = token['token']

    def call_api(self, resource_path, method,
                 path_params=None, query_params=None, header_params=None,
                 body=None, post_params=None, files=None,
                 response_type=None, auth_settings=None, async_req=None,
                 _return_http_data_only=None, collection_formats=None,
                 _preload_content=True, _request_timeout=None, _host=None):
        self._get_or_refresh_token()
        return super().call_api(resource_path, method,
                                path_params=path_params, query_params=query_params,
                                header_params=header_params,
                                body=body, post_params=post_params, files=files,
                                response_type=response_type, auth_settings=auth_settings,
                                async_req=async_req,
                                _return_http_data_only=_return_http_data_only,
                                collection_formats=collection_formats,
                                _preload_content=_preload_content,
                                _request_timeout=_request_timeout, _host=_host)
