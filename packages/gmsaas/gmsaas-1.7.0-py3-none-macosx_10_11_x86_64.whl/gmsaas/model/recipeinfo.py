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
Recipe data
"""
from distutils.version import LooseVersion
from collections import OrderedDict

from tabulate import tabulate


RECIPES_TABLE_HEADERS = ["UUID", "NAME", "ANDROID", "SCREEN", "SOURCE"]
NONE_PLACEHOLDER = "Unknown"


def _key_for_entry(entry):
    source = entry.source
    version = entry.android_version
    name = entry.name

    if version == NONE_PLACEHOLDER:
        version = "0.0.0"
    version = LooseVersion(version)

    return (source, version, name)


class Recipe:
    """ Class representing one Recipe
    """

    def __init__(self, uuid=None):
        self.uuid = uuid
        self.name = None
        self.android_version = None
        self.screen_width = None
        self.screen_height = None
        self.screen_density = None
        self.source = None

    def as_dict(self):
        """ Return Recipe as dict object
        Using OrderedDict here because dict() preserves insertion order since Python 3.7 only
        """
        data = OrderedDict()
        data["uuid"] = self.uuid or ""
        data["name"] = self.name or ""
        data["android_version"] = self.android_version or NONE_PLACEHOLDER
        data["screen_width"] = self.screen_width or 0
        data["screen_height"] = self.screen_height or 0
        data["screen_density"] = self.screen_density or 0
        data["screen"] = self.screen or NONE_PLACEHOLDER
        data["source"] = self.source or NONE_PLACEHOLDER
        return data

    @property
    def screen(self):
        """ Return string representation of screen properties """
        if all([self.screen_width, self.screen_height, self.screen_density]):
            return "{} x {} dpi {}".format(self.screen_width, self.screen_height, self.screen_density)
        return NONE_PLACEHOLDER

    @staticmethod
    def create_from_saas(raw_recipe):
        """ Factory function to get Recipe object from SaaS API content """

        def _get_item_data(raw_recipe, item):
            """
            Retrieve the data of the given item, return empty dict if not found
            """
            for i in raw_recipe["items"]:
                if i["type"] == item:
                    return i["data"]
            return {}

        recipe = Recipe()
        if not raw_recipe:
            # Recipe might be None depending on the state of the instance.
            # For example when the instance is almost stopped. Need investigation
            # on the SaaS API side to fix this inconsistency.
            return recipe

        recipe.uuid = raw_recipe["uuid"]
        recipe.name = raw_recipe["name"]
        recipe.android_version = _get_item_data(raw_recipe, "ova").get("android_version", NONE_PLACEHOLDER)
        screen_data = _get_item_data(raw_recipe, "screen")
        recipe.screen_width = screen_data.get("width")
        recipe.screen_height = screen_data.get("height")
        recipe.screen_density = screen_data.get("density")
        recipe.source = raw_recipe["source"]
        return recipe


class Recipes:
    """ Class storing a list of Recipe """

    def __init__(self):
        self.recipes = []

    def __len__(self):
        return len(self.recipes)

    def __iter__(self):
        return iter(self.recipes)

    def as_list(self):
        """ Return list of dict structured Recipe """
        self.sort()
        return [r.as_dict() for r in self.recipes]

    @staticmethod
    def create_from_saas(raw_recipes):
        """ Factory function to get Recipes object from SaaS API content """
        raw_recipes = raw_recipes["base"] + raw_recipes["user"] + raw_recipes["shared"]
        recipes = Recipes()
        for raw_recipe in raw_recipes:
            recipes.recipes.append(Recipe.create_from_saas(raw_recipe))
        return recipes

    def filter_by_name(self, name):
        """ Filter recipes in place by name """
        self.recipes = [r for r in self.recipes if name.strip().casefold() in r.name.casefold()]

    def sort(self):
        """ Sort recipes in place
        Recipes are sorted by several criteria which are (by priority ASC):
        NAME, ANDROID, SOURCE
        """
        self.recipes = sorted(self.recipes, key=_key_for_entry)

    def tabulate(self):
        """ Return a tabulated string representation of recipes """
        self.sort()
        recipes_table = self._get_table_format()
        return tabulate(recipes_table, headers=RECIPES_TABLE_HEADERS, numalign="left")

    def _get_table_format(self):
        """
        Return recipes as a two dimension table structure
        """
        formated_recipes = [[r.uuid, r.name, r.android_version, r.screen, r.source] for r in self.recipes]
        return formated_recipes
