import pyxel
import time
import sys

sys.path.append("..")

from plugins import Hero, Enemy, plugin
from base import threaded
from shapes import *


@plugin
class DjinnHero(Hero):
    def __init__(self):
        super().__init__(width=60, height=70, name="djinn", title="Djinn", special_color=pyxel.COLOR_LIME)
        self.is_blocked = False
        # self.rect = Rectangle(0, 0, self.width, self.height, pyxel.COLOR_GREEN, self.frame)
        #  self.sprinkles = Sprinkles(100, pyxel.COLOR_BROWN, self.rect)

    def _body(self):
        self.draw(self.rect)
        self.draw(self.sprinkles)
        self.draw(Rectangle(10, 45, 15, 20, pyxel.COLOR_WHITE, self.frame))
        self.draw(Rectangle(35, 45, 15, 20, pyxel.COLOR_WHITE, self.frame))
        self.draw(Rectangle(12, 47, 5, 5, pyxel.COLOR_BLACK, self.frame))
        self.draw(Rectangle(38, 52, 5, 5, pyxel.COLOR_BLACK, self.frame))
        self.draw(Rectangle(10, 10, self.width - 20, 30, pyxel.COLOR_BLACK, self.frame))
        self.draw(Rectangle(12, 10, self.width - 20 - 4, 4, pyxel.COLOR_RED, self.frame))

    def selection_preview(self):
        self._body()
        self.release()

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    def start_animation(self, enemy):
        self.move_to(enemy, 20)
        for i in range(25):
            time.sleep(0.03)
            self.y += 1

        for i in range(25):
            time.sleep(0.03)
            self.y -= 1

    def attack(self, enemy: Enemy):
        if abs(enemy.x - self.x) < 20:
            enemy.get_attacked(self, 30)

    def super(self, enemy: Enemy):
        for i in range(100):
            self._body()

            time.sleep(0.01)

            rect = Rectangle(-i, 20, 15, 10, pyxel.COLOR_CYAN, self.frame)

            self.draw(rect)
            self.draw(Sprinkles(30, pyxel.COLOR_YELLOW, rect))
            self.release()

        self.special -= 20
        enemy.get_attacked(enemy, 50)
        self._body()
        self.release()

    def block(self, enemy: Enemy):
        self.is_blocked = True

    def walk(self, direction, enemy: Enemy):
        for i in range(8):
            time.sleep(0.03)

            if i == 0:
                self.y += 3

            self.x += direction

        self.y -= 3

    def win_animation(self, enemy: Enemy):
        self.move_to(enemy, 5)
        for i in range(10):
            time.sleep(0.03)
            self.y += 1

        for i in range(10):
            time.sleep(0.03)
            self.y -= 1

        time.sleep(2)

    def lose_animation(self, enemy: Enemy):
        for i in range(500):
            time.sleep(0.01)
            self.y -= 1

    def get_attacked(self, enemy, damage):
        if not self.is_blocked:
            self.health -= damage
        self.is_blocked = False

    def get_pushed(self, enemy, distance):
        self.move_to(enemy, distance)

    def get_kicked(self, enemy, damage, distance):
        self.move_to(enemy, distance)

