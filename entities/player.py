"""Player – the rolling red ball."""
import pygame
import math
from config import (GRAVITY, JUMP_FORCE, MAX_FALL, FRICTION,
                    AIR_FRICTION, ACCEL, MAX_SPEED,
                    C_BALL, C_BALL_SHINE)
from utils.helpers import clamp


class Player:
    RADIUS = 22

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.was_ground = False
        self.alive = True
        self.won = False
        self._roll_angle = 0.0
        self._coyote = 0
        self._jump_buf = 0

    @property
    def rect(self) -> pygame.Rect:
        r = self.RADIUS
        return pygame.Rect(int(self.x) - r, int(self.y) - r, r * 2, r * 2)

    def handle_input(self, keys):
        if not self.alive or self.won:
            return
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        jump = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]

        if right:
            self.vx = clamp(self.vx + ACCEL, -MAX_SPEED, MAX_SPEED)
        elif left:
            self.vx = clamp(self.vx - ACCEL, -MAX_SPEED, MAX_SPEED)
        else:
            self.vx *= FRICTION if self.on_ground else AIR_FRICTION
            if abs(self.vx) < 0.03:
                self.vx = 0.0

        if jump:
            self._jump_buf = 7
        if self._jump_buf > 0:
            self._jump_buf -= 1
            if self._coyote > 0:
                self.vy = JUMP_FORCE
                self._coyote = 0
                self._jump_buf = 0

    def apply_gravity(self):
        if self.alive:
            self.vy = min(self.vy + GRAVITY, MAX_FALL)

    def move(self):
        if not self.alive:
            return
        self.was_ground = self.on_ground
        self.on_ground = False
        if self._coyote > 0:
            self._coyote -= 1
        self.x += self.vx
        self.y += self.vy
        self._roll_angle += self.vx * 4.0

    def resolve_platform(self, platform):
        if not self.alive or platform.gone:
            return False
        pr = self.rect
        plr = platform.rect
        if not pr.colliderect(plr):
            return False

        dx = pr.centerx - plr.centerx
        dy = pr.centery - plr.centery
        overlap_x = (pr.width * 0.5 + plr.width * 0.5) - abs(dx)
        overlap_y = (pr.height * 0.5 + plr.height * 0.5) - abs(dy)

        if overlap_x < overlap_y:
            self.x += overlap_x if dx > 0 else -overlap_x
            self.vx = 0
            return True

        if dy < 0:
            self.y -= overlap_y
            if self.vy > 0:
                self.vy = 0
            self.on_ground = True
            self._coyote = 8
            if platform.kind == "crumble":
                platform.trigger_crumble()
        else:
            self.y += overlap_y
            if self.vy < 0:
                self.vy = 0
        return True

    def resolve_spike(self, spike):
        if self.alive and self.rect.colliderect(spike.rect):
            self.alive = False

    def resolve_bounce_pad(self, pad):
        if not self.alive:
            return False
        if self.rect.colliderect(pad.rect) and self.vy >= 0 and self.rect.bottom <= pad.rect.bottom + 16:
            self.vy = pad.boost
            self.y = min(self.y, pad.rect.top - self.RADIUS)
            pad.trigger()
            return True
        return False

    def resolve_goal(self, goal):
        if not self.alive or self.won or goal.collected:
            return False
        if self.rect.colliderect(goal.rect):
            self.won = True
            goal.collected = True
            return True
        return False

    def draw(self, surface: pygame.Surface, cam):
        if not self.alive:
            return
        sx, sy = cam.apply_xy(self.x, self.y)
        sx, sy = int(sx), int(sy)

        speed_ratio = min(1.0, abs(self.vx) / 9.0)
        sh_w = int(self.RADIUS * (2.3 + speed_ratio * 0.4))
        shadow = pygame.Surface((sh_w, int(self.RADIUS * 0.6)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 75), shadow.get_rect())
        surface.blit(shadow, (sx - sh_w // 2, sy + self.RADIUS - 5))

        rot_s = pygame.Surface((self.RADIUS * 2 + 6, self.RADIUS * 2 + 6), pygame.SRCALPHA)
        cx = rot_s.get_width() // 2
        cy = rot_s.get_height() // 2
        pygame.draw.circle(rot_s, C_BALL, (cx, cy), self.RADIUS)

        for offset in (-self.RADIUS // 2, 0, self.RADIUS // 2):
            a = math.radians(self._roll_angle + offset * 8)
            px = cx + int(math.cos(a) * self.RADIUS * 0.45)
            py = cy + int(math.sin(a) * self.RADIUS * 0.45)
            pygame.draw.circle(rot_s, (160, 14, 24, 120), (px, py), max(4, self.RADIUS // 4))

        shine_r = self.RADIUS // 3
        pygame.draw.circle(rot_s, C_BALL_SHINE + (205,), (cx - self.RADIUS // 3, cy - self.RADIUS // 3), shine_r)
        pygame.draw.circle(rot_s, (255, 255, 255, 70), (cx - 4, cy + 4), self.RADIUS, 2)

        surface.blit(rot_s, (sx - cx, sy - cy))
