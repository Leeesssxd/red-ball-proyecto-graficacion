import math
import random
import pygame
from config import MAX_PARTICLES


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "lifetime", "max_life", "size", "gravity", "fade", "shrink")

    def __init__(self):
        self.x = self.y = 0.0
        self.vx = self.vy = 0.0
        self.color = (255, 255, 255)
        self.lifetime = 0.0
        self.max_life = 1.0
        self.size = 4.0
        self.gravity = 200.0
        self.fade = True
        self.shrink = True


class ParticleSystem:
    def __init__(self):
        self._pool = [Particle() for _ in range(MAX_PARTICLES)]
        self._active = []
        self._pool_idx = 0

    def _get(self):
        if len(self._active) >= MAX_PARTICLES:
            return None
        p = self._pool[self._pool_idx % MAX_PARTICLES]
        self._pool_idx += 1
        return p

    def spawn(self, x, y, color=(255, 255, 255), speed_range=(50, 150), angle_range=(0, 360), lifetime=0.6, size=4, gravity=200.0, count=1, fade=True, shrink=True):
        for _ in range(count):
            p = self._get()
            if p is None:
                break
            angle = math.radians(random.uniform(*angle_range))
            speed = random.uniform(*speed_range)
            p.x = x + random.uniform(-2, 2)
            p.y = y + random.uniform(-2, 2)
            p.vx = math.cos(angle) * speed
            p.vy = math.sin(angle) * speed
            p.color = color
            p.lifetime = lifetime * random.uniform(0.7, 1.3)
            p.max_life = p.lifetime
            p.size = float(size) * random.uniform(0.6, 1.4)
            p.gravity = gravity
            p.fade = fade
            p.shrink = shrink
            if p not in self._active:
                self._active.append(p)

    def spawn_burst(self, x, y, color, n=20, **kwargs):
        self.spawn(x, y, color=color, count=n, **kwargs)

    def update(self, dt):
        dead = []
        for p in self._active:
            p.vy += p.gravity * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.vx *= (1.0 - 2.0 * dt)
            p.lifetime -= dt
            if p.lifetime <= 0:
                dead.append(p)
        for p in dead:
            self._active.remove(p)

    def draw(self, surface, camera):
        for p in self._active:
            t = p.lifetime / max(p.max_life, 1e-6)
            alpha = int(255 * t) if p.fade else 255
            size = max(1, int(p.size * t)) if p.shrink else max(1, int(p.size))
            sx, sy = camera.world_to_screen(p.x, p.y)
            sx, sy = int(sx), int(sy)
            if not (0 <= sx < 1300 and 0 <= sy < 760):
                continue
            r, g, b = p.color[:3]
            tmp = pygame.Surface((size * 2 + 2, size * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(tmp, (r, g, b, alpha), (size + 1, size + 1), size)
            surface.blit(tmp, (sx - size - 1, sy - size - 1))

    def clear(self):
        self._active.clear()


def explosion_burst(ps, x, y, color=(255, 140, 30)):
    ps.spawn(x, y, color=color, count=25, speed_range=(80, 300), angle_range=(0, 360), lifetime=0.6, size=6, gravity=150)
    ps.spawn(x, y, color=(255, 255, 200), count=15, speed_range=(40, 140), angle_range=(0, 360), lifetime=0.4, size=3, gravity=60)


def land_dust(ps, x, y, color=(180, 180, 200)):
    ps.spawn(x, y, color=color, count=10, speed_range=(30, 100), angle_range=(190, 350), lifetime=0.35, size=3, gravity=80)


def speed_trail(ps, x, y, color):
    ps.spawn(x, y, color=color, count=2, speed_range=(5, 20), angle_range=(150, 210), lifetime=0.2, size=3, gravity=0, fade=True, shrink=True)
