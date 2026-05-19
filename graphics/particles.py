"""Particle system for movement and impact feedback."""
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
        self.vy += 0.16
        self.vx *= 0.96
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
        for _ in range(14):
            angle = random.uniform(math.pi, 2 * math.pi)
            speed = random.uniform(1.8, 4.4)
            self._particles.append(Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed, random.randint(14, 28), (200, 220, 255), random.randint(2, 5)))

    def emit_land(self, x, y):
        for _ in range(10):
            self._particles.append(Particle(x + random.uniform(-14, 14), y, random.uniform(-2.6, 2.6), random.uniform(-1.8, 0.4), random.randint(10, 18), (120, 190, 255), random.randint(2, 4)))

    def emit_death(self, x, y):
        for _ in range(42):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 8.5)
            self._particles.append(Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed, random.randint(24, 56), (230, 45, 60), random.randint(3, 8)))

    def emit_goal(self, x, y):
        for _ in range(68):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.8, 6.4)
            col = random.choice([(255, 220, 30), (255, 140, 0), (255, 255, 110)])
            self._particles.append(Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed, random.randint(35, 72), col, random.randint(3, 9)))

    def emit_roll(self, x, y, vx):
        if random.random() > 0.35:
            return
        self._particles.append(Particle(x + random.uniform(-4, 4), y + 8, vx * 0.2 + random.uniform(-0.5, 0.5), random.uniform(-0.8, 0.0), random.randint(8, 15), (65, 135, 210), random.randint(2, 4)))

    def update(self):
        self._particles = [p for p in self._particles if p.alive]
        for p in self._particles:
            p.update()

    def draw(self, surface, cam_x, cam_y):
        for p in self._particles:
            p.draw(surface, cam_x, cam_y)
