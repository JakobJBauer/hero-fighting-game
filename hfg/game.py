import pyxel
import time
import hfg.plugins as plugins
import os.path

from enum import Enum
from copy import deepcopy

from hfg.base import ThreadStorage, threaded
from hfg.drawing import Drawable, ReferenceFrame
from hfg.helpers import FillerHero, HeroBar
from hfg.shapes import Line, Rectangle, Sprinkles, Text, Circle
from hfg.plugins import Hero, Enemy, DEFAULT_HEALTH, DEFAULT_SPECIAL, DEFAULT_HEIGHT, DEFAULT_WIDTH
from hfg.importer import Importer

DISPLAY_CAPTION = "Hero Fighting Game"
DISPLAY_WIDTH = 256
DISPLAY_HEIGHT = 128
DISPLAY_FPS = 60

CLF_DELAY = 0.2

CLEAR_SCREEN = True

SHOW_MOUSE = True
SHOW_MID = False
SHOW_HINTS = True
SHOW_TITLE = True
SHOW_ROUND = True
SHOW_CURRENT_PLAYER = True
SHOW_SELECTION_TEXT = True

SHOW_HEALTH = True
SHOW_SPECIAL = True

BACKGROUND_COLOR = pyxel.COLOR_BLACK

GROUND_HEIGHT = 30

GROUND_COLOR = pyxel.COLOR_BROWN
GROUND_SPRINKLES_COLOR = pyxel.COLOR_LIGHTGRAY
GROUND_LINE_COLOR = pyxel.COLOR_GREEN

SELECTION_HEIGHT = 30
SELECTION_SLEEP_TIME = 0.01
SELECTION_DIVISOR = 2
SELECTION_OFFSET = 16
SELECTION_STEP = 4

SELECTION_LEFT_KEY = pyxel.KEY_LEFT
SELECTION_RIGHT_KEY = pyxel.KEY_RIGHT
SELECTION_ENTER_KEY = pyxel.KEY_ENTER

FIGHT_LEFT_KEY = pyxel.KEY_LEFT
FIGHT_RIGHT_KEY = pyxel.KEY_RIGHT
FIGHT_BLOCK_KEY = pyxel.KEY_B
FIGHT_SUPER_KEY = pyxel.KEY_S
FIGHT_ATTACK_KEY = pyxel.KEY_A

HERO_HEALTH_COLOR = pyxel.COLOR_RED
HERO_HEALTH_BAR_DISTANCE = 15 - 10
HERO_SPECIAL_BAR_DISTANCE = 18 - 10
HERO_BAR_LENGTH = 50
HERO_TITLE_HEIGHT = 18
HERO_TITLE_COLOR = pyxel.COLOR_WHITE

SELECTION_HEIGHT_FROM_TOP = 8
SELECTION_TEXT_COLOR = pyxel.COLOR_WHITE

ROUND_HEIGHT_FROM_TOP = 8
ROUND_TEXT_COLOR = pyxel.COLOR_WHITE

MINIMUM_HERO_DISTANCE = 0


class GameStates(Enum):
    RESTART = 0
    SELECT_RIGHT = 1
    SELECT_LEFT = 2
    START = 3
    WAITING_START = 4
    ROUND_RIGHT = 5
    WAITING_RIGHT = 6
    ROUND_LEFT = 7
    WAITING_LEFT = 8
    WIN_RIGHT = 9
    WIN_LEFT = 10
    WAITING_END = 11


