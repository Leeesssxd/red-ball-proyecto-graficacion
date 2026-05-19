"""Title screen and win screen."""
import pygame
import math
from config import SCREEN_W, SCREEN_H, C_BG, C_BALL, C_WHITE, C_CYAN
from utils.helpers import pulse


class TitleScreen:
    def __init__(self):
        pygame.font.init()
        try:
            self._font_title = pygame.font.SysFont("impact", 118, bold=True)
            self._font_sub = pygame.font.SysFont("consolas", 28)
            self._font_hint = pygame.font.SysFont("consolas", 20)
        except Exception:
            self._font_title = pygame.font.Font(None, 118)
            self._font_sub = pygame.font.Font(None, 30)
            self._font_hint = pygame.font.Font(None, 22)
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface):
        surface.fill(C_BG)
        for i in range(0, SCREEN_W, 72):
            pygame.draw.line(surface, (18, 34, 58), (i, 0), (i, SCREEN_H))
        for j in range(0, SCREEN_H, 56):
            pygame.draw.line(surface, (16, 28, 50), (0, j), (SCREEN_W, j))

        y = SCREEN_H // 2 - 190 + int(8 * math.sin(self._t * 2.1))
        title_shadow = self._font_title.render("REDBALL", True, (30, 10, 10))
        title = self._font_title.render("REDBALL", True, C_BALL)
        tx = SCREEN_W // 2 - title.get_width() // 2

        glow = pygame.Surface((title.get_width() + 70, title.get_height() + 40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 35, 45, 55), glow.get_rect())
        surface.blit(glow, (tx - 35, y - 12))
        surface.blit(title_shadow, (tx + 6, y + 8))
        surface.blit(title, (tx, y))

        sub = self._font_sub.render("Neon Kinetics Edition", True, (120, 220, 255))
        surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, y + 125))

        alpha = int(180 + 75 * pulse(self._t, 1.8))
        hint = self._font_hint.render("Press ENTER to launch", True, C_WHITE)
        hint.set_alpha(alpha)
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 50))

        ctrl = self._font_hint.render("Arrows / A,D Move   Space Jump   R Restart", True, C_CYAN)
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

    def draw(self, surface, time_str=""):
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 10, 20, 190))
        surface.blit(dim, (0, 0))

        col = (220, int(190 + 65 * pulse(self._t, 2.2)), 40)
        txt = self._font_big.render("YOU WIN", True, col)
        tx = SCREEN_W // 2 - txt.get_width() // 2
        ty = SCREEN_H // 2 - 105
        surface.blit(txt, (tx, ty))

        if time_str:
            ts = self._font_sm.render(f"Run Time: {time_str}", True, (220, 235, 255))
            surface.blit(ts, (SCREEN_W // 2 - ts.get_width() // 2, ty + 110))

        hint = self._font_sm.render("ENTER Restart   ESC Quit", True, (120, 180, 255))
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 62))

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return ""
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return "restart"
        if event.key == pygame.K_ESCAPE:
            return "quit"
        return ""
