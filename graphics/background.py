"""Arctic parallax background with snow and glacial grid."""
import pygame
import math
import random
from config import SCREEN_W, SCREEN_H


class Flake:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_W)
        self.y = random.uniform(0, SCREEN_H)
        self.z = random.uniform(0.2, 1.0)
        self.v = random.uniform(12, 44)

    def update(self, dt):
        self.y += self.v * self.z * dt
        self.x += math.sin(self.y * 0.01) * 6 * self.z * dt
        if self.y > SCREEN_H + 8:
            self.y = -8
            self.x = random.uniform(0, SCREEN_W)


class Star:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_W)
        self.y = random.uniform(0, SCREEN_H)
        self.size = random.choice([1, 1, 2])
        self.brightness = random.randint(120, 220)
        self.speed = random.choice([0.08, 0.16, 0.3])

    def draw(self, surface, cam_x, t):
        sx = (self.x - cam_x * self.speed) % SCREEN_W
        tw = 0.65 + 0.35 * math.sin(t * 2.2 + self.x * 0.01)
        v = int(self.brightness * tw)
        col = (v, v, min(255, v + 35))
        if self.size == 1:
            surface.set_at((int(sx), int(self.y)), col)
        else:
            pygame.draw.circle(surface, col, (int(sx), int(self.y)), self.size)


class Background:
    def __init__(self):
        self._stars = [Star() for _ in range(180)]
        self._flakes = [Flake() for _ in range(110)]
        self._bg_surf = pygame.Surface((SCREEN_W, SCREEN_H))
        self._bg_surf.fill((6, 12, 28))

    def draw(self, surface, cam_x, cam_y, t):
        surface.blit(self._bg_surf, (0, 0))

        # aurora bands
        aur = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for i in range(3):
            y = int(80 + i * 60 + math.sin(t * 0.4 + i) * 20)
            h = 70
            pygame.draw.ellipse(aur, (90 - i * 10, 180 + i * 18, 220 + i * 8, 26 - i * 5), (-120, y, SCREEN_W + 240, h))
        surface.blit(aur, (0, 0))

        for star in self._stars:
            star.draw(surface, cam_x, t)

        self._draw_glacier_grid(surface, cam_x, t)

        for fl in self._flakes:
            fl.update(1 / 60)
            pygame.draw.circle(surface, (220, 245, 255), (int(fl.x), int(fl.y)), 1 if fl.z < 0.7 else 2)

    def _draw_glacier_grid(self, surface, cam_x, t):
        horizon = SCREEN_H * 0.46
        col_a = (20, 55, 90)
        col_b = (45, 110, 160)

        for i in range(18):
            y_norm = i / 17
            y_screen = horizon + (SCREEN_H - horizon) * (y_norm ** 1.6)
            col = (
                int(col_a[0] + (col_b[0] - col_a[0]) * y_norm),
                int(col_a[1] + (col_b[1] - col_a[1]) * y_norm),
                int(col_a[2] + (col_b[2] - col_a[2]) * y_norm),
            )
            pygame.draw.line(surface, col, (0, int(y_screen)), (SCREEN_W, int(y_screen)), 1)

        cx = SCREEN_W // 2
        num_vlines = 26
        for i in range(num_vlines + 1):
            frac = i / num_vlines
            x_top = cx + (frac - 0.5) * SCREEN_W * 0.35
            x_bot = frac * SCREEN_W
            off = (cam_x * 0.05) % (SCREEN_W / num_vlines)
            x_top -= off * 0.2
            x_bot -= off
            pygame.draw.line(surface, (35, 86, 130), (int(x_top), int(horizon)), (int(x_bot), SCREEN_H), 1)

        scan = pygame.Surface((SCREEN_W, 4), pygame.SRCALPHA)
        scan.fill((130, 215, 255, 30))
        sy = int(horizon + (SCREEN_H - horizon) * ((0.5 + 0.5 * math.sin(t * 0.7)) ** 1.6))
        surface.blit(scan, (0, sy))
