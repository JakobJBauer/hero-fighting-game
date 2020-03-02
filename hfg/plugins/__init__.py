import pyxel
import sys

sys.path.append("..")

from uuid import uuid4
from abc import ABC, abstractmethod
from base import ThreadStorage, threaded
from drawing import Drawable, ReferenceFrame


DEFAULT_WIDTH = 30
DEFAULT_HEIGHT = 50
DEFAULT_HEALTH = 100
DEFAULT_SPECIAL = 100
DEFAULT_SPECIAL_COLOR = pyxel.COLOR_YELLOW


def plugin(cls):
    if issubclass(cls, Hero):
        cls._is_hero_plugin = True

    return cls


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

    def __init_subclass__(cls, **kwargs):
        cls.get_attacked = threaded(cls.get_attacked)
        cls.get_pushed = threaded(cls.get_pushed)
        cls.get_kicked = threaded(cls.get_kicked)

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

    def move_to(self, enemy, distance):
        if self.x > enemy.x:
            self.x -= distance
        else:
            self.x += distance

    @abstractmethod
    def get_attacked(self, enemy, damage):
        pass

    @abstractmethod
    def get_pushed(self, enemy, distance):
        pass

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

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.start_animation = threaded(cls.start_animation)
        cls.attack = threaded(cls.attack)
        cls.super = threaded(cls.super)
        cls.block = threaded(cls.block)
        cls.walk = threaded(cls.walk)
        cls.win_animation = threaded(cls.win_animation)
        cls.lose_animation = threaded(cls.lose_animation)

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def selection_preview(self):
        pass

    @abstractmethod
    def select(self):
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
    def start(self):
        pass

    @abstractmethod
    @threaded
    def start_animation(self, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def attack(self, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def super(self, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def block(self, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def walk(self, direction, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def win_animation(self, enemy: Enemy):
        pass

    @abstractmethod
    @threaded
    def lose_animation(self, enemy: Enemy):
        pass


