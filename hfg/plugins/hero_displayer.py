import sys
import pyxel
import importlib

from hfg.plugins import Enemy, Hero


arguments = sys.argv
hero_module = arguments[1]


class TestEnemy(Enemy):
    def get_attacked(self, enemy, damage):
        pass

    def get_pushed(self, enemy, distance):
        pass

    def get_kicked(self, enemy, damage, distance):
        pass


class App:
    def __init__(self, hero: Hero):
        pyxel.init(256, 128, fps=60)

        pyxel.mouse(True)

        self.hero = hero

        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.hero.get("start_animation"):
            self.hero.selection_preview()
            self.hero.store("start_animation", self.hero.start_animation())

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.hero.display()


module = importlib.import_module(hero_module)

imported_hero = None

for item in module.__dict__.keys():
    if item.startswith("Test"):
        imported_hero = getattr(module, item)()
        break

App(imported_hero)
