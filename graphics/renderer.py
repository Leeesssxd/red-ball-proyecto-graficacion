import math
import pygame
from config import SCREEN_W, SCREEN_H, C_BG, C_GRID, PARALLAX_FACTORS, NEON_PALETTE


class BackgroundRenderer:
    def __init__(self):
        self._t = 0.0
        import random
        self._stars = [(random.randint(0, SCREEN_W * 4), random.randint(0, SCREEN_H * 3), random.uniform(0.5, 2.5)) for _ in range(120)]
        self._orbs = [{"x": random.randint(0, SCREEN_W * 4), "y": random.randint(0, SCREEN_H * 2), "r": random.randint(20, 60), "col": NEON_PALETTE[i % len(NEON_PALETTE)], "phase": random.uniform(0, math.tau)} for i in range(18)]

    def update(self, dt):
        self._t += dt

    def draw(self, surface, camera):
        surface.fill(C_BG)
        self._draw_grid(surface, camera)
        self._draw_stars(surface, camera)
        self._draw_orbs(surface, camera)

    def _draw_grid(self, surface, camera):
        factor = PARALLAX_FACTORS[0]
        cell = 80
        off_x = -(camera.x * factor) % cell
        off_y = -(camera.y * factor) % cell

        for gx in range(-1, SCREEN_W // cell + 2):
            sx = int(off_x + gx * cell)
            pygame.draw.line(surface, C_GRID, (sx, 0), (sx, SCREEN_H), 1)
        for gy in range(-1, SCREEN_H // cell + 2):
            sy = int(off_y + gy * cell)
            pygame.draw.line(surface, C_GRID, (0, sy), (SCREEN_W, sy), 1)

        hor_y = int(SCREEN_H * 0.62 - camera.y * 0.06)
        for i in range(3):
            s = pygame.Surface((SCREEN_W, 2 + i * 3), pygame.SRCALPHA)
            s.fill((30, 50, 120, max(0, 20 - i * 5)))
            surface.blit(s, (0, hor_y + i * 2))

    def _draw_stars(self, surface, camera):
        factor = PARALLAX_FACTORS[0] * 0.5
        for (wx, wy, sz) in self._stars:
            sx = (wx - camera.x * factor) % SCREEN_W
            sy = (wy - camera.y * factor) % SCREEN_H
            brightness = int(120 + 80 * math.sin(self._t + wx * 0.01))
            pygame.draw.circle(surface, (brightness, brightness, min(255, brightness + 40)), (int(sx), int(sy)), int(sz))

    def _draw_orbs(self, surface, camera):
        factor = PARALLAX_FACTORS[1]
        for o in self._orbs:
            wx = o["x"]
            wy = o["y"] + math.sin(self._t * 0.4 + o["phase"]) * 15
            sx = (wx - camera.x * factor) % (SCREEN_W + 120) - 60
            sy = (wy - camera.y * factor) % (SCREEN_H + 120) - 60
            r, g, b = o["col"]
            orb_surf = pygame.Surface((o["r"] * 2 + 2, o["r"] * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(orb_surf, (r, g, b, 18), (o["r"] + 1, o["r"] + 1), o["r"])
            pygame.draw.circle(orb_surf, (r, g, b, 30), (o["r"] + 1, o["r"] + 1), o["r"] // 2)
            surface.blit(orb_surf, (int(sx) - o["r"] - 1, int(sy) - o["r"] - 1))


def draw_glow(surface, x, y, radius, color, alpha=60, rings=3):
    for i in range(rings):
        r = radius + i * 8
        a = max(0, alpha - i * 18)
        tmp = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
        pygame.draw.circle(tmp, (*color[:3], a), (r + 1, r + 1), r)
        surface.blit(tmp, (int(x) - r - 1, int(y) - r - 1))


class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 100), size=22, lifetime=1.2):
        self.x, self.y = float(x), float(y)
        self.text = text
        self.color = color
        self.lifetime = lifetime
        self.max_life = lifetime
        self._vy = -60.0
        self._font = pygame.font.SysFont("consolas", size, bold=True)

    def update(self, dt):
        self.lifetime -= dt
        self.y += self._vy * dt
        self._vy *= 0.92

    def draw(self, surface, camera):
        if self.lifetime <= 0:
            return
        t = self.lifetime / self.max_life
        alpha = int(255 * t)
        sx, sy = camera.world_to_screen(self.x, self.y)
        img = self._font.render(self.text, True, self.color)
        img.set_alpha(alpha)
        surface.blit(img, img.get_rect(center=(int(sx), int(sy))))

    @property
    def dead(self):
        return self.lifetime <= 0


class FloatingTextManager:
    def __init__(self):
        self._items = []

    def add(self, x, y, text, **kwargs):
        self._items.append(FloatingText(x, y, text, **kwargs))

    def update(self, dt):
        for item in self._items:
            item.update(dt)
        self._items = [i for i in self._items if not i.dead]

    def draw(self, surface, camera):
        for item in self._items:
            item.draw(surface, camera)
