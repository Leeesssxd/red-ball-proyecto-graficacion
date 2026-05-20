"""Goal entity with arctic crystal style."""
import pygame
import math
from config import C_WHITE
from utils.helpers import pulse


class Goal:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
        self._t = 0.0
        self.collected = False

    def update(self):
        self._t += 1 / 60

    def draw(self, surface, cam):
        if self.collected:
            return
        sx, sy = cam.apply_xy(self.x, self.y)
        sx, sy = int(sx), int(sy)

        glow_r = int(self.size + 8 + 5 * pulse(self._t, 2.8))
        glow_s = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        alpha = int(65 + 45 * pulse(self._t, 2.8))
        pygame.draw.circle(glow_s, (150, 235, 255, alpha), (glow_r, glow_r), glow_r)
        surface.blit(glow_s, (sx - glow_r, sy - glow_r))

        self._draw_star(surface, sx, sy, int(self.size * (0.9 + 0.1 * pulse(self._t, 3))), 6, (175, 240, 255))
        pygame.draw.circle(surface, C_WHITE, (sx, sy), 6)

    @staticmethod
    def _draw_star(surface, cx, cy, r, points, colour):
        pts = []
        for i in range(points * 2):
            angle = math.pi / points * i - math.pi / 2
            radius = r if i % 2 == 0 else r * 0.45
            pts.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
        pygame.draw.polygon(surface, colour, pts)
        pygame.draw.polygon(surface, (235, 252, 255), pts, 2)
