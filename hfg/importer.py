import importlib
import os.path
import sys

sys.path.append("..")

from plugins.test_hero import TestHero
from plugins.monster_hero import MonsterHero
from plugins.djinn_hero import DjinnHero

HERO_MODULE_ENDING = "_hero.py"

path = os.path.join(os.path.dirname(__file__), "plugins", "resources")


class Importer:
    def __init__(self, base_path):
        self.base_path = base_path

    def import_heroes(self):
        return [DjinnHero(path),TestHero(), TestHero(),TestHero(),MonsterHero(),TestHero(),TestHero(),TestHero(),TestHero()]
