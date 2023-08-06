# Copyright 2019 Genymobile
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Genymotion Cloud SaaS API client
"""

import os
import requests
from requests_toolbelt.utils import dump

import gmsaas

from gmsaas.gmsaas.triggererrors import get_fake_http_instance_state
from gmsaas.storage import authcache
from gmsaas.gmsaas.proxy import get_proxies_from_config
from gmsaas.saas.sioclient import SIOClient
from gmsaas.gmsaas import errors as err
from gmsaas.gmsaas.logger import LOGGER
from gmsaas.model.recipeinfo import Recipes
from gmsaas.model.instanceinfo import Instance, Instances, InstanceState, is_instance_starting, is_instance_stopping
from gmsaas.saas.api import (
    get_login_url,
    get_recipes_url,
    get_start_disposable_url,
    get_stop_disposable_url,
    get_instance_url,
    get_instance_list_url,
)
from gmsaas.gmsaas.timeout import wait_until, get_start_timeout, get_stop_timeout


HTTP_FAKE_INSTANCE_STATE = get_fake_http_instance_state()


def _http_call(method, url, **kwargs):
    """
    Perform HTTP call and log around it
    """
    LOGGER.info("Request: %s %s", method.upper(), url)
    try:
        proxies = get_proxies_from_config()

        response = requests.request(method, url, proxies=proxies, **kwargs)
        if response:
            if LOGGER.verbosity > 1:
                response.request.body = "<hidden>"
                LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
            else:
                LOGGER.info("Response: %s", response.status_code)
        else:
            # In case of error, request and response (including redirects) are logged.
            # Note: request's body is not logged as it can contain critical information.
            response.request.body = "<hidden>"
            LOGGER.info("Response: %s", dump.dump_all(response).decode("utf-8"))
        return response
    except requests.exceptions.ProxyError as exception:
        raise err.ProxyError(exception) from exception
    except requests.exceptions.SSLError as exception:
        raise err.SSLError(exception) from exception
    except requests.RequestException as exception:
        # Possible exceptions http://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        # Despite the fact many causes can trigger exceptions, error message is oriented for ConnectionError.
        raise err.RequestError(exception) from exception


class Client:
    """
    Genymotion Cloud SaaS HTTP API client
    """

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.jwt = None

    @staticmethod
    def _get_user_agent():
        """
        Craft User Agent HTTP header
        """

        user_agent_data = ["Genymobile", gmsaas.__application__, gmsaas.__version__]
        extra_data = os.environ.get("GMSAAS_USER_AGENT_EXTRA_DATA")
        if extra_data:
            user_agent_data.append(extra_data)
        return " ".join(user_agent_data)

    def _get_authorization(self):
        """
        Craft Authorization HTTP header for user
        """
        token = self._get_jwt()
        return "Bearer {}".format(token)

    def _get_headers(self, authorization_needed=True):
        """
        Craft HTTP headers for request
        """
        headers = {"user-agent": self._get_user_agent()}

        if authorization_needed:
            headers["Authorization"] = self._get_authorization()

        return headers

    def _make_session_api_call(self, api_call):
        response = api_call()
        if response.status_code == 401 or os.environ.get("GMSAAS_FORCE_JWT_REFRESH"):
            self._fetch_jwt()
            return api_call()
        return response

    def _get_paginated_results(self, url, ordering, page_size):
        """
        Perform HTTP calls on paginated endpoint, until all elements are fetched.
        Return results array.
        """
        count = None
        current_page = 1
        results = []

        while count is None or len(results) < count:
            params = {"page_size": page_size, "page": current_page, "ordering": ordering}
            response = self._make_session_api_call(
                lambda: _http_call("get", url, headers=self._get_headers(), params=params)
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                    count = data["count"]
                    if not data["results"]:
                        # If results array is empty, early break here and so
                        # ignore the count property to avoid any infinite loop.
                        break
                    results.extend(data["results"])
                    current_page += 1
                except Exception as exception:
                    raise err.InvalidJsonError(response.status_code, response.text) from exception
            else:
                raise err.ApiError(response.status_code, response.text)

        return results

    def list_recipes(self):
        """
        List available Recipes for user, return Recipes object
        """
        LOGGER.debug("Listing available Recipes")
        response = self._make_session_api_call(
            lambda: _http_call("get", get_recipes_url(), headers=self._get_headers())
        )

        if response.status_code == 200:
            try:
                return Recipes.create_from_saas(response.json())
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_instance(self, instance_uuid):
        """
        Return Instance from SaaS API
        """
        LOGGER.debug("Get instance")
        response = self._make_session_api_call(
            lambda: _http_call("get", get_instance_url(instance_uuid), headers=self._get_headers())
        )
        if response.status_code == 200:
            try:
                data = response.json()
                return Instance.create_from_saas(data)
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def get_instances(self):
        """
        Return Instances from SaaS API
        """
        LOGGER.debug("Listing Instances")
        results = self._get_paginated_results(get_instance_list_url(), ordering="+created_at", page_size=50)
        return Instances.create_from_saas(results)

    def _get_jwt(self):
        """
        Get JWT for user
        """
        self.jwt = authcache.get_jwt()
        if not self.jwt:
            self._fetch_jwt()
        return self.jwt

    def _fetch_jwt(self):
        LOGGER.info("Requesting new JWT")
        payload = {"email": self.email, "password": self.password}
        response = _http_call("post", get_login_url(), json=payload, headers=self._get_headers(False))
        if response.status_code == 200:
            try:
                self.jwt = response.json()["token"]
                authcache.set_jwt(self.jwt)
            except Exception as exception:
                raise err.AuthenticationError(response.status_code, response.text) from exception
        else:
            raise err.AuthenticationError(response.status_code, response.text)

    def _request_instance_state(self, instance_uuid):
        """
        Return instance state via HTTP API
        """
        LOGGER.info("[%s] Request instance details", instance_uuid)

        if HTTP_FAKE_INSTANCE_STATE:
            LOGGER.info("Using fake instance state %s", HTTP_FAKE_INSTANCE_STATE)
            return HTTP_FAKE_INSTANCE_STATE

        url = get_instance_url(instance_uuid)
        response = self._make_session_api_call(lambda: _http_call("get", url, json={}, headers=self._get_headers()))

        if response.status_code == 200:
            try:
                return response.json()["state"]
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        elif response.status_code == 404:
            LOGGER.info("[%s] Instance not found, considering it as DELETED", instance_uuid)
            return InstanceState.DELETED
        raise err.ApiError(response.status_code, response.text)

    def _wait_for_instance_stopped(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s stopped (HTTP fallback)", instance_uuid)
        wait_until(
            lambda: not is_instance_stopping(self._request_instance_state(instance_uuid)), get_stop_timeout(), period=3
        )
        return self._request_instance_state(instance_uuid)

    def _wait_for_instance_started(self, instance_uuid):
        """
        Return the actual state whether it succeeds or not, the caller needs to check it.
        """
        LOGGER.debug("Waiting for %s started (HTTP fallback)", instance_uuid)
        wait_until(
            lambda: not is_instance_starting(self._request_instance_state(instance_uuid)), get_start_timeout(), period=3
        )
        return self._request_instance_state(instance_uuid)

    def login(self):
        """
        Perform a login request
        """
        return self._get_jwt()

    def _start_api_call(self, recipe_uuid, instance_name, stop_when_inactive):
        """
        Start instance with API, returns dict response on success
        """
        payload = {"instance_name": instance_name, "stop_when_inactive": stop_when_inactive}
        url = get_start_disposable_url(recipe_uuid)

        response = self._make_session_api_call(
            lambda: _http_call("post", url, json=payload, headers=self._get_headers())
        )
        if response.status_code == 201:
            try:
                return response.json()
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def start_disposable_instance(self, recipe_uuid, instance_name, stop_when_inactive, no_wait):
        """
        Start a new disposable instance, return Instance object
        """
        LOGGER.debug('Starting new "%s" disposable Instance', instance_name)

        instance = Instance.create_from_saas(self._start_api_call(recipe_uuid, instance_name, stop_when_inactive))
        if no_wait:
            return instance

        with SIOClient(jwt=self._get_jwt()) as sio:
            if not sio.exception:
                instance.state = sio.wait_for_instance_started(instance.uuid)
            else:
                LOGGER.warning(
                    "[%s] SIO client unreachable (%s), fallback to HTTP polling", instance.uuid, str(sio.exception)
                )
                instance.state = self._wait_for_instance_started(instance.uuid)

        if is_instance_starting(instance.state):
            # Perform an HTTP call to be sure in case Socket.IO server got down,
            # or missed to push one message.
            LOGGER.info("[%s] Instance not started yet, perform HTTP request to confirm", instance.uuid)
            instance.state = self._request_instance_state(instance.uuid)

        if instance.state != InstanceState.ONLINE:
            LOGGER.error("[%s] Instance not started", instance.uuid)
            raise err.InstanceError(instance.uuid, InstanceState.ONLINE, instance.state)

        LOGGER.info("[%s] Instance started", instance.uuid)
        return instance

    def _stop_api_call(self, instance_uuid):
        """
        Stop instance with API returns dict response on success
        """
        url = get_stop_disposable_url(instance_uuid)
        response = self._make_session_api_call(lambda: _http_call("post", url, json={}, headers=self._get_headers()))

        if response.status_code == 200:
            try:
                return response.json()
            except Exception as exception:
                raise err.InvalidJsonError(response.status_code, response.text) from exception
        else:
            raise err.ApiError(response.status_code, response.text)

    def stop_disposable_instance(self, instance_uuid, no_wait):
        """
        Stop a running disposable Instance, return Instance object
        """
        LOGGER.debug("[%s] Stopping disposable Instance", instance_uuid)

        instance = Instance.create_from_saas(self._stop_api_call(instance_uuid))
        if no_wait:
            return instance

        with SIOClient(jwt=self._get_jwt()) as sio:
            if not sio.exception:
                instance.state = sio.wait_for_instance_stopped(instance_uuid)
            else:
                LOGGER.warning(
                    "[%s] SIO client unreachable (%s), fallback to HTTP polling", instance.uuid, str(sio.exception)
                )
                instance.state = self._wait_for_instance_stopped(instance_uuid)

        if is_instance_stopping(instance.state):
            # Perform an HTTP call to be sure in case Socket.IO server got down,
            # or missed to push one message.
            LOGGER.info("[%s] Instance not stopped yet, perform HTTP request to confirm", instance_uuid)
            instance.state = self._request_instance_state(instance_uuid)

        if instance.state != InstanceState.DELETED:
            LOGGER.error("[%s] Instance not stopped", instance_uuid)
            raise err.InstanceError(instance_uuid, InstanceState.DELETED, instance.state)

        LOGGER.info("[%s] Instance stopped", instance_uuid)
        return instance
