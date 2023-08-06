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
Cli for subcommand instance
"""

import click

from gmsaas.model.instanceinfo import Instance, Instances, InstanceState, TunnelState
from gmsaas.gmsaas import errors as err
from gmsaas.cli.checks import credentials_required, adb_tools_required
from gmsaas.saas import get_client
from gmsaas.storage import authcache
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.gmsaas.logger import LOGGER
from gmsaas.cli.clioutput import ui


@click.group("instances")
def instances_cmd_group():
    """
    Manage your Genymotion Cloud SaaS instances
    """


@click.command("start")
@click.argument("RECIPE_UUID", type=click.UUID)
@click.argument("INSTANCE_NAME")
@click.option(
    "--stop-when-inactive",
    type=click.BOOL,
    is_flag=True,
    help="Automatically stop the instance after long inactivity period",
)
@click.option("--no-wait", type=click.BOOL, is_flag=True, help="Do not wait for the instance to be fully started")
@click.pass_context
@credentials_required
def start_disposable_instance(ctx, recipe_uuid, instance_name, stop_when_inactive, no_wait):
    """
    Start a disposable instance from a recipe
    """
    del ctx
    saas = _get_api_client()

    instance = saas.start_disposable_instance(recipe_uuid, instance_name, bool(stop_when_inactive), no_wait)
    ui().instances_start(instance)


@click.command("stop")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.option("--no-wait", type=click.BOOL, is_flag=True, help="Do not wait for the instance to be fully stopped")
@click.pass_context
@credentials_required
@adb_tools_required
def stop_disposable_instance(ctx, instance_uuid, no_wait):
    """
    Stop a running disposable instance
    """
    del ctx
    instance_uuid = str(instance_uuid)
    adbtunnel = get_adbtunnel()
    adbtunnel.disconnect(instance_uuid)
    tunnel_state = adbtunnel.wait_for_adb_disconnected(instance_uuid).tunnel_state
    if tunnel_state != TunnelState.DISCONNECTED:
        LOGGER.error("[%s] Instance can't be disconnected from ADB tunnel", instance_uuid)
    saas = _get_api_client()
    instance = saas.stop_disposable_instance(instance_uuid, no_wait)
    ui().instances_stop(instance)


@click.command("get")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@credentials_required
@adb_tools_required
def get_instance(ctx, instance_uuid):
    """
    Get instance information
    """
    del ctx
    instance_uuid = str(instance_uuid)
    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    ui().instances_get(instance)


@click.command("list")
@click.option("--quiet", "-q", is_flag=True, help="Only display running instance UUIDs")
@click.pass_context
@credentials_required
@adb_tools_required
def list_instances(ctx, quiet):
    """
    List all currently running instances
    """
    del ctx
    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instances = saas.get_instances()
    adbtunnel_instances = adbtunnel.get_instances()
    instances = Instances.merge(saas_instances, adbtunnel_instances)

    LOGGER.debug("%d Instances available", len(instances))
    ui().instances_list(instances, quiet)


@click.command("adbconnect")
@click.option("--adb-serial-port", type=click.IntRange(1024, 65535))
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@credentials_required
@adb_tools_required
def connect_instance_to_adb(ctx, instance_uuid, adb_serial_port):
    """
    Connect a running instance to ADB
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    if instance.state != InstanceState.ONLINE:
        # Instance should be started in order to connect ADB
        raise err.AdbTunnelInstanceNotReadyError(instance_uuid, instance.state)

    running_port = instance.adb_serial_port
    if running_port:
        # ADB Tunnel is already running for this instance
        # If it's on the same port: early return
        # Else raise an error
        if running_port == adb_serial_port or not adb_serial_port:
            LOGGER.info("[%s] Instance already connected to ADB tunnel", instance_uuid)
            ui().instances_adbconnect(instance)
            return
        raise err.AdbTunnelRunningOnDifferentPortError(instance_uuid, running_port, adb_serial_port)

    adbtunnel.connect(instance_uuid, adb_serial_port)
    adbtunnel_instance = adbtunnel.wait_for_adb_connected(instance_uuid)
    instance = Instance.merge(instance, adbtunnel_instance)

    if instance.tunnel_state == TunnelState.CONNECTED:
        LOGGER.info("[%s] Instance connected to ADB tunnel", instance_uuid)
        ui().instances_adbconnect(instance)
        return
    if instance.tunnel_state == TunnelState.PORT_BUSY:
        raise err.AdbTunnelBusyPortError(instance_uuid, adb_serial_port)
    raise err.AdbTunnelGenericError(instance_uuid)


@click.command("adbdisconnect")
@click.argument("INSTANCE_UUID", type=click.UUID)
@click.pass_context
@credentials_required
@adb_tools_required
def disconnect_instance_from_adb(ctx, instance_uuid):
    """
    Disconnect a running instance from ADB
    """
    del ctx
    instance_uuid = str(instance_uuid)

    saas = _get_api_client()
    adbtunnel = get_adbtunnel()
    saas_instance = saas.get_instance(instance_uuid)
    adbtunnel_instance = adbtunnel.get_instance(instance_uuid)
    instance = Instance.merge(saas_instance, adbtunnel_instance)

    adbtunnel.disconnect(instance_uuid)
    adbtunnel_instance = adbtunnel.wait_for_adb_disconnected(instance_uuid)
    instance = Instance.merge(instance, adbtunnel_instance)

    if instance.tunnel_state == TunnelState.DISCONNECTED:
        LOGGER.info("[%s] Instance disconnected from ADB tunnel", instance_uuid)
        ui().instances_adbdisconnect(instance)
        return
    raise err.AdbTunnelGenericError(instance_uuid)


def _get_api_client():
    """
    Get the Genymotion Cloud SaaS API client
    """
    return get_client(authcache.get_email(), authcache.get_password())


instances_cmd_group.add_command(start_disposable_instance)
instances_cmd_group.add_command(stop_disposable_instance)
instances_cmd_group.add_command(get_instance)
instances_cmd_group.add_command(list_instances)
instances_cmd_group.add_command(connect_instance_to_adb)
instances_cmd_group.add_command(disconnect_instance_from_adb)
