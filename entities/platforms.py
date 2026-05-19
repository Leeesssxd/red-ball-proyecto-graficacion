import math
import pygame
from config import C_WHITE, C_GREEN, C_YELLOW, PLATFORM_THICKNESS, SHADOW_OFFSET_X, SHADOW_OFFSET_Y


class Platform:
    COLOR = (60, 90, 160)
    EDGE_COLOR = (100, 140, 220)

    def __init__(self, x, y, w, h):
        self.x, self.y = float(x), float(y)
        self.w, self.h = float(w), float(h)
        self.solid = True
        self.enabled = True

    @property
    def rect(self):
        return pygame.FRect(self.x, self.y, self.w, self.h)

    def update(self, dt):
        pass

    def collide_player(self, player):
        if not self.enabled or not self.solid:
            return
        r = player.radius
        px, py = player.x, player.y
        vx, vy = player.vx, player.vy

        ex = self.x - r
        ey = self.y - r
        ew = self.w + r * 2
        eh = self.h + r * 2
        if not (ex <= px <= ex + ew and ey <= py <= ey + eh):
            return

        overlap_left = px - self.x
        overlap_right = (self.x + self.w) - px
        overlap_top = py - self.y
        overlap_bot = (self.y + self.h) - py
        min_ov = min(overlap_left, overlap_right, overlap_top, overlap_bot)

        was_on = player.on_ground
        if min_ov == overlap_top and vy >= 0:
            if not was_on and hasattr(player, "land_vfx"):
                player.land_vfx()
            player.y = self.y - r
            player.vy = 0.0
            player.on_ground = True
            self.on_land(player)
        elif min_ov == overlap_bot and vy < 0:
            player.y = self.y + self.h + r
            player.vy = abs(player.vy) * 0.3
        elif min_ov == overlap_left and vx > 0:
            player.x = self.x - r
            player.vx = -player.vx * 0.2
        elif min_ov == overlap_right and vx < 0:
            player.x = self.x + self.w + r
            player.vx = -player.vx * 0.2

    def on_land(self, player):
        pass

    def draw(self, surface, camera):
        if hasattr(camera, "rect_visible") and not camera.rect_visible(self.x, self.y, self.w, self.h):
            return
        self._draw_pseudo3d(surface, camera, self.COLOR, self.EDGE_COLOR)

    def _draw_pseudo3d(self, surface, camera, top_col, edge_col):
        sx, sy = camera.world_to_screen(self.x, self.y)
        sw = camera.scale(self.w)
        sh = camera.scale(self.h)
        thick = camera.scale(PLATFORM_THICKNESS)

        shad_rect = pygame.Rect(int(sx + SHADOW_OFFSET_X), int(sy + SHADOW_OFFSET_Y), int(sw), int(sh + thick))
        s = pygame.Surface((max(1, shad_rect.w + 4), max(1, shad_rect.h + 4)), pygame.SRCALPHA)
        pygame.draw.rect(s, (0, 0, 0, 60), (0, 0, shad_rect.w, shad_rect.h), border_radius=4)
        surface.blit(s, shad_rect.topleft)

        side_pts = [(int(sx), int(sy + sh)), (int(sx + sw), int(sy + sh)), (int(sx + sw), int(sy + sh + thick)), (int(sx), int(sy + sh + thick))]
        pygame.draw.polygon(surface, edge_col, side_pts)

        top_rect = pygame.Rect(int(sx), int(sy), int(sw), int(sh))
        pygame.draw.rect(surface, top_col, top_rect, border_radius=4)
        pygame.draw.line(surface, (200, 220, 255), (int(sx + 2), int(sy + 2)), (int(sx + sw - 2), int(sy + 2)), 2)


