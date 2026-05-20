"""Title screen and win screen."""
import pygame
import math
from config import SCREEN_W, SCREEN_H, C_WHITE
from utils.helpers import pulse


class TitleScreen:
    def __init__(self):
        pygame.font.init()
        self._font_title = pygame.font.SysFont("impact", 102, bold=True)
        self._font_sub = pygame.font.SysFont("consolas", 26)
        self._font_hint = pygame.font.SysFont("consolas", 20)
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface):
        surface.fill((7, 14, 28))
        for i in range(0, SCREEN_W, 96):
            pygame.draw.line(surface, (16, 38, 62), (i, 0), (i, SCREEN_H))

        y = SCREEN_H // 2 - 180 + int(8 * math.sin(self._t * 2.1))
        title_shadow = self._font_title.render("FROSTBOUND PAWS", True, (20, 40, 58))
        title = self._font_title.render("FROSTBOUND PAWS", True, (210, 245, 255))
        tx = SCREEN_W // 2 - title.get_width() // 2

        glow = pygame.Surface((title.get_width() + 70, title.get_height() + 40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (130, 215, 255, 48), glow.get_rect())
        surface.blit(glow, (tx - 35, y - 12))
        surface.blit(title_shadow, (tx + 6, y + 8))
        surface.blit(title, (tx, y))

        sub = self._font_sub.render("Polar Bear Indie Adventure", True, (150, 225, 255))
        surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, y + 120))

        alpha = int(180 + 75 * pulse(self._t, 1.8))
        hint = self._font_hint.render("Press ENTER to start expedition", True, C_WHITE)
        hint.set_alpha(alpha)
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 52))

        ctrl = self._font_hint.render("Arrows/A,D Move   Space Jump   R Restart", True, (155, 216, 248))
        surface.blit(ctrl, (SCREEN_W // 2 - ctrl.get_width() // 2, SCREEN_H - 45))

    def handle_event(self, event):
        return event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)


class WinScreen:
    def __init__(self):
        pygame.font.init()
        self._font_big = pygame.font.SysFont("impact", 84)
        self._font_sm = pygame.font.SysFont("consolas", 24)
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface, time_str="", coin_count=0, secret_open=False):
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((5, 16, 28, 198))
        surface.blit(dim, (0, 0))

        col = (200, int(210 + 45 * pulse(self._t, 2.2)), 255)
        txt = self._font_big.render("EXPEDITION COMPLETE", True, col)
        tx = SCREEN_W // 2 - txt.get_width() // 2
        ty = SCREEN_H // 2 - 120
        surface.blit(txt, (tx, ty))

        if time_str:
            ts = self._font_sm.render(f"Time: {time_str}", True, (220, 240, 255))
            surface.blit(ts, (SCREEN_W // 2 - ts.get_width() // 2, ty + 100))

        rel = self._font_sm.render(f"Relics: {coin_count}/3", True, (220, 240, 255))
        surface.blit(rel, (SCREEN_W // 2 - rel.get_width() // 2, ty + 136))
        sec = "Secret Cleared" if secret_open else "Secret Locked"
        sec_col = (160, 245, 255) if secret_open else (220, 220, 235)
        ss = self._font_sm.render(sec, True, sec_col)
        surface.blit(ss, (SCREEN_W // 2 - ss.get_width() // 2, ty + 170))

        hint = self._font_sm.render("ENTER Restart   ESC Quit", True, (140, 210, 245))
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 90))

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return ""
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return "restart"
        if event.key == pygame.K_ESCAPE:
            return "quit"
        return ""
