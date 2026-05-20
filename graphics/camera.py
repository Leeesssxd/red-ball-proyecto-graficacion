"""Smooth-follow 2-D camera with optional shake."""
import pygame
import math
import random
from config import (SCREEN_W, SCREEN_H, CAM_SMOOTH, CAM_OFFSET_X, CAM_OFFSET_Y)
from utils import lerp


class Camera:
    def __init__(self, level_w: int, level_h: int):
        self.x = 0.0
        self.y = 0.0
        self.level_w = level_w
        self.level_h = level_h
        self._shake = 0.0
        self._sx = 0.0
        self._sy = 0.0

    def add_shake(self, amount=2.0):
        self._shake = max(self._shake, amount)

    def update(self, target_x: float, target_y: float):
        dest_x = target_x - CAM_OFFSET_X
        dest_y = target_y - CAM_OFFSET_Y
        dest_x = max(0, min(dest_x, self.level_w - SCREEN_W))
        dest_y = max(0, min(dest_y, self.level_h - SCREEN_H))

        self.x = lerp(self.x, dest_x, CAM_SMOOTH)
        self.y = lerp(self.y, dest_y, CAM_SMOOTH)

        if self._shake > 0.01:
            ang = random.uniform(0, math.tau)
            self._sx = math.cos(ang) * self._shake
            self._sy = math.sin(ang) * self._shake
            self._shake *= 0.88
        else:
            self._shake = 0.0
            self._sx = 0.0
            self._sy = 0.0

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x - int(self.x - self._sx), rect.y - int(self.y - self._sy), rect.width, rect.height)

    def apply_xy(self, x: float, y: float):
        return x - self.x + self._sx, y - self.y + self._sy

    def offset(self):
        return int(self.x), int(self.y)
