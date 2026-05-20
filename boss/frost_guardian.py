import math
import pygame


class FrostGuardian:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 120
        self.h = 92
        self.hp = 120
        self.max_hp = 120
        self.alive = True
        self._t = 0.0
        self._phase = 0
        self._projectiles = []
        self._hurt_flash = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x - self.w / 2), int(self.y - self.h), self.w, self.h)

    def update(self, dt, player):
        if not self.alive:
            return
        self._t += dt
        self._hurt_flash = max(0.0, self._hurt_flash - dt * 4)

        self.x += math.sin(self._t * 1.2) * 0.8

        if self._t > 1.0:
            self._t = 0.0
            vx = -3.2 if player.x < self.x else 3.2
            self._projectiles.append([self.x, self.y - 30, vx, -2.0])

        alive_proj = []
        for p in self._projectiles:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.11
            if p[1] < 1200:
                alive_proj.append(p)
        self._projectiles = alive_proj

    def resolve_hits(self, player):
        if not self.alive:
            return {"player_hit": False, "boss_hit": False, "boss_dead": False}

        out = {"player_hit": False, "boss_hit": False, "boss_dead": False}

        if player.rect.colliderect(self.rect):
            if player.vy > 0 and player.rect.bottom <= self.rect.top + 16:
                self.hp -= 20
                self._hurt_flash = 1.0
                player.vy = -12
                out["boss_hit"] = True
                if self.hp <= 0:
                    self.alive = False
                    out["boss_dead"] = True
            elif player.hurt_timer <= 0:
                player.hurt_timer = 0.7
                player.alive = player.alive
                out["player_hit"] = True

        for pr in self._projectiles:
            r = pygame.Rect(int(pr[0] - 8), int(pr[1] - 8), 16, 16)
            if player.rect.colliderect(r) and player.hurt_timer <= 0:
                player.hurt_timer = 0.7
                out["player_hit"] = True

        return out

    def draw(self, surface, cam):
        if not self.alive:
            return
        r = cam.apply(self.rect)
        base = (185, 230, 255)
        if self._hurt_flash > 0:
            base = (255, 180, 180)
        pygame.draw.rect(surface, (85, 120, 160), r.inflate(8, 10), border_radius=14)
        pygame.draw.rect(surface, base, r, border_radius=12)
        pygame.draw.rect(surface, (225, 246, 255), pygame.Rect(r.x + 14, r.y + 14, r.w - 28, r.h - 32), border_radius=8)
        pygame.draw.circle(surface, (15, 35, 55), (r.centerx - 18, r.y + 32), 4)
        pygame.draw.circle(surface, (15, 35, 55), (r.centerx + 18, r.y + 32), 4)
        pygame.draw.rect(surface, (20, 40, 60), pygame.Rect(r.centerx - 8, r.y + 43, 16, 8), border_radius=3)

        for pr in self._projectiles:
            sx, sy = cam.apply_xy(pr[0], pr[1])
            pygame.draw.circle(surface, (170, 240, 255), (int(sx), int(sy)), 8)
            pygame.draw.circle(surface, (240, 255, 255), (int(sx), int(sy)), 4)

        bw = 220
        bh = 12
        bx = 20
        by = 50
        pygame.draw.rect(surface, (25, 40, 60), (bx, by, bw, bh), border_radius=4)
        fill = int(bw * max(0.0, self.hp / self.max_hp))
        pygame.draw.rect(surface, (120, 230, 255), (bx, by, fill, bh), border_radius=4)
        pygame.draw.rect(surface, (220, 245, 255), (bx, by, bw, bh), 1, border_radius=4)
