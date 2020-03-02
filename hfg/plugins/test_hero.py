import pyxel
import time
import random
import sys

from base import threaded
from plugins import Hero, Enemy, plugin
from shapes import Rectangle


@plugin
class TestHero(Hero):
    def __init__(self, resources_path: str = None):
        super().__init__()

        self.resources_path = resources_path
        self.color = random.randint(1, 10)

    def selection_preview(self):
        self.draw(Rectangle(0, 0, self.width, self.height, self.color, self.frame))
        self.release()

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    def start_animation(self, enemy):
        for i in range(5):
            time.sleep(0.05)
            self.move_frame(self.x + 1, self.y)

    def attack(self, enemy: Enemy):
        self.health = 0

    def super(self, enemy: Enemy):
        pass

    def block(self, enemy: Enemy):
        pass

    def walk(self, direction, enemy: Enemy):
        self.x += 5 * direction

    def win_animation(self, enemy):
        pass

    def lose_animation(self, enemy):
        pass

    def get_attacked(self, enemy, damage):
        pass

    def get_pushed(self, enemy, distance):
        pass

    def get_kicked(self, enemy, damage, distance):
        pass

    def move_frame(self, x, y):
        super().move_frame(x, y)

    def display(self):
        super().display()
