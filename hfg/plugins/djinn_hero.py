from abc import ABC

import pyxel
import time
import sys
import os
import numpy
import math
from threading import Thread

from hfg.plugins import Hero, Enemy, plugin
from hfg.base import threaded
from hfg.shapes import *
from hfg.drawing import ReferenceFrame

@plugin
class DjinnHero(Hero):
    def __init__(self, resources_path: str = __file__):
        super().__init__(width=60, height=70, health=80, special=80, name="djinn", title="Djinn", special_color=pyxel.COLOR_LIME)
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
        colors = [
            pyxel.COLOR_NAVY,
            pyxel.COLOR_RED,
            pyxel.COLOR_BLACK,
            pyxel.COLOR_DARKGRAY,
            pyxel.COLOR_WHITE,
            pyxel.COLOR_RED,
            pyxel.COLOR_PINK,
            pyxel.COLOR_ORANGE,
            pyxel.COLOR_CYAN

        ]

        bitmap = [
            [2, 2, 1, 0, 0, 8, 8, 1, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 0, 1, 8, 8, 8, 8, 1, 2, 2, 2, 2, 2, 2],
            [2, 2, 1, 1, 8, 2, 8, 2, 1, 1, 2, 2, 2, 2, 2],
            [2, 1, 0, 1, 8, 8, 8, 8, 1, 0, 1, 2, 2, 2, 2],
            [1, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0, 1, 2, 2, 2],
            [0, 8, 8, 0, 0, 0, 8, 8, 0, 8, 8, 0, 1, 2, 2],
            [0, 8, 8, 8, 8, 8, 8, 0, 0, 0, 8, 0, 1, 2, 2],
            [1, 0, 8, 8, 8, 8, 0, 8, 8, 8, 0, 1, 2, 2, 2],
            [2, 1, 8, 0, 0, 0, 8, 0, 0, 0, 1, 2, 2, 2, 2],
            [2, 2, 1, 1, 0, 0, 8, 8, 8, 0, 0, 1, 2, 2, 2],
            [2, 1, 1, 2, 1, 1, 0, 0, 8, 8, 8, 0, 1, 2, 2],
            [1, 0, 0, 1, 2, 2, 1, 0, 8, 8, 8, 0, 1, 2, 2],
            [0, 1, 0, 0, 1, 2, 2, 1, 8, 8, 8, 0, 1, 2, 2],
            [0, 1, 1, 0, 0, 1, 1, 0, 8, 8, 8, 0, 1, 2, 2],
            [1, 0, 1, 0, 8, 0, 0, 8, 8, 8, 0, 1, 2, 2, 2],
            [1, 1, 1, 1, 0, 0, 8, 8, 8, 0, 1, 2, 2, 2, 2]
        ]

        for y in range(0,64):
            for x in range(0,60):
                self.draw(Point(60 - x, 70 - y, colors[bitmap[math.floor(y/4)][math.floor(x/4)]], self.frame))

        if self.is_blocked:
            self.draw(Line(-6, 5, -6, self.height + 3, pyxel.COLOR_LIME, self.frame))

    def _carpet(self, reference_frame: ReferenceFrame = None):
        if reference_frame is None:
            reference_frame = self.frame
        # carpet
        self.draw((Line(0, 4, 60, 4, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(0, 5, 4, 5, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(0, 4, 4, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(8, 3, 12, 3, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(8, 4, 12, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(16, 5, 20, 5, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(16, 4, 20, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(24, 3, 28, 3, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(24, 4, 28, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(32, 5, 36, 5, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(32, 4, 36, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(40, 3, 44, 3, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(40, 4, 44, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(48, 5, 52, 5, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(48, 4, 52, 4, pyxel.COLOR_BLACK, reference_frame)))
        self.draw((Line(56, 3, 60, 3, pyxel.COLOR_ORANGE, reference_frame)))
        self.draw((Line(56, 4, 60, 4, pyxel.COLOR_BLACK, reference_frame)))

    def cycle_heads(self, direction):
        pass

    def cycle_body(self, direction):
        pass

    def cycle_legs(self, direction):
        pass

    def start_animation(self, enemy):
        self.release()
        time.sleep(1)

        thread = Thread(target=self._sprinkles, args=[False])
        thread.start()

        time.sleep(2.2)

        self._body()
        self._carpet()

        self.release()

    def _sprinkles(self, show_body=True):
        for i in range(20):
            self.draw(Sprinkles(20, pyxel.COLOR_YELLOW, Rectangle(0,0,self.width,self.height,pyxel.COLOR_WHITE, self.frame)))
            self._carpet()
            if show_body:
                self._body()
            self.draw(Text("**Snap**", 100, 75, pyxel.COLOR_PINK, ReferenceFrame(0, 0)))
            time.sleep(0.1)
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
                self._carpet()
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
                self._carpet()

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
                enemy.get_attacked(self, 15)

            ready_attacks.pop(0)

        self._body()
        self._carpet()
        self.release()

    def super(self, enemy: Enemy):
        for i in range(250):
            self._body()
            self._carpet()

            time.sleep(0.01)

            rect = Rectangle(-i, 20, 15, 10, pyxel.COLOR_CYAN, self.frame)

            self.draw(rect)
            self.draw(Sprinkles(30, pyxel.COLOR_YELLOW, rect))
            self.release()

        self.special -= 30
        enemy.get_attacked(enemy, 50)
        self.health += (80-self.health) * 0.5
        self._body()
        self._carpet()
        self.release()

    def block(self, enemy: Enemy):
        self._body()
        self._carpet()
        self.draw(Line(-6, 5, -6, self.height + 3, pyxel.COLOR_LIME, self.frame))
        self.release()
        self.is_blocked = True

    def walk(self, direction, enemy: Enemy):
        for i in range(12):
            time.sleep(0.05)
            self.x += direction

            self._body()

            self.draw(Line(0, 4, 60, 4, pyxel.COLOR_ORANGE, self.frame))
            self.draw((Line(0, 5, 4 - i, 5, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(0, 4, 4 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(8, 3, 12 - i, 3, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(8, 4, 12 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(16, 5, 20 - i, 5, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(16, 4, 20 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(24, 3, 28 - i, 3, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(24, 4, 28 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(32, 5, 36 - i, 5, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(32, 4, 36 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(40, 3, 44 - i, 3, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(40, 4, 44 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(48, 5, 52 - i, 5, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(48, 4, 52 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(56, 3, 60 - i, 3, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(56, 4, 60 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(64, 5, 68 - i, 5, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(64, 4, 68 - i, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(72, 4, 76 - i, 3, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(72, 4, 76 - i, 4, pyxel.COLOR_ORANGE, self.frame)))
            self.draw((Line(-7, 3, 0, 3, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(-7, 4, 0, 4, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Line(-7, 5, 0, 5, pyxel.COLOR_BLACK, self.frame)))
            self.draw((Rectangle(63, 3, 17, 2, pyxel.COLOR_BLACK, self.frame)))

            self.release()

        self._carpet()
        self._body()
        self.release()

    def _win_sprinkles(self):
        fixed_x = self.x
        fixed_y = self.y
        for i in range(40):
            self._body()
            self._carpet(ReferenceFrame(fixed_x, fixed_y))
            self.draw(Sprinkles(30, pyxel.COLOR_PINK, Rectangle(-5,-5,70,80,pyxel.COLOR_WHITE,self.frame)))
            self.release()
            time.sleep(0.1)
        self._carpet()
        self._body()
        self.release()

    def win_animation(self, enemy: Enemy):
        Thread(target=self._win_sprinkles).start()
        self.move_to(enemy, 5)
        for i in range(10):
            time.sleep(0.03)
            self.y += 1

        for i in range(10):
            time.sleep(0.03)
            self.y -= 1

        time.sleep(2)

    def lose_animation(self, enemy: Enemy):
        for i in range(self.height + self.y):
            self._body()
            self._carpet()
            self.draw(Rectangle(0, self.height, self.width, 30, pyxel.COLOR_BLACK, self.frame))
            self.y -= 1
            time.sleep(0.05)
            self.release()

    def get_attacked(self, enemy, damage):
        if not self.is_blocked:
            self.health -= damage

        if self.health < 0:
            self.health = 0
        self.is_blocked = False
        self._body()
        self._carpet()
        self.release()

    def get_pushed(self, enemy, distance):
        self.move_to(enemy, distance)

    def get_kicked(self, enemy, damage, distance):
        self.move_to(enemy, distance)
