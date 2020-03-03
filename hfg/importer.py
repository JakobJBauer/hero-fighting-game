import importlib
import os.path
import sys

from hfg.plugins.test_hero import TestHero
from hfg.plugins.monster_hero import MonsterHero
from hfg.plugins.djinn_hero import DjinnHero

HERO_MODULE_ENDING = "_hero.py"

path = os.path.join(os.path.dirname(__file__), "plugins", "resources")


class Importer:
    def __init__(self, base_path):
        self.base_path = base_path

    def import_heroes(self):
        return [DjinnHero(), TestHero(), TestHero(),TestHero(),MonsterHero(),TestHero(),TestHero(),TestHero(),TestHero()]
