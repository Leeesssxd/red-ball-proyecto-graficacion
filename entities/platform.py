"""Platform entity – static, moving, or crumbling (arctic skin)."""
import pygame
from config import C_PLAT_TOP, C_PLAT_SIDE
from utils.helpers import draw_platform


class Platform:
    KIND_STATIC = "static"
    KIND_MOVING = "moving"
    KIND_CRUMBLE = "crumble"

    def __init__(self, x, y, w, h, kind=KIND_STATIC, move_range=0, move_speed=1.5, move_axis="x", colour_top=None, colour_side=None):
        self.rect = pygame.Rect(x, y, w, h)
        self._origin_x = x
        self._origin_y = y
        self.kind = kind
        self.move_range = move_range
        self.move_speed = move_speed
        self.move_axis = move_axis
        self._t = 0.0
        self.dx = 0
        self.dy = 0

        self.crumble_timer = 0
        self.crumble_max = 90
        self.crumbling = False
        self.gone = False

        self.col_top = colour_top or C_PLAT_TOP
        self.col_side = colour_side or C_PLAT_SIDE

    def update(self):
        self.dx = 0
        self.dy = 0
        oldx, oldy = self.rect.x, self.rect.y
        if self.kind == self.KIND_MOVING:
            import math
            self._t += 0.02
            offset = math.sin(self._t * self.move_speed) * self.move_range
            if self.move_axis == "x":
                self.rect.x = int(self._origin_x + offset)
            else:
                self.rect.y = int(self._origin_y + offset)
        self.dx = self.rect.x - oldx
        self.dy = self.rect.y - oldy

        if self.crumbling:
            self.crumble_timer += 1
            if self.crumble_timer >= self.crumble_max:
                self.gone = True

    def trigger_crumble(self):
        if self.kind == self.KIND_CRUMBLE and not self.crumbling:
            self.crumbling = True

    def draw(self, surface, cam):
        if self.gone:
            return
        r = cam.apply(self.rect)

        if self.crumbling:
            ratio = 1.0 - self.crumble_timer / self.crumble_max
            import random
            shake = int(2 + 3 * (1 - ratio))
            r = r.move(random.randint(-shake, shake), random.randint(-shake, shake))
            alpha_surf = pygame.Surface((r.width, r.height + 14), pygame.SRCALPHA)
            col_t = tuple(int(c * ratio) for c in self.col_top)
            col_s = tuple(int(c * ratio) for c in self.col_side)
            draw_platform(alpha_surf, pygame.Rect(0, 0, r.width, r.height), col_t, col_s)
            frost = pygame.Surface(alpha_surf.get_size(), pygame.SRCALPHA)
            frost.fill((210, 245, 255, 20))
            alpha_surf.blit(frost, (0, 0))
            surface.blit(alpha_surf, (r.x, r.y))
            return

        draw_platform(surface, r, self.col_top, self.col_side)
        shine = pygame.Surface((r.width, max(2, r.height // 4)), pygame.SRCALPHA)
        shine.fill((235, 250, 255, 28))
        surface.blit(shine, (r.x, r.y + 2))

        # small props: snow mounds
        seed = (self.rect.x * 73856093 + self.rect.y * 19349663) & 0xFFFFFFFF
        if seed % 3 == 0 and r.width > 70:
            pygame.draw.ellipse(surface, (230, 248, 255), (r.x + 8, r.y - 6, 24, 8))
        if seed % 5 == 0 and r.width > 120:
            pygame.draw.ellipse(surface, (210, 236, 248), (r.right - 34, r.y - 5, 20, 7))
