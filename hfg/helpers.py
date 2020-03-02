import math
import sys

from hfg.base import threaded
from hfg.plugins import Hero, Enemy
from hfg.shapes import Line


class HeroBar(Line):
    def __init__(self, value, total, length, distance, color, hero):
        x1 = 0
        y1 = hero.height + distance

        x2 = math.floor((value / total) * length)
        y2 = y1

        super().__init__(x1, y1, x2, y2, color, hero.frame)

    def rotate(self, angle, x, y):
        raise NotImplementedError


class FillerHero(Hero):
    def __init__(self):
        super().__init__(title="")

    def selection_preview(self):
        pass

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    @threaded
    def start_animation(self):
        pass

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
