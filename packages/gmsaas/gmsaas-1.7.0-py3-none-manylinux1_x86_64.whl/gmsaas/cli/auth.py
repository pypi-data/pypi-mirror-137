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
Cli for subcommand auth
"""

import click

from gmsaas.saas import get_client
from gmsaas.storage import authcache
from gmsaas.adbtunnel import get_adbtunnel
from gmsaas.cli.clioutput import ui


def _logout():
    adbtunnel = get_adbtunnel()
    if adbtunnel.is_ready():
        adbtunnel.stop()
    authcache.clear()


@click.group()
def auth():
    """
    Manage your Genymotion Cloud SaaS credentials
    """


@click.command(
    "login",
    short_help="Allows you to input your Genymotion Cloud SaaS credentials, ensure their validity, and store them",
)
@click.argument("email")
@click.argument("password", required=False)
def auth_login(email, password):
    """
    Allows you to input your Genymotion Cloud SaaS credentials, ensure their validity, and store them
    """
    # Note: `short_help` makes help text not being truncated to 45 char, don't remove it.
    if not password:
        password = click.prompt("Password", type=click.STRING, hide_input=True)

    _logout()

    client = get_client(email, password)
    jwt = client.login()

    authcache.set_email(email)
    authcache.set_password(password)
    authcache.set_jwt(jwt)

    ui().auth_login(email, authcache.get_path())


@click.command("whoami")
def auth_whoami():
    """
    Display credentials currently in use
    """
    ui().auth_whoami(authcache.get_email(), authcache.get_path())


@click.command("logout")
def auth_logout():
    """
    Remove stored credentials and clean up
    """
    _logout()
    ui().auth_logout()


auth.add_command(auth_login)
auth.add_command(auth_whoami)
auth.add_command(auth_logout)