class HeroesSelection(Drawable, ThreadStorage):
    def __init__(self, heroes: list):
        Drawable.__init__(self, ReferenceFrame())
        ThreadStorage.__init__(self)

        self.selector = 2
        self.heroes = heroes
        self._arrange(self.selector)

    def _arrange(self, index):
        heroes = self.heroes

        for i in range(len(heroes)):
            heroes[i].move_frame((i - index + 1) * pyxel.width // SELECTION_DIVISOR - SELECTION_OFFSET, SELECTION_HEIGHT)
            self.draw(heroes[i])

        self.release()

    def _move(self, count):
        heroes = self.heroes

        for i in range(len(heroes)):
            heroes[i].move_frame(heroes[i].x + count, SELECTION_HEIGHT)
            self.draw(heroes[i])

        self.release()

    @threaded
    def right(self):
        if self.selector < len(self.heroes) - 1:
            self.selector += 1

            for i in range(pyxel.width // (SELECTION_DIVISOR * SELECTION_STEP)):
                self._move(-SELECTION_STEP)
                time.sleep(SELECTION_SLEEP_TIME)

    @threaded
    def left(self):
        if self.selector > 2:
            self.selector -= 1

            for i in range(pyxel.width // (SELECTION_DIVISOR * SELECTION_STEP)):
                self._move(SELECTION_STEP)
                time.sleep(SELECTION_SLEEP_TIME)

    def selected_hero(self) -> Hero:
        return self.heroes[self.selector]


class Display(Drawable):
    def __init__(self):
        super().__init__(ReferenceFrame())


class App:
    def __init__(self, heroes: list):
        pyxel.init(DISPLAY_WIDTH, DISPLAY_HEIGHT, caption=DISPLAY_CAPTION, fps=DISPLAY_FPS)
        pyxel.mouse(SHOW_MOUSE)

        self.display = Display()

        self.heroes = heroes
        self.state = GameStates.RESTART

        self.button_clf_max = CLF_DELAY * DISPLAY_FPS
        self.button_clf = 0

        self.heroes_selection = None
        self.right = None
        self.left = None
        self.left_is_winner = False

        self.round = 1

        self.ground = Rectangle(0, 0, pyxel.width, GROUND_HEIGHT, GROUND_COLOR, ReferenceFrame(0, 0))
        self.ground_sprinkles = Sprinkles(30, GROUND_SPRINKLES_COLOR, self.ground)
        self.ground_line = Line(0, 0, pyxel.width, 0, GROUND_LINE_COLOR, ReferenceFrame(0, GROUND_HEIGHT))

        pyxel.run(self.update, self.draw)

    @staticmethod
    def _show_mid():
        x1 = pyxel.width // 2
        y1 = 0
        x2 = x1
        y2 = pyxel.height

        Line(x1, y1, x2, y2, pyxel.COLOR_WHITE, ReferenceFrame()).display()

    def _show_ground(self):
        self.ground.display()
        self.ground_sprinkles.display()
        self.ground_line.display()

    def _show_hints(self):
        pass

    def _select(self):
        hs = self.heroes_selection

        if not self.button_clf:
            if pyxel.btn(SELECTION_RIGHT_KEY):
                self.button_clf = self.button_clf_max

                if not hs.get("right") or not hs["right"].is_alive():
                    hs.store("right", hs.right())
            elif pyxel.btn(SELECTION_LEFT_KEY):
                self.button_clf = self.button_clf_max

                if not hs.get("left") or not hs["left"].is_alive():
                    hs.store("left", hs.left())
            elif pyxel.btn(SELECTION_ENTER_KEY):
                self.button_clf = self.button_clf_max

                hero = deepcopy(self.heroes_selection.selected_hero())
                hero.clear()

                return hero
        else:
            if self.button_clf > 0:
                self.button_clf -= 1
            if self.button_clf <= 0:
                self.button_clf = 0

    def _preview(self):
        for hero in self.heroes:
            hero.clear()
            hero.selection_preview()

    def _fight(self, active: Hero, passive: Enemy):
        if not self.button_clf:
            if pyxel.btn(FIGHT_ATTACK_KEY):
                active.store("fighting", active.attack(passive))
            elif pyxel.btn(FIGHT_SUPER_KEY):
                active.store("fighting", active.super(passive))
            elif pyxel.btn(FIGHT_BLOCK_KEY):
                active.store("fighting", active.block(passive))
            elif pyxel.btn(FIGHT_RIGHT_KEY):
                active.store("fighting", active.walk(1, passive))
            elif pyxel.btn(FIGHT_LEFT_KEY):
                active.store("fighting", active.walk(-1, passive))
            else:
                return False

            self.button_clf = self.button_clf_max
            return True
        else:
            if self.button_clf > 0:
                self.button_clf -= 1
            if self.button_clf <= 0:
                self.button_clf = 0

    def _round_over(self, next_state: GameStates):
        self.right.clear()
        self.left.clear()

        if self.right.x - self.left.x < MINIMUM_HERO_DISTANCE:
            self.left.x = self.right.x - MINIMUM_HERO_DISTANCE

        if self.left.health < 1:
            self.state = GameStates.WIN_RIGHT
        elif self.right.health < 1:
            self.state = GameStates.WIN_LEFT
        else:
            if next_state == GameStates.ROUND_RIGHT:
                self.round += 1
            self.state = next_state

    def update(self):
        if self.state == GameStates.RESTART:
            self.heroes_selection = HeroesSelection(self.heroes)

            self.state = GameStates.SELECT_RIGHT

        elif self.state == GameStates.SELECT_RIGHT:
            self._preview()
            hero = self._select()

            if hero is not None:
                self.right = hero
                self.state = GameStates.SELECT_LEFT

        elif self.state == GameStates.SELECT_LEFT:
            self._preview()
            hero = self._select()

            if hero is not None:
                self.left = hero
                self.state = GameStates.START
                self.button_clf = 0

        elif self.state == GameStates.START:
            self.left.move_frame(pyxel.width // 4, GROUND_HEIGHT)
            self.right.move_frame(3 * (pyxel.width // 4), GROUND_HEIGHT)

            self.right.store("start_animation", self.right.start_animation(self.left))
            self.left.store("start_animation", self.left.start_animation(self.right))

            self.state = GameStates.WAITING_START

        elif self.state == GameStates.WAITING_START:
            if not (self.right.running() or self.left.running()):
                self.state = GameStates.ROUND_RIGHT

        elif self.state == GameStates.ROUND_RIGHT:
            self.display.draw(Text(f"Right is playing ({self.right.title})", 10, 10,
                                   pyxel.COLOR_WHITE, ReferenceFrame()))
            if self._fight(self.right, self.left):
                self.state = GameStates.WAITING_RIGHT

        elif self.state == GameStates.WAITING_RIGHT:
            if not self.right.running():
                self._round_over(GameStates.ROUND_LEFT)

        elif self.state == GameStates.ROUND_LEFT:
            self.display.draw(
                Text(f"Left is playing ({self.left.title})", 10, 10, pyxel.COLOR_WHITE, ReferenceFrame()))
            if self._fight(self.left, self.right):
                self.state = GameStates.WAITING_LEFT

        elif self.state == GameStates.WAITING_LEFT:
            if not self.left.running():
                self._round_over(GameStates.ROUND_RIGHT)

        elif self.state == GameStates.WIN_RIGHT:
            left = self.left
            right = self.right

            self.left_is_winner = False

            left.store("end", left.lose_animation(self.right))
            right.store("end", right.win_animation(self.left))

            self.state = GameStates.WAITING_END

        elif self.state == GameStates.WIN_LEFT:
            left = self.left
            right = self.right

            self.left_is_winner = True

            right.store("end", right.lose_animation(self.left))
            left.store("end", left.win_animation(self.right))

            self.state = GameStates.WAITING_END

        elif self.state == GameStates.WAITING_END:
            if self.left_is_winner:
                winner_name = self.left.title
                position = "left"
            else:
                winner_name = self.right.title
                position = "right"

            self.display.draw(Text(f"Game over! Player {position} ({winner_name}) wins!", 10, 10, pyxel.COLOR_WHITE,
                                   ReferenceFrame()))
            if not (self.right.running() or self.left.running()):
                self.state = GameStates.RESTART

    def draw(self):
        if CLEAR_SCREEN:
            pyxel.cls(BACKGROUND_COLOR)
        if SHOW_MID:
            self._show_mid()
        if not (self.state == GameStates.SELECT_RIGHT or self.state == GameStates.SELECT_LEFT):
            self._show_ground()

        if self.state == GameStates.SELECT_LEFT or self.state == GameStates.SELECT_RIGHT:
            Text("Choose one:", pyxel.width // 4, 70, pyxel.COLOR_WHITE, ReferenceFrame()).display()

            if SHOW_TITLE:
                for hero in self.heroes_selection.heroes:
                    Text(hero.title, 0, HERO_TITLE_HEIGHT + hero.height, HERO_TITLE_COLOR, hero.frame).display()
            self.heroes_selection.display()

            if SHOW_SELECTION_TEXT:
                if self.state == GameStates.SELECT_RIGHT:
                    Text(f"Select right player", 10, 10, pyxel.COLOR_WHITE, ReferenceFrame()).display()
                elif self.state == GameStates.SELECT_LEFT:
                    Text(f"Select left player", 10, 10, pyxel.COLOR_WHITE, ReferenceFrame()).display()
        else:
            if SHOW_TITLE:
                if self.state == GameStates.WAITING_END:
                    if self.left_is_winner:
                        color_left = pyxel.COLOR_GREEN
                        color_right = pyxel.COLOR_RED
                    else:
                        color_left = pyxel.COLOR_RED
                        color_right = pyxel.COLOR_GREEN
                else:
                    color_right = HERO_TITLE_COLOR
                    color_left = HERO_TITLE_COLOR

                self.display.draw(Text(self.left.title, - self.left.width,
                                       HERO_TITLE_HEIGHT + self.left.height,
                                       color_left, self.left.frame))
                self.display.draw(Text(self.right.title, 0,
                                       HERO_TITLE_HEIGHT + self.right.height,
                                       color_right, self.right.frame))

            if not (self.state == GameStates.WIN_LEFT or
                    self.state == GameStates.WAITING_END or
                    self.state == GameStates.WIN_RIGHT):
                if SHOW_HEALTH:
                    HeroBar(self.left.health, DEFAULT_HEALTH,
                            HERO_BAR_LENGTH, HERO_HEALTH_BAR_DISTANCE,
                            HERO_HEALTH_COLOR, self.left).display_left()
                    HeroBar(self.right.health, DEFAULT_HEALTH,
                            HERO_BAR_LENGTH, HERO_HEALTH_BAR_DISTANCE,
                            HERO_HEALTH_COLOR, self.right).display()
                if SHOW_SPECIAL:
                    HeroBar(self.left.special, DEFAULT_SPECIAL,
                            HERO_BAR_LENGTH, HERO_SPECIAL_BAR_DISTANCE,
                            self.left.special_color, self.left).display_left()
                    HeroBar(self.right.special, DEFAULT_SPECIAL,
                            HERO_BAR_LENGTH, HERO_SPECIAL_BAR_DISTANCE,
                            self.right.special_color, self.right).display()

            if SHOW_ROUND and not (self.state == GameStates.WIN_LEFT or
                                   self.state == GameStates.WIN_RIGHT or
                                   self.state == GameStates.WAITING_END):
                pyxel.text(10, ROUND_HEIGHT_FROM_TOP, f"Round {self.round}", ROUND_TEXT_COLOR)

            self.display.release()
            self.display.display()

            if self.state == GameStates.ROUND_RIGHT or self.state == GameStates.WAITING_RIGHT:
                self.left.display_left()
                self.right.display()
            else:
                self.right.display()
                self.left.display_left()


imported_heroes = Importer(os.path.dirname(plugins.__file__)).import_heroes()

for i in range(2):
    imported_heroes.insert(0, FillerHero())

print(imported_heroes)

App(imported_heroes)
