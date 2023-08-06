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
Cli for subcommand recipes
"""
import click

from gmsaas.cli.checks import credentials_required
from gmsaas.saas import get_client
from gmsaas.storage import authcache

from gmsaas.gmsaas.logger import LOGGER
from gmsaas.cli.clioutput import ui


@click.group("recipes")
def recipes_cmd_group():
    """
    View your Genymotion Cloud SaaS recipes
    """


@click.command("list")
@click.option("--name", help="Filter results with substring")
@click.pass_context
@credentials_required
def list_recipes(ctx, name):
    """
    List all available recipes
    """
    del ctx
    saas = get_client(authcache.get_email(), authcache.get_password())
    recipes = saas.list_recipes()

    LOGGER.debug("%d Recipes available", len(recipes))

    if name:
        recipes.filter_by_name(name)

    ui().recipes_list(recipes)


recipes_cmd_group.add_command(list_recipes)
