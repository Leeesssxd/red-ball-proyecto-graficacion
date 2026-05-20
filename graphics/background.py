"""Image-based arctic background manager (no sci-fi grid)."""
import os
import pygame
import random

from config import SCREEN_W, SCREEN_H


class Background:
    def __init__(self):
        self._cache = {}
        self._theme = None
        self._snow = [[random.uniform(0, SCREEN_W), random.uniform(0, SCREEN_H), random.uniform(12, 50), random.uniform(0.3, 1.0)] for _ in range(120)]

    def set_theme(self, theme):
        if self._theme != theme:
            self._theme = theme
            if theme not in self._cache:
                self._cache[theme] = self._build_theme(theme)

    def _load_file_bg(self, path):
        img = pygame.image.load(path).convert()
        iw, ih = img.get_size()
        # Crop tiny bottom strip to reduce visible watermark artifacts
        crop_h = max(1, int(ih * 0.94))
        img = img.subsurface(pygame.Rect(0, 0, iw, crop_h)).copy()
        return pygame.transform.smoothscale(img, (SCREEN_W, SCREEN_H))

    def _build_theme(self, theme):
        file_map = {
            "final_image": os.path.join("assets", "backgrounds", "nivel_final.jpg"),
            "secret_image": os.path.join("assets", "backgrounds", "nivel_final_secreto.jpg"),
        }
        if theme in file_map and os.path.exists(file_map[theme]):
            return self._load_file_bg(file_map[theme])

        surf = pygame.Surface((SCREEN_W, SCREEN_H))
        palettes = {
            "tundra_day": ((154, 210, 248), (220, 243, 255), (82, 126, 170), (34, 66, 102)),
            "forest_blue": ((72, 150, 208), (180, 228, 248), (58, 110, 150), (20, 52, 90)),
            "dusk_violet": ((170, 126, 178), (244, 202, 220), (106, 72, 120), (52, 36, 62)),
            "sunset_ice": ((40, 132, 194), (255, 180, 120), (72, 86, 160), (24, 36, 90)),
        }
        top, sun, m1, m2 = palettes.get(theme, palettes["tundra_day"])

        for y in range(SCREEN_H):
            t = y / SCREEN_H
            r = int(top[0] * (1 - t) + 12 * t)
            g = int(top[1] * (1 - t) + 30 * t)
            b = int(top[2] * (1 - t) + 60 * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W, y))

        pygame.draw.circle(surf, sun, (SCREEN_W - 220, 140), 78)

        pts_far = [(0, 380), (180, 290), (360, 360), (520, 250), (700, 340), (900, 240), (1120, 360), (1280, 300), (1280, 720), (0, 720)]
        pts_near = [(0, 470), (140, 360), (280, 430), (430, 320), (620, 455), (820, 340), (1030, 470), (1240, 360), (1280, 410), (1280, 720), (0, 720)]
        pygame.draw.polygon(surf, m1, pts_far)
        pygame.draw.polygon(surf, m2, pts_near)

        for x in range(0, SCREEN_W, 26):
            h = random.randint(26, 72)
            pygame.draw.polygon(surf, (26, 44, 58), [(x, SCREEN_H - 80), (x + 12, SCREEN_H - 80 - h), (x + 24, SCREEN_H - 80)])

        return surf

    def draw(self, surface, cam_x, cam_y, t):
        if self._theme is None:
            self.set_theme("tundra_day")
        base = self._cache[self._theme]
        surface.blit(base, (0, 0))

        # snow pass
        snow_layer = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for fl in self._snow:
            fl[1] += fl[2] * fl[3] * (1 / 60)
            fl[0] += fl[3] * 0.25
            if fl[1] > SCREEN_H + 5:
                fl[1] = -5
                fl[0] = random.uniform(0, SCREEN_W)
            if fl[0] > SCREEN_W + 2:
                fl[0] = -2
            r = 1 if fl[3] < 0.8 else 2
            pygame.draw.circle(snow_layer, (235, 247, 255, 160), (int(fl[0]), int(fl[1])), r)
        surface.blit(snow_layer, (0, 0))
