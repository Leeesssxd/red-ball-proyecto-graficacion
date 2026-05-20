"""HUD and transient overlay (arctic style)."""
import pygame
import math
from config import SCREEN_W, SCREEN_H, C_HUD_TEXT, C_CYAN, C_GOAL, C_WHITE


class HUD:
    def __init__(self):
        pygame.font.init()
        self._font_big = pygame.font.SysFont("consolas", 24, bold=True)
        self._font_med = pygame.font.SysFont("consolas", 18)
        self._font_sm = pygame.font.SysFont("consolas", 14)
        self._elapsed = 0.0

    def update(self, dt):
        self._elapsed += dt

    def draw(self, surface, level_title, level_num, total_levels, player, timer_secs, coin_count, secret_unlocked):
        panel = pygame.Surface((560, 90), pygame.SRCALPHA)
        panel.fill((8, 18, 34, 178))
        pygame.draw.rect(panel, (130, 225, 255, 100), panel.get_rect(), 1)
        surface.blit(panel, (10, 10))

        lev = self._font_big.render(f"{level_num:02d}/{total_levels:02d} {level_title}", True, C_CYAN)
        surface.blit(lev, (18, 14))

        mins = int(timer_secs) // 60
        secs = int(timer_secs) % 60
        ms = int((timer_secs % 1) * 100)
        tim = self._font_med.render(f"TIME {mins:02d}:{secs:02d}.{ms:02d}", True, C_HUD_TEXT)
        surface.blit(tim, (18, 46))

        coin_txt = self._font_med.render(f"Relics: {coin_count}/3", True, (236, 246, 255))
        surface.blit(coin_txt, (240, 46))
        gate = "Secret Gate: OPEN" if secret_unlocked else "Secret Gate: LOCKED"
        gate_col = (150, 240, 255) if secret_unlocked else (220, 230, 255)
        gate_txt = self._font_sm.render(gate, True, gate_col)
        surface.blit(gate_txt, (420, 50))

        if self._elapsed < 8.0:
            alpha = int(255 * min(1.0, (8.0 - self._elapsed) / 1.8))
            hint = self._font_sm.render("MOVE: ARROWS / A,D   JUMP: SPACE   RESTART: R", True, (175, 220, 255))
            hint.set_alpha(alpha)
            surface.blit(hint, (16, SCREEN_H - 28))

    def draw_progress_bar(self, surface, px, level_w):
        bar_w = SCREEN_W - 40
        bar_h = 8
        bx, by = 20, 6
        frac = min(1.0, max(0.0, px / max(1, level_w)))
        fill = int(bar_w * frac)
        pygame.draw.rect(surface, (20, 38, 60), (bx, by, bar_w, bar_h), border_radius=4)
        if fill > 0:
            pygame.draw.rect(surface, (120, 220, 255), (bx, by, fill, bar_h), border_radius=4)
        pygame.draw.circle(surface, (220, 245, 255), (bx + fill, by + bar_h // 2), 5)
        pygame.draw.circle(surface, C_GOAL, (bx + bar_w, by + bar_h // 2), 5)


class MessageOverlay:
    def __init__(self):
        pygame.font.init()
        self._font_h = pygame.font.SysFont("impact", 72, bold=True)
        self._font_s = pygame.font.SysFont("consolas", 24)
        self._msg = ""
        self._sub = ""
        self._timer = 0.0
        self._dur = 0.0
        self._colour = C_WHITE

    def show(self, msg, sub="", duration=2.0, colour=None):
        if not msg and not sub:
            self.clear()
            return
        self._msg = msg
        self._sub = sub
        self._timer = duration
        self._dur = duration
        self._colour = colour or C_WHITE

    def clear(self):
        self._msg = ""
        self._sub = ""
        self._timer = 0.0
        self._dur = 0.0

    def update(self, dt):
        if self._timer > 0:
            self._timer -= dt

    @property
    def active(self):
        return self._timer > 0 and (self._msg or self._sub)

    def draw(self, surface):
        if not self.active:
            return
        t = self._dur - self._timer
        alpha = int(min(255, t * 360))
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((0, 8, 18, min(145, alpha)))
        surface.blit(dim, (0, 0))

        bounce = int(6 * math.sin(t * 4))
        h_surf = self._font_h.render(self._msg, True, self._colour)
        h_surf.set_alpha(alpha)
        hx = SCREEN_W // 2 - h_surf.get_width() // 2
        hy = SCREEN_H // 2 - h_surf.get_height() // 2 + bounce
        surface.blit(h_surf, (hx, hy))

        if self._sub:
            s_surf = self._font_s.render(self._sub, True, C_HUD_TEXT)
            s_surf.set_alpha(alpha)
            sx = SCREEN_W // 2 - s_surf.get_width() // 2
            sy = hy + h_surf.get_height() + 12
            surface.blit(s_surf, (sx, sy))
