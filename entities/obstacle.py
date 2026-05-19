"""Spike / hazard obstacles."""
import pygame
import math
from config import C_SPIKE, C_MAGENTA
from utils.helpers import pulse, draw_platform


class Spike:
    """Triangular spike that kills the player on touch."""

    def __init__(self, x, y, w=32, h=32, flip=False):
        self.rect  = pygame.Rect(x, y, w, h)
        self.flip  = flip          # True = spike points DOWN
        self._t    = 0.0

    def update(self):
        self._t += 1 / 60

    def draw(self, surface, cam):
        r    = cam.apply(self.rect)
        self._t += 0

        glow = int(30 + 20 * pulse(self._t, 4))
        col  = (min(255, C_SPIKE[0] + glow),
                max(0,  C_SPIKE[1] - glow),
                max(0,  C_SPIKE[2] - glow))

        if not self.flip:
            pts = [(r.centerx, r.top),
                   (r.left,    r.bottom),
                   (r.right,   r.bottom)]
        else:
            pts = [(r.centerx, r.bottom),
                   (r.left,    r.top),
                   (r.right,   r.top)]

        pygame.draw.polygon(surface, col, pts)
        # bright outline
        pygame.draw.polygon(surface, (255, 255, 255), pts, 1)


class BouncePad:
    """Green pad that bounces the ball high."""

    def __init__(self, x, y, w=64, h=16, boost=-22):
        self.rect  = pygame.Rect(x, y, w, h)
        self.boost = boost
        self._anim = 0.0

    def update(self):
        if self._anim > 0:
            self._anim -= 0.06

    def trigger(self):
        self._anim = 1.0

    def draw(self, surface, cam):
        r = cam.apply(self.rect)
        compress = int(self._anim * 6)
        draw_r = pygame.Rect(r.x, r.y + compress, r.width, r.height - compress)
        pygame.draw.rect(surface, (40, 220, 100), draw_r, border_radius=6)
        pygame.draw.rect(surface, (80, 255, 140), draw_r, 2, border_radius=6)
        # arrow up
        cx = draw_r.centerx
        ty = draw_r.top - 8
        arrow_pts = [(cx, ty), (cx - 8, ty + 10), (cx + 8, ty + 10)]
        pygame.draw.polygon(surface, (80, 255, 140), arrow_pts)
