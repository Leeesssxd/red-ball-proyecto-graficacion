"""Smooth-follow 2-D camera."""
import pygame
from config import (SCREEN_W, SCREEN_H, CAM_SMOOTH,
                    CAM_OFFSET_X, CAM_OFFSET_Y)
from utils import lerp


class Camera:
    def __init__(self, level_w: int, level_h: int):
        self.x = 0.0
        self.y = 0.0
        self.level_w = level_w
        self.level_h = level_h

    # ── update ───────────────────────────────────────────────
    def update(self, target_x: float, target_y: float):
        dest_x = target_x - CAM_OFFSET_X
        dest_y = target_y - CAM_OFFSET_Y

        # clamp so we never show outside the level
        dest_x = max(0, min(dest_x, self.level_w  - SCREEN_W))
        dest_y = max(0, min(dest_y, self.level_h - SCREEN_H))

        self.x = lerp(self.x, dest_x, CAM_SMOOTH)
        self.y = lerp(self.y, dest_y, CAM_SMOOTH)

    # ── helpers ──────────────────────────────────────────────
    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        return pygame.Rect(rect.x - int(self.x),
                            rect.y - int(self.y),
                            rect.width, rect.height)

    def apply_xy(self, x: float, y: float):
        return x - self.x, y - self.y

    def offset(self):
        return int(self.x), int(self.y)