class MovingPlatform(Platform):
    COLOR = (40, 130, 80)
    EDGE_COLOR = (60, 200, 120)

    def __init__(self, x, y, w, h, path, speed=80):
        super().__init__(x, y, w, h)
        self._path = path
        self._speed = speed
        self._idx = 0
        self._prev_x = x
        self._prev_y = y

    def update(self, dt):
        if len(self._path) < 2:
            return
        self._prev_x, self._prev_y = self.x, self.y
        tx, ty = self._path[self._idx]
        dx, dy = tx - self.x, ty - self.y
        dist = math.hypot(dx, dy)
        step = self._speed * dt
        if dist <= step:
            self.x, self.y = float(tx), float(ty)
            self._idx = (self._idx + 1) % len(self._path)
        else:
            self.x += (dx / dist) * step
            self.y += (dy / dist) * step

    def on_land(self, player):
        player.x += self.x - self._prev_x
        player.y += self.y - self._prev_y


class BouncePad(Platform):
    COLOR = (200, 60, 200)
    EDGE_COLOR = (255, 100, 255)
    BOUNCE_MUL = 1.7

    def __init__(self, x, y, w=80, h=14):
        super().__init__(x, y, w, h)
        self._anim = 0.0

    def update(self, dt):
        self._anim = max(0.0, self._anim - dt * 5)

    def on_land(self, player):
        jump_v = getattr(player, "jump_vel", 700)
        player.vy = -(abs(player.vy) * self.BOUNCE_MUL + jump_v * 0.6)
        player.on_ground = False
        self._anim = 1.0
        if hasattr(player, "bounce_vfx"):
            player.bounce_vfx()


class CrumblingPlatform(Platform):
    COLOR = (140, 100, 40)
    EDGE_COLOR = (180, 140, 60)
    CRUMBLE_DELAY = 0.7
    RESPAWN_DELAY = 3.0

    def __init__(self, x, y, w=100, h=16):
        super().__init__(x, y, w, h)
        self._timer = 0.0
        self._state = "solid"

    def update(self, dt):
        if self._state == "shaking":
            self._timer -= dt
            if self._timer <= 0:
                self._state = "gone"
                self.enabled = False
                self._timer = self.RESPAWN_DELAY
        elif self._state == "gone":
            self._timer -= dt
            if self._timer <= 0:
                self._state = "solid"
                self.enabled = True

    def on_land(self, player):
        if self._state == "solid":
            self._state = "shaking"
            self._timer = self.CRUMBLE_DELAY


class Hazard(Platform):
    COLOR = (200, 30, 30)
    EDGE_COLOR = (255, 80, 60)

    def __init__(self, x, y, w=40, h=16, damage=1):
        super().__init__(x, y, w, h)
        self.damage = damage
        self._pulse = 0.0

    def update(self, dt):
        self._pulse = (self._pulse + dt * 3) % math.tau

    def on_land(self, player):
        if getattr(player, "inv_time", 0) <= 0:
            if hasattr(player, "hp"):
                player.hp -= self.damage
            player.inv_time = 1.5
            player.vy = -400
            if hasattr(player, "hp") and player.hp <= 0:
                player.alive = False


class Checkpoint:
    RADIUS = 14

    def __init__(self, x, y):
        self.x, self.y = float(x), float(y)
        self.activated = False
        self._anim = 0.0

    def update(self, dt):
        self._anim = (self._anim + dt * 2) % math.tau

    def check(self, player):
        if self.activated:
            return
        if math.hypot(player.x - self.x, player.y - self.y) < self.RADIUS + player.radius:
            self.activated = True
            if hasattr(player, "set_checkpoint"):
                player.set_checkpoint(self.x, self.y)

    def draw(self, surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)
        col = C_GREEN if self.activated else C_YELLOW
        wave = math.sin(self._anim) * 4
        pygame.draw.circle(surface, col, (int(sx), int(sy)), int(camera.scale(self.RADIUS)))
        pygame.draw.line(surface, C_WHITE, (int(sx), int(sy)), (int(sx), int(sy - camera.scale(30))), 2)
        flag_pts = [(int(sx), int(sy - camera.scale(30))), (int(sx + camera.scale(16) + wave), int(sy - camera.scale(24))), (int(sx), int(sy - camera.scale(18)))]
        pygame.draw.polygon(surface, col, flag_pts)
