# Copyright 2020 Genymobile
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
gmsaas output controls
"""
from abc import ABC, abstractmethod
import json
from collections import OrderedDict

import click

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.gmsaas.errors import ExitCode
from gmsaas.storage.configcache import get_output_format
from gmsaas.model.instanceinfo import Instances

TEXT_OUTPUT = "text"
JSON_OUTPUT = "json"
COMPACT_JSON_OUTPUT = "compactjson"
OUTPUT_FORMATS = [TEXT_OUTPUT, JSON_OUTPUT, COMPACT_JSON_OUTPUT]


def ui():  # pylint: disable=invalid-name
    """ Factory function returning the right Out instance
    """
    output_format = OutputFormat.get()
    LOGGER.info("Using `%s` output format", output_format)
    if output_format == JSON_OUTPUT:
        return JSONOut()
    if output_format == COMPACT_JSON_OUTPUT:
        return CompactJSONOut()
    return PlainTextOut()


class OutputFormat:
    """ Static class able to get the output format to use
    """

    from_option = None

    @staticmethod
    def get():
        """ Return the output format to use:
        * return format set with `--format` option if set
        * otherwise return format from configuration if set
        * else return the default format
        """
        output_format = OutputFormat.from_option
        if not output_format:
            output_format = get_output_format()
        if not output_format:
            output_format = TEXT_OUTPUT

        if output_format not in OUTPUT_FORMATS:
            LOGGER.warning("`%s` output format not supported, ignoring", output_format)
            return TEXT_OUTPUT

        return output_format


class Out(ABC):
    """ Abstract class inherited by each output format supported
    """

    def write_stdout(self, message, loggable=False):
        """ Write message in stdout and log it if wanted """
        # pylint: disable=no-self-use
        if loggable:
            LOGGER.info(message)
        click.echo(message)

    def write_stderr(self, message, extra_log=None):
        """ Write message in stderr, log it, also log `extra_log` if set """
        # pylint: disable=no-self-use
        LOGGER.error(message)
        if extra_log:
            LOGGER.error(extra_log)
        click.echo(message, err=True)

    @abstractmethod
    def error(self, exit_code, message, hint, details):
        """ Output for any error raised by gmsaas """

    @abstractmethod
    def show_version(self, name, version, doc_url, pypi_url):
        """ Output for `gmsaas --version` """

    @abstractmethod
    def auth_login(self, email, auth_cache_path):
        """ Output for `gmsaas auth login` """

    @abstractmethod
    def auth_logout(self):
        """ Output for `gmsaas auth logout` """

    @abstractmethod
    def auth_whoami(self, email, auth_cache_path):
        """ Output for `gmsaas auth whoami` """

    @abstractmethod
    def config_set(self, key, value):
        """ Output for `gmsaas config set` """

    @abstractmethod
    def config_get(self, key, value):
        """ Output for `gmsaas config get` """

    @abstractmethod
    def config_list(self, configuration):
        """ Output for `gmsaas config list` """

    @abstractmethod
    def instances_adbconnect(self, instance):
        """ Output for `gmsaas instances adbconnect` """

    @abstractmethod
    def instances_adbdisconnect(self, instance):
        """ Output for `gmsaas instances adbdisconnect` """

    @abstractmethod
    def instances_get(self, instance):
        """ Output for `gmsaas instances get` """

    @abstractmethod
    def instances_list(self, instances, quiet):
        """ Output for `gmsaas instances list` """

    @abstractmethod
    def instances_start(self, instance):
        """ Output for `gmsaas instances start` """

    @abstractmethod
    def instances_stop(self, instance):
        """ Output for `gmsaas instances stop` """

    @abstractmethod
    def logzip(self, archive_path):
        """ Output for `gmsaas logzip` """

    @abstractmethod
    def recipes_list(self, recipes):
        """ Output for `gmsaas recipes list` """


class PlainTextOut(Out):
    """ Subclass for text format output implementation
    """

    def error(self, exit_code, message, hint, details):
        """ Output for any error raised by gmsaas
        Note: `hint` is appended to message if it exists
        """
        output = message
        if hint:
            output += "\n" + hint
        self.write_stderr(output, details)

    def show_version(self, name, version, doc_url, pypi_url):
        """ Output for `gmsaas --version` """
        self.write_stdout("{} version {}\nDocumentation: {}\nChangelog: {}".format(name, version, doc_url, pypi_url))

    def auth_login(self, email, auth_cache_path):
        """ Output for `gmsaas auth login` """
        self.write_stdout(
            "User {} is logged in.\n" "Credentials saved to file: [{}]".format(email, auth_cache_path), loggable=True
        )

    def auth_logout(self):
        """ Output for `gmsaas auth logout` """
        self.write_stdout("Logged out.", loggable=True)

    def auth_whoami(self, email, auth_cache_path):
        """ Output for `gmsaas auth whoami` """
        if email:
            self.write_stdout(email)
            return
        self.write_stdout("No credentials found. To set them up, use 'gmsaas auth login' command.")

    def config_set(self, key, value):
        """ Output for `gmsaas config set` """
        if not value:
            self.write_stdout("'{}' has been unset.".format(key))
            return
        self.write_stdout("'{}' has been set to '{}'.".format(key, value))

    def config_get(self, key, value):
        """ Output for `gmsaas config get` """
        self.write_stdout(value)

    def config_list(self, configuration):
        """ Output for `gmsaas config list` """
        items = sorted(["{}={}".format(key, configuration[key]) for key in configuration])
        self.write_stdout("\n".join(items))

    def instances_adbconnect(self, instance):
        """ Output for `gmsaas instances adbconnect` """
        self.write_stdout(instance.adb_serial)

    def instances_adbdisconnect(self, instance):
        """ Output for `gmsaas instances adbdisconnect` """

    def instances_get(self, instance):
        """ Output for `gmsaas instances get` """
        instances = Instances()
        instances.instances = [instance]
        self.instances_list(instances, False)

    def instances_list(self, instances, quiet):
        """ Output for `gmsaas instances list` """
        output = instances.tabulate(quiet)
        if output:
            self.write_stdout(output)

    def instances_start(self, instance):
        """ Output for `gmsaas instances start` """
        self.write_stdout(instance.uuid)

    def instances_stop(self, instance):
        """ Output for `gmsaas instances stop` """

    def logzip(self, archive_path):
        """ Output for `gmsaas logzip` """
        self.write_stdout("'{}' generated.".format(archive_path))

    def recipes_list(self, recipes):
        """ Output for `gmsaas recipes list` """
        self.write_stdout(recipes.tabulate())


class JSONOut(Out):
    """ Subclass for JSON format output implementation
    """

    def __init__(self, indent=4):
        self.indent = indent

    def write_data_stdout(self, data):
        """ Add exit OK to data and print it as JSON """
        assert isinstance(data, OrderedDict), "write_data_stderr only accepts OrderedDict"
        data["exit_code"] = ExitCode.NO_ERROR.value
        data["exit_code_desc"] = ExitCode.NO_ERROR.name
        self.write_stdout(json.dumps(data, indent=self.indent, sort_keys=False))

    def write_data_stderr(self, data, exit_code):
        """ Add exit code to data and print it as JSON """
        assert isinstance(data, OrderedDict), "write_data_stderr only accepts OrderedDict"
        data["exit_code"] = exit_code
        data["exit_code_desc"] = ExitCode(exit_code).name
        self.write_stderr(json.dumps(data, indent=self.indent, sort_keys=False))

    def error(self, exit_code, message, hint, details):
        """ Output for any error raised by gmsaas
        Note: `hint` is not used in JSON output
        """
        data = OrderedDict()
        data["error"] = OrderedDict([("message", message), ("details", details or "")])
        self.write_data_stderr(data, exit_code)

    def show_version(self, name, version, doc_url, pypi_url):
        """ Output for `gmsaas --version` """
        data = OrderedDict()
        data["name"] = name
        data["version"] = version
        data["documentation_url"] = doc_url
        data["changelog_url"] = pypi_url
        self.write_data_stdout(data)

    def auth_login(self, email, auth_cache_path):
        """ Output for `gmsaas auth login` """
        data = OrderedDict()
        data["auth"] = OrderedDict([("email", email), ("credentials_path", auth_cache_path)])
        self.write_data_stdout(data)

    def auth_logout(self):
        """ Output for `gmsaas auth logout` """
        self.write_data_stdout(OrderedDict())

    def auth_whoami(self, email, auth_cache_path):
        """ Output for `gmsaas auth whoami` """
        self.auth_login(email, auth_cache_path)

    def config_set(self, key, value):
        """ Output for `gmsaas config set` """
        self.config_list({key: value})

    def config_get(self, key, value):
        """ Output for `gmsaas config get` """
        self.config_list({key: value})

    def config_list(self, configuration):
        """ Output for `gmsaas config list` """
        # configuration is {key: value} dict that need to be sorted
        data = OrderedDict(sorted(configuration.items(), key=lambda x: x[0]))
        self.write_data_stdout(OrderedDict([("configuration", data)]))

    def instances_adbconnect(self, instance):
        """ Output for `gmsaas instances adbconnect` """
        self.instances_start(instance)

    def instances_adbdisconnect(self, instance):
        """ Output for `gmsaas instances adbdisconnect` """
        self.instances_start(instance)

    def instances_get(self, instance):
        """ Output for `gmsaas instances get` """
        self.instances_start(instance)

    def instances_list(self, instances, quiet):
        """ Output for `gmsaas instances list` """
        self.write_data_stdout(OrderedDict([("instances", instances.as_list())]))

    def instances_start(self, instance):
        """ Output for `gmsaas instances start` """
        self.write_data_stdout(OrderedDict([("instance", instance.as_dict())]))

    def instances_stop(self, instance):
        """ Output for `gmsaas instances stop` """
        self.instances_start(instance)

    def logzip(self, archive_path):
        """ Output for `gmsaas logzip` """
        self.write_data_stdout(OrderedDict([("archive_path", archive_path)]))

    def recipes_list(self, recipes):
        """ Output for `gmsaas recipes list` """
        self.write_data_stdout(OrderedDict([("recipes", recipes.as_list())]))


class CompactJSONOut(JSONOut):
    """ Subclass for compact JSON output implementation
    """

    def __init__(self):
        super().__init__(indent=None)
