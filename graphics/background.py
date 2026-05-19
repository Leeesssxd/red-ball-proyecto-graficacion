"""Parallax background with neon pseudo-3D grid."""
import pygame
import math
import random
from config import SCREEN_W, SCREEN_H, C_BG, C_GRID, C_GRID2, PARALLAX_SPEEDS


class Star:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_W)
        self.y = random.uniform(0, SCREEN_H)
        self.size = random.choice([1, 1, 1, 2])
        self.brightness = random.randint(120, 255)
        self.speed = random.choice(PARALLAX_SPEEDS)

    def draw(self, surface, cam_x, t):
        sx = (self.x - cam_x * self.speed) % SCREEN_W
        tw = 0.7 + 0.3 * math.sin(t * 2.5 + self.x * 0.01)
        v = int(self.brightness * tw)
        col = (v, v, min(255, v + 20))
        if self.size == 1:
            surface.set_at((int(sx), int(self.y)), col)
        else:
            pygame.draw.circle(surface, col, (int(sx), int(self.y)), self.size)


class Background:
    def __init__(self):
        self._stars = [Star() for _ in range(240)]
        self._bg_surf = pygame.Surface((SCREEN_W, SCREEN_H))
        self._bg_surf.fill(C_BG)

    def draw(self, surface, cam_x, cam_y, t):
        surface.blit(self._bg_surf, (0, 0))
        for star in self._stars:
            star.draw(surface, cam_x, t)
        self._draw_grid(surface, cam_x, cam_y, t)

    def _draw_grid(self, surface, cam_x, cam_y, t):
        horizon = SCREEN_H * 0.43

        for i in range(18):
            y_norm = i / 17
            y_screen = horizon + (SCREEN_H - horizon) * (y_norm ** 1.62)
            col = (
                int(C_GRID[0] + (C_GRID2[0] - C_GRID[0]) * y_norm),
                int(C_GRID[1] + (C_GRID2[1] - C_GRID[1]) * y_norm),
                int(C_GRID[2] + (C_GRID2[2] - C_GRID[2]) * y_norm),
            )
            pygame.draw.line(surface, col, (0, int(y_screen)), (SCREEN_W, int(y_screen)), 1)

        cx = SCREEN_W // 2
        num_vlines = 30
        for i in range(num_vlines + 1):
            frac = i / num_vlines
            x_top = cx + (frac - 0.5) * SCREEN_W * 0.36
            x_bot = frac * SCREEN_W
            off = (cam_x * PARALLAX_SPEEDS[0] * 0.5) % (SCREEN_W / num_vlines)
            x_top -= off * 0.2
            x_bot -= off
            col_v = (35, 68, 112)
            pygame.draw.line(surface, col_v, (int(x_top), int(horizon)), (int(x_bot), SCREEN_H), 1)

        glow = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        scan_y = int(horizon + (SCREEN_H - horizon) * ((0.5 + 0.5 * math.sin(t * 0.8)) ** 1.8))
        pygame.draw.rect(glow, (0, 190, 255, 28), (0, scan_y, SCREEN_W, 5))
        surface.blit(glow, (0, 0))
