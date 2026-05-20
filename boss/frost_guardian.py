import math
import pygame


class FrostGuardian:
    def __init__(self, x, y, tier="mini"):
        self.x = float(x)
        self.y = float(y)
        self.tier = tier

        cfg = {
            "mini": {"hp": 70, "fire": 1.4, "proj": 1, "speed": 2.2, "size": (104, 80)},
            "mini_hard": {"hp": 90, "fire": 1.1, "proj": 2, "speed": 2.8, "size": (108, 84)},
            "final": {"hp": 140, "fire": 0.95, "proj": 2, "speed": 3.0, "size": (124, 96)},
            "secret": {"hp": 190, "fire": 0.72, "proj": 3, "speed": 3.8, "size": (132, 102)},
        }[tier]

        self.w, self.h = cfg["size"]
        self.hp = cfg["hp"]
        self.max_hp = cfg["hp"]
        self.fire_cd = cfg["fire"]
        self.proj_count = cfg["proj"]
        self.proj_speed = cfg["speed"]

        self.alive = True
        self._timer = 0.0
        self._wave_t = 0.0
        self._projectiles = []
        self._hurt_flash = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w / 2), int(self.y - self.h), self.w, self.h)

    def update(self, dt, player):
        if not self.alive:
            return
        self._timer += dt
        self._wave_t += dt
        self._hurt_flash = max(0.0, self._hurt_flash - dt * 4)

        self.x += math.sin(self._wave_t * 1.2) * 0.9

        if self._timer >= self.fire_cd:
            self._timer = 0.0
            direction = -1 if player.x < self.x else 1
            spread = 0.45
            n = self.proj_count
            for i in range(n):
                off = (i - (n - 1) / 2.0) * spread
                self._projectiles.append([self.x, self.y - 36, direction * self.proj_speed + off, -2.2 - abs(off) * 0.8])

        keep = []
        for p in self._projectiles:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.115
            if p[1] < 1200:
                keep.append(p)
        self._projectiles = keep

    def resolve_hits(self, player):
        if not self.alive:
            return {"player_hit": False, "boss_hit": False, "boss_dead": False}

        out = {"player_hit": False, "boss_hit": False, "boss_dead": False}

        if player.rect.colliderect(self.rect):
            if player.vy > 0 and player.rect.bottom <= self.rect.top + 18:
                self.hp -= 18 if self.tier in ("final", "secret") else 24
                self._hurt_flash = 1.0
                player.vy = -12.5
                out["boss_hit"] = True
                if self.hp <= 0:
                    self.alive = False
                    out["boss_dead"] = True
            elif player.hurt_timer <= 0:
                player.hurt_timer = 0.68
                out["player_hit"] = True

        for pr in self._projectiles:
            r = pygame.Rect(int(pr[0] - 8), int(pr[1] - 8), 16, 16)
            if player.rect.colliderect(r) and player.hurt_timer <= 0:
                player.hurt_timer = 0.68
                out["player_hit"] = True

        return out

    def draw(self, surface, cam):
        if not self.alive:
            return
        r = cam.apply(self.rect)
        base = (192, 235, 255)
        if self._hurt_flash > 0:
            base = (255, 188, 188)
        pygame.draw.rect(surface, (80, 118, 154), r.inflate(8, 10), border_radius=15)
        pygame.draw.rect(surface, base, r, border_radius=13)
        pygame.draw.rect(surface, (230, 248, 255), pygame.Rect(r.x + 14, r.y + 14, r.w - 28, r.h - 35), border_radius=8)
        pygame.draw.circle(surface, (14, 34, 50), (r.centerx - 18, r.y + 34), 4)
        pygame.draw.circle(surface, (14, 34, 50), (r.centerx + 18, r.y + 34), 4)
        pygame.draw.rect(surface, (20, 40, 60), pygame.Rect(r.centerx - 9, r.y + 46, 18, 8), border_radius=3)

        for pr in self._projectiles:
            sx, sy = cam.apply_xy(pr[0], pr[1])
            pygame.draw.circle(surface, (166, 236, 255), (int(sx), int(sy)), 8)
            pygame.draw.circle(surface, (240, 255, 255), (int(sx), int(sy)), 4)

        bw = 240
        bh = 11
        bx = 20
        by = 52
        pygame.draw.rect(surface, (24, 38, 56), (bx, by, bw, bh), border_radius=4)
        fill = int(bw * max(0.0, self.hp / self.max_hp))
        bar_col = (120, 232, 255) if self.tier != "secret" else (255, 170, 220)
        pygame.draw.rect(surface, bar_col, (bx, by, fill, bh), border_radius=4)
        pygame.draw.rect(surface, (225, 245, 255), (bx, by, bw, bh), 1, border_radius=4)
