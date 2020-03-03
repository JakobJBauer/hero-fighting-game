from abc import ABC

import pyxel
import time
import sys
import os
import numpy

sys.path.append("..")

from plugins import Hero, Enemy, plugin
from base import threaded
from shapes import *

@plugin
class DjinnHero(Hero):
    def __init__(self, resources_path: str = __file__):
        super().__init__(width=60, height=70, name="djinn", title="Djinn", special_color=pyxel.COLOR_LIME)
        self.is_blocked = False
        # self.rect = Rectangle(0, 0, self.width, self.height, pyxel.COLOR_GREEN, self.frame)
        #  self.sprinkles = Sprinkles(100, pyxel.COLOR_BROWN, self.rect)

    def selection_preview(self):

        # region Bitmap
        colors = [
            pyxel.COLOR_NAVY,
            pyxel.COLOR_RED,
            pyxel.COLOR_BLACK,
            pyxel.COLOR_DARKGRAY,
            pyxel.COLOR_WHITE,
            pyxel.COLOR_RED,
            pyxel.COLOR_PINK,
            pyxel.COLOR_ORANGE
        ]
        bitmap = [
            [3, 3, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 7, 2, 1, 1, 1, 1, 2, 1, 1],
            [3, 3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 2, 1],
            [3, 3, 3, 3, 3, 3, 3, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 2, 1, 1, 2, 0, 0, 2, 1],
            [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 2, 0, 2, 1],
            [3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 2, 0, 2, 1],
            [1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0,
             0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0,
             0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 1, 1, 1, 3],
            [1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0,
             0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 1, 3, 3, 3],
            [1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 2, 0, 0, 2, 0, 0, 2, 1, 3, 3, 3, 1],
            [1, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 1, 1, 3, 3, 3, 3, 3, 3, 2, 4, 2, 0, 0, 0, 0, 2, 4, 4, 2, 0, 0, 0, 0, 0, 0,
             0, 2, 0, 0, 0, 2, 0, 0, 2, 1, 1, 3, 1, 1],
            [1, 1, 1, 3, 3, 1, 1, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 2, 4, 4, 2, 0, 0, 0, 2, 4, 4, 4, 4, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 2, 1, 3, 1, 1, 1],
            [1, 1, 1, 3, 3, 1, 1, 3, 1, 1, 3, 3, 1, 1, 1, 3, 3, 3, 2, 4, 4, 4, 2, 0, 2, 4, 4, 4, 4, 4, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 0, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 3, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 2, 4, 4, 4, 2, 0, 2, 4, 4, 4, 4, 4, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 2, 1, 1, 1, 1, 1, 3],
            [1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 2, 4, 4, 4, 2, 0, 2, 4, 4, 4, 4, 4, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 2, 3, 1, 1, 3, 3, 3],
            [3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 2, 4, 4, 2, 2, 0, 2, 4, 4, 2, 4, 4, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 2, 0, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4, 4, 2, 2, 0, 2, 4, 4, 2, 4, 2, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 2, 0, 2, 3, 3, 3, 3, 3, 3],
            [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 4, 4, 4, 2, 0, 2, 4, 4, 4, 2, 2, 2, 2, 2, 0, 0, 0,
             0, 0, 0, 0, 2, 0, 0, 2, 1, 3, 3, 3, 3, 1],
            [3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 2, 0, 0, 0, 0, 0, 2, 4, 2, 0, 0, 0, 2, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 2, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2,
             2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 4, 2, 2,
             0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 3, 3, 1, 1, 3, 3, 1, 1, 1, 2, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 2, 0, 2,
             0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 3],
            [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 3, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 2, 0, 2,
             0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 3, 3],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 2,
             0, 0, 2, 0, 0, 0, 0, 2, 1, 1, 1, 3, 3, 3],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 2, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 4, 4, 4, 2, 2, 0, 2,
             2, 0, 2, 2, 0, 0, 2, 1, 1, 1, 3, 3, 3, 1],
            [1, 1, 3, 3, 1, 1, 1, 3, 3, 1, 3, 2, 2, 0, 0, 0, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 4, 4, 4, 2, 2, 5, 2, 0, 2,
             2, 0, 2, 0, 2, 2, 2, 1, 1, 3, 3, 3, 1, 1],
            [1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 0, 2,
             2, 0, 2, 0, 0, 0, 2, 2, 1, 3, 3, 1, 1, 1],
            [3, 3, 1, 1, 1, 3, 1, 1, 1, 2, 0, 0, 2, 0, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 6, 6, 6, 2, 0, 2,
             2, 0, 0, 2, 0, 0, 0, 2, 3, 3, 1, 1, 1, 1],
            [3, 3, 1, 3, 1, 3, 1, 1, 2, 0, 0, 0, 0, 2, 4, 4, 4, 2, 2, 5, 5, 5, 5, 5, 5, 2, 6, 6, 2, 6, 6, 6, 2, 2, 0, 2,
             2, 2, 0, 2, 0, 0, 0, 2, 3, 3, 1, 3, 3, 1],
            [3, 3, 1, 1, 3, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 2, 2, 2, 5, 5, 2, 6, 6, 6, 6, 6, 2, 2, 4, 2, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 2, 2, 3, 3, 1, 1, 1],
            [1, 3, 3, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 2, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1],
            [1, 3, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 0, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 2, 1, 1, 1, 3, 3],
            [1, 1, 3, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 0, 0, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 2, 1, 1, 3, 3, 3],
            [1, 1, 1, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 0, 2, 3, 3, 3, 1],
            [1, 1, 1, 3, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 0, 2, 3, 3, 3, 1],
            [3, 1, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             2, 2, 0, 2, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3],
            [3, 3, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
             2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 3],
            [1, 3, 3, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
             2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1],
            [1, 1, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2,
             2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1],
            [1, 2, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2,
             0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],
            [2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2,
             0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0,
             0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0,
             2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 2,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 2, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 2, 0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 2, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        # endregion

        for y in range(0,50):
            for x in range(0,50):
                self.draw(Point(55 - x, 60 - y, colors[bitmap[y][x]], self.frame))

        self.release()

        self.select()

    def select(self):
        pass

    def _body(self):
        self.draw(Circle(37, 60, 7, pyxel.COLOR_NAVY, self.frame))
        self.draw(Circle(35, 58, 6, pyxel.COLOR_NAVY, self.frame))
        self.draw(Circle(34, 51, 9, pyxel.COLOR_NAVY, self.frame))
        self.draw(Rectangle(18, 45, 30, 5, pyxel.COLOR_NAVY, self.frame))

        # carpet
        self.draw((Line(0, 4, 60, 4, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(0, 5, 4, 5, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(0, 4, 4, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(8, 3, 12, 3, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(8, 4, 12, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(16, 5, 20, 5, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(16, 4, 20, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(24, 3, 28, 3, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(24, 4, 28, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(32, 5, 36, 5, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(32, 4, 36, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(40, 3, 44, 3, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(40, 4, 44, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(48, 5, 52, 5, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(48, 4, 52, 4, pyxel.COLOR_BLACK, self.frame)))
        self.draw((Line(56, 3, 60, 3, pyxel.COLOR_ORANGE, self.frame)))
        self.draw((Line(56, 4, 60, 4, pyxel.COLOR_BLACK, self.frame)))

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    def start_animation(self, enemy):
        self._body()

        self.release()

    def attack(self, enemy: Enemy):
        xy: list = list()
        attacks = numpy.random.randint(2, 5)
        ready_attacks = []

        for i in range(attacks):
            xy.append((numpy.random.randint(- 4, 1), numpy.random.randint(self.y, self.height)))

        for x, y in xy:
            current_y = 0
            while current_y < y:
                self._body()
                self.draw(CircleBorder(x, current_y + 3, 1, pyxel.COLOR_LIME, self.frame))
                self.draw(Line(x, current_y + 2, x, current_y, pyxel.COLOR_LIME, self.frame))
                self.draw(Line(x - 1, current_y, x + 1, current_y, pyxel.COLOR_LIME, self.frame))
                self.draw((Point(x - 2, current_y - 2, pyxel.COLOR_ORANGE, self.frame)))
                self.draw((Point(x - 1, current_y - 3, pyxel.COLOR_ORANGE, self.frame)))
                self.draw((Point(x, current_y - 2, pyxel.COLOR_ORANGE, self.frame)))
                self.draw((Point(x + 1, current_y - 3, pyxel.COLOR_ORANGE, self.frame)))
                self.draw((Point(x + 2, current_y - 2, pyxel.COLOR_ORANGE, self.frame)))

                for ready_attack in ready_attacks:
                    for shape in ready_attack:
                        if shape[0] == "CircleBorder":
                            self.draw(CircleBorder(shape[1], shape[2], shape[3], shape[4], shape[5]))
                        elif shape[0] == "Line":
                            self.draw((Line(shape[1], shape[2], shape[3], shape[4], shape[5], shape[6])))
                        elif shape[0] == "Point":
                            self.draw(Point(shape[1], shape[2], shape[3], shape[4]))
                        else:
                            raise ValueError(f"'shape[0]' is incorrect")

                self.release()
                time.sleep(0.02)
                current_y += 1

            ready_attacks.append([
                ["CircleBorder", x, current_y + 3, 1, pyxel.COLOR_LIME, self.frame],
                ["Line", x, current_y + 2, x, current_y, pyxel.COLOR_LIME, self.frame],
                ["Line", x - 1, current_y, x + 1, current_y, pyxel.COLOR_LIME, self.frame],
                ["Point", x - 2, current_y - 2, pyxel.COLOR_ORANGE, self.frame],
                ["Point", x - 1, current_y - 3, pyxel.COLOR_ORANGE, self.frame],
                ["Point", x, current_y - 2, pyxel.COLOR_ORANGE, self.frame],
                ["Point", x + 1, current_y - 3, pyxel.COLOR_ORANGE, self.frame],
                ["Point", x + 2, current_y - 2, pyxel.COLOR_ORANGE, self.frame]
            ])

        for i in range(len(ready_attacks)):
            x = 0
            while (enemy.x + x) - self.x > -(enemy.width/2) or (self.x + x) - enemy.x > -(enemy.width/2):
                x -= 1
                self._body()

                for shape in ready_attacks[0]:
                    if shape[0] == "CircleBorder":
                        shape[1] -= 1
                    elif shape[0] == "Line":
                        shape[1] -= 1
                        shape[3] -= 1
                    elif shape[0] == "Point":
                        shape[1] -= 1
                    else:
                        raise ValueError(f"'shape[0]' is incorrect")

                for ready_attack_2 in ready_attacks:
                    for shape in ready_attack_2:
                        if shape[0] == "CircleBorder":
                            self.draw(CircleBorder(shape[1], shape[2], shape[3], shape[4], shape[5]))
                        elif shape[0] == "Line":
                            self.draw((Line(shape[1], shape[2], shape[3], shape[4], shape[5], shape[6])))
                        elif shape[0] == "Point":
                            self.draw(Point(shape[1], shape[2], shape[3], shape[4]))
                        else:
                            raise ValueError(f"'shape[0]' is incorrect")

                time.sleep(0.02)
                self.release()

            if (ready_attacks[0][2][2] > enemy.y) and (ready_attacks[0][2][2] < enemy.y + enemy.height):
                enemy.get_attacked(self, 30)

            ready_attacks.pop(0)

        self._body()
        self.release()

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

        if self.health < 0:
            self.health = 0
        self.is_blocked = False

    def get_pushed(self, enemy, distance):
        self.move_to(enemy, distance)

    def get_kicked(self, enemy, damage, distance):
        self.move_to(enemy, distance)
