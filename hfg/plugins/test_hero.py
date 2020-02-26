import pyxel
import time

from hfg.base import threaded
from hfg.plugins import Hero, Enemy
from hfg.shapes import Rectangle


class TestHero(Hero):
    def __init__(self):
        super().__init__(10, 20)

    def selection_preview(self):
        self.draw(Rectangle(0, 0, 10, 20, pyxel.COLOR_GREEN, self.frame))
        self.release()

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    @threaded
    def start_animation(self):
        for i in range(100):
            time.sleep(1)
            self.move_frame(self.x + 1, self.y)

    @threaded
    def attack(self, enemy: Enemy):
        pass

    @threaded
    def super(self, enemy: Enemy):
        pass

    @threaded
    def block(self, enemy: Enemy):
        pass

    @threaded
    def walk(self, direction, enemy: Enemy):
        pass

    @threaded
    def win_animation(self):
        pass

    @threaded
    def lose_animation(self):
        pass

    @threaded
    def get_attacked(self, enemy, damage):
        pass

    @threaded
    def get_pushed(self, enemy, distance):
        pass

    @threaded
    def get_kicked(self, enemy, damage, distance):
        pass
