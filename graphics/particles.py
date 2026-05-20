"""Particle system for movement and impact feedback (arctic polish)."""
import pygame
import random
import math


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "colour", "size")

    def __init__(self, x, y, vx, vy, life, colour, size=3):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = life
        self.max_life = life
        self.colour = colour
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.13
        self.vx *= 0.97
        self.life -= 1

    @property
    def alive(self):
        return self.life > 0

    def draw(self, surface, cam_x, cam_y):
        ratio = self.life / self.max_life
        alpha = int(255 * ratio)
        r = max(1, int(self.size * ratio))
        sx = int(self.x - cam_x)
        sy = int(self.y - cam_y)
        s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, self.colour + (alpha,), (r, r), r)
        surface.blit(s, (sx - r, sy - r))


class ParticleSystem:
    def __init__(self):
        self._particles = []

    def emit_jump(self, x, y):
        for _ in range(12):
            a = random.uniform(math.pi, 2 * math.pi)
            sp = random.uniform(1.6, 4.0)
            self._particles.append(Particle(x, y, math.cos(a) * sp, math.sin(a) * sp, random.randint(14, 26), (205, 235, 255), random.randint(2, 4)))

    def emit_land(self, x, y):
        for _ in range(10):
            self._particles.append(Particle(x + random.uniform(-14, 14), y, random.uniform(-2.4, 2.4), random.uniform(-1.5, 0.2), random.randint(9, 18), (170, 220, 255), random.randint(2, 4)))

    def emit_death(self, x, y):
        for _ in range(36):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(2.0, 7.2)
            c = random.choice([(240, 245, 255), (180, 225, 255), (120, 180, 230)])
            self._particles.append(Particle(x, y, math.cos(a) * sp, math.sin(a) * sp, random.randint(24, 56), c, random.randint(3, 7)))

    def emit_goal(self, x, y):
        for _ in range(56):
            a = random.uniform(0, 2 * math.pi)
            sp = random.uniform(1.6, 6.1)
            c = random.choice([(170, 230, 255), (240, 255, 255), (120, 180, 235)])
            self._particles.append(Particle(x, y, math.cos(a) * sp, math.sin(a) * sp, random.randint(32, 66), c, random.randint(3, 8)))

    def emit_roll(self, x, y, vx):
        if random.random() > 0.35:
            return
        self._particles.append(Particle(x + random.uniform(-4, 4), y + 8, vx * 0.2 + random.uniform(-0.4, 0.4), random.uniform(-0.6, -0.05), random.randint(8, 14), (130, 190, 230), random.randint(2, 3)))

    def update(self):
        self._particles = [p for p in self._particles if p.alive]
        for p in self._particles:
            p.update()

    def draw(self, surface, cam_x, cam_y):
        for p in self._particles:
            p.draw(surface, cam_x, cam_y)
