import pyxel
import random
import sys

sys.path.append("..")
from drawing import Displayable, Rotatable


class Point(Displayable):
    def __init__(self, x, y, color, frame):
        super().__init__(frame)

        self.x = x
        self.y = y

        self.color = color

    def rotate(self, angle, x, y):
        raise NotImplementedError

    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.pset(x, y, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.pset(x, y, self.color)


class Line(Displayable, Rotatable):
    def __init__(self, x1, y1, x2, y2, color, frame):
        super().__init__(frame)

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.color = color

    def rotate(self, angle, x, y):
        raise NotImplementedError

    def display(self):
        x1, y1 = self.translate_point(self.x1, self.y1, self.frame)
        x2, y2 = self.translate_point(self.x2, self.y2, self.frame)

        pyxel.line(x1, y1, x2, y2, self.color)

    def display_left(self):
        x1, y1 = self.translate_left(self.x1, self.y1, self.frame)
        x2, y2 = self.translate_left(self.x2, self.y2, self.frame)

        pyxel.line(x1, y1, x2, y2, self.color)


class Rectangle(Displayable):
    def __init__(self, x, y, width, height, color, frame):
        super().__init__(frame)

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.color = color

    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.rect(x, y - self.height, self.width, self.height, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.rect(x - self.width, y - self.height, self.width, self.height, self.color)


class RectangleBorder(Rectangle):
    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.rectb(x, y - self.height, self.width, self.height, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.rectb(x, y - self.height, self.width, self.height, self.color)


class Circle(Displayable):
    def __init__(self, x, y, radius, color, frame):
        super().__init__(frame)

        self.x = x
        self.y = y
        self.radius = radius

        self.color = color

    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.circ(x, y, self.radius, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.circ(x, y, self.radius, self.color)


class CircleBorder(Circle):
    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.circb(x, y, self.radius, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.circb(x, y, self.radius, self.color)


class Sprinkles(Displayable):
    def __init__(self, count, color, rectangle: Rectangle):
        super().__init__(rectangle.frame)

        points = []

        for i in range(count):
            lowerx = rectangle.x
            upperx = rectangle.x + rectangle.width - 1

            lowery = rectangle.y + 1
            uppery = rectangle.y + rectangle.height

            x = random.randint(lowerx, upperx)
            y = random.randint(lowery, uppery)

            points.append(Point(x, y, color, rectangle.frame))

        self.points = points

    def display(self):
        for pixel in self.points:
            pixel.display()

    def display_left(self):
        for pixel in self.points:
            pixel.display_left()


class Text(Displayable):
    def __init__(self, text, x, y, color, frame):
        super().__init__(frame)

        self.text = text
        self.x = x
        self.y = y

        self.color = color

    def display(self):
        x, y = self.translate_point(self.x, self.y, self.frame)

        pyxel.text(x, y, self.text, self.color)

    def display_left(self):
        x, y = self.translate_left(self.x, self.y, self.frame)

        pyxel.text(x, y, self.text, self.color)
