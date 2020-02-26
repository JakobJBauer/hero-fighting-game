import pyxel

from uuid import uuid4
from abc import ABC, abstractmethod
from hfg.base import ThreadStorage, threaded
from hfg.drawing import Drawable, ReferenceFrame


DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 50
DEFAULT_HEALTH = 100
DEFAULT_SPECIAL = 100
DEFAULT_SPECIAL_COLOR = pyxel.COLOR_YELLOW


class Enemy(Drawable, ThreadStorage, ABC):
    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                 health: int = DEFAULT_HEALTH, special: int = DEFAULT_SPECIAL, special_color=DEFAULT_SPECIAL_COLOR,
                 displayables: list = None, meta: dict = None):
        Drawable.__init__(self, ReferenceFrame(), displayables)
        ThreadStorage.__init__(self)

        self.id = uuid4()

        self.width = width
        self.height = height

        self.health = health
        self.special = special
        self.special_color = special_color

        if meta is not None:
            self.meta = meta
        else:
            self.meta = {}

    @property
    def x(self):
        return self.frame.x

    @x.setter
    def x(self, value):
        self.frame.x = value

    @property
    def y(self):
        return self.frame.y

    @y.setter
    def y(self, value):
        self.frame.y = value

    @threaded
    @abstractmethod
    def get_attacked(self, enemy, damage):
        pass

    @threaded
    @abstractmethod
    def get_pushed(self, enemy, distance):
        pass

    @threaded
    @abstractmethod
    def get_kicked(self, enemy, damage, distance):
        pass


class Hero(Enemy, ABC):
    def __init__(self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT,
                 health: int = DEFAULT_HEALTH, special: int = DEFAULT_SPECIAL, special_color=DEFAULT_SPECIAL_COLOR,
                 super_name: str = "Super", name: str = "<hero>", title: str = "Some Hero",
                 displayables: list = None, meta: dict = None):
        super().__init__(width, height, health, special, special_color, displayables, meta)

        self.super_name = super_name

        self.name = name
        self.title = title

    @abstractmethod
    def selection_preview(self):
        pass

    @abstractmethod
    def cycle_heads(self, direction):
        pass

    @abstractmethod
    def cycle_body(self, direction):
        pass

    @abstractmethod
    def cycle_legs(self, direction):
        pass

    @abstractmethod
    @threaded
    def start_animation(self):
        pass

    @threaded
    @abstractmethod
    def attack(self, enemy: Enemy):
        pass

    @threaded
    @abstractmethod
    def super(self, enemy: Enemy):
        pass

    @threaded
    @abstractmethod
    def block(self, enemy: Enemy):
        pass

    @threaded
    @abstractmethod
    def walk(self, direction, enemy: Enemy):
        pass

    @threaded
    @abstractmethod
    def win_animation(self):
        pass

    @threaded
    @abstractmethod
    def lose_animation(self):
        pass


