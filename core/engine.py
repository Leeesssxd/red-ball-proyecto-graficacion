import pygame
import sys
from config import SCREEN_W, SCREEN_H, FPS, TITLE, C_BG


class State:
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    CHAR_SELECT = "char_select"
    LEVEL_SELECT = "level_select"
    PLAYING = "playing"
    PAUSED = "paused"
    BOSS = "boss"
    VICTORY = "victory"
    GAME_OVER = "game_over"
    TRANSITION = "transition"


class Engine:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
        except pygame.error:
            pass

        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.0
        self._scenes = {}
        self._current = None
        self._next = None
        self._next_args = {}

    def register(self, name, scene):
        self._scenes[name] = scene
        scene.engine = self

    def switch(self, name, **kwargs):
        self._next = name
        self._next_args = kwargs

    def _do_switch(self):
        if self._next is None:
            return
        name = self._next
        self._next = None
        if self._current:
            self._current.on_exit()
        self._current = self._scenes[name]
        self._current.on_enter(**self._next_args)

    def run(self, start_scene):
        self.switch(start_scene)
        while self.running:
            self.dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self._do_switch()

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    self.running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_F4:
                    self.running = False

            if self._current:
                self._current.handle_events(events)
                self._current.update(self.dt)
                self.screen.fill(C_BG)
                self._current.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()


class Scene:
    engine: Engine = None

    def on_enter(self, **kwargs):
        pass

    def on_exit(self):
        pass

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass
