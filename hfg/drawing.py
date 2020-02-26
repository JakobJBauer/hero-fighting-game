import pyxel
from abc import ABC, abstractmethod


class ReferenceFrame:
    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y


class Displayable(ABC):
    def __init__(self, frame: ReferenceFrame):
        self.frame = frame

    def move_frame(self, x, y):
        self.frame.x = x
        self.frame.y = y

    @staticmethod
    def translate_point(x, y, frame: ReferenceFrame):
        x = x + frame.x
        y = y + frame.y

        return x, pyxel.height - y

    @staticmethod
    def translate_left(x, y, frame: ReferenceFrame):
        return Displayable.translate_point(-x, y, frame)

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def display_left(self):
        pass


class Drawable(Displayable):
    def __init__(self, frame: ReferenceFrame, displayables: list = None):
        super().__init__(frame)

        if displayables is not None:
            for item in displayables:
                item.frame = self.frame

            self.displayables = displayables
        else:
            self.displayables = []

        self.intermediates = []

    def draw(self, displayable):
        displayable.frame = self.frame
        self.intermediates.append(displayable)

    def release(self):
        self.displayables = self.intermediates

    def display(self):
        for displayable in self.displayables:
            displayable.display()

    def display_left(self):
        for displayable in self.displayables:
            displayable.display_left()


class Rotatable(ABC):
    @abstractmethod
    def rotate(self, angle, x, y):
        pass
