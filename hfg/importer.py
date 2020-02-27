import importlib
import os.path

from hfg.plugins.test_hero import TestHero
from hfg.plugins.monster_hero import MonsterHero

HERO_MODULE_ENDING = "_hero.py"


class Importer:
    def __init__(self, base_path):
        self.base_path = base_path

    def import_heroes(self):
        return [TestHero(), TestHero(),TestHero(),MonsterHero(),TestHero(),TestHero(),TestHero(),TestHero()]
