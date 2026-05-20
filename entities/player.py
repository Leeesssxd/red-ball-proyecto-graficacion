"""Player controller with polar bear animation on top of existing physics."""
import pygame
import math
from config import (GRAVITY, JUMP_FORCE, MAX_FALL, FRICTION,
                    AIR_FRICTION, ACCEL, MAX_SPEED)
from utils.helpers import clamp
from player.polar_bear_sprite import PolarBearSpriteSet


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
        self.hurt_timer = 0.0
        self.death_timer = 0.0
        self._roll_angle = 0.0
        self._coyote = 0
        self._jump_buf = 0
        self._anim_t = 0.0
        self._sprites = PolarBearSpriteSet(scale=3)
        self._facing = 1

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
            self._facing = 1
        elif left:
            self.vx = clamp(self.vx - ACCEL, -MAX_SPEED, MAX_SPEED)
            self._facing = -1
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
            self.death_timer += 1 / 60
            return
        self.was_ground = self.on_ground
        self.on_ground = False
        if self._coyote > 0:
            self._coyote -= 1
        self.x += self.vx
        self.y += self.vy
        self._roll_angle += self.vx * 4.0
        self.hurt_timer = max(0.0, self.hurt_timer - 1 / 60)
        self._anim_t += 1 / 60

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
        eps = 0.001

        if overlap_x + eps < overlap_y:
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

    def _state(self):
        if not self.alive:
            return "death"
        if self.hurt_timer > 0:
            return "hurt"
        if self.won:
            return "win"
        if not self.on_ground and self.vy < -1.2:
            return "jump"
        if not self.on_ground and self.vy >= -1.2:
            return "fall"
        if abs(self.vx) > 0.7:
            return "walk"
        return "idle"

    def draw(self, surface: pygame.Surface, cam):
        sx, sy = cam.apply_xy(self.x, self.y)
        sx, sy = int(sx), int(sy)

        speed_ratio = min(1.0, abs(self.vx) / 9.0)
        sh_w = int(self.RADIUS * (2.3 + speed_ratio * 0.4))
        shadow = pygame.Surface((sh_w, int(self.RADIUS * 0.6)), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 75), shadow.get_rect())
        surface.blit(shadow, (sx - sh_w // 2, sy + self.RADIUS - 5))

        state = self._state()
        frame = self._sprites.frame(state, self._anim_t)
        if self._facing < 0:
            frame = pygame.transform.flip(frame, True, False)

        fx = sx - frame.get_width() // 2
        fy = sy - frame.get_height() // 2 + 2

        if self.hurt_timer > 0 and int(self.hurt_timer * 20) % 2 == 0:
            tint = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            tint.fill((255, 180, 180, 80))
            frame = frame.copy()
            frame.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        surface.blit(frame, (fx, fy))

    @property
    def speed(self):
        return math.hypot(self.vx, self.vy)
