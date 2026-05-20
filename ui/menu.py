"""Pantalla de título y pantalla de victoria — Garras Glaciares."""
import pygame
import math
from config import SCREEN_W, SCREEN_H, C_WHITE
from utils.helpers import pulse


def _load_font(size, bold=False):
    """Fuente pixel art / monospace limpia."""
    for name in ("Courier New", "Lucida Console", "Consolas", "monospace"):
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except Exception:
            pass
    return pygame.font.Font(None, size)


class TitleScreen:
    def __init__(self):
        pygame.font.init()
        self._font_title = _load_font(88, bold=True)
        self._font_sub   = _load_font(24)
        self._font_hint  = _load_font(19)
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface):
        # Fondo ártico oscuro (el background real se dibuja antes)
        # Aquí sólo renderizamos el overlay de texto sobre el fondo de Background
        # Si el background no está disponible, pintamos nuestro fondo
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((4, 10, 22, 160))   # Capa semi-transparente sobre el fondo real
        surface.blit(overlay, (0, 0))

        # Título
        y = SCREEN_H // 2 - 190 + int(7 * math.sin(self._t * 2.0))

        # Sombra
        title_shadow = self._font_title.render("GARRAS GLACIARES", True, (14, 32, 50))
        title_surf   = self._font_title.render("GARRAS GLACIARES", True, (210, 245, 255))
        tx = SCREEN_W // 2 - title_surf.get_width() // 2

        # Resplandor suave
        glow = pygame.Surface((title_surf.get_width() + 60, title_surf.get_height() + 36), pygame.SRCALPHA)
        glow_alpha = int(38 + 18 * math.sin(self._t * 1.8))
        pygame.draw.ellipse(glow, (120, 200, 255, glow_alpha), glow.get_rect())
        surface.blit(glow, (tx - 30, y - 10))
        surface.blit(title_shadow, (tx + 5, y + 7))
        surface.blit(title_surf,   (tx, y))

        # Subtítulo
        sub = self._font_sub.render("Aventura Indie de Oso Polar", True, (145, 215, 255))
        surface.blit(sub, (SCREEN_W // 2 - sub.get_width() // 2, y + 108))

        # Pulsante "Presionar tecla"
        alpha = int(175 + 80 * pulse(self._t, 1.7))
        hint  = self._font_hint.render("Presiona ENTER para comenzar la expedición", True, C_WHITE)
        hint.set_alpha(alpha)
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 56))

        # Controles
        ctrl = self._font_hint.render("← → / A,D Mover     Espacio Saltar     R Reiniciar", True, (145, 206, 240))
        surface.blit(ctrl, (SCREEN_W // 2 - ctrl.get_width() // 2, SCREEN_H - 42))

    def handle_event(self, event):
        return event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE
        )


class WinScreen:
    def __init__(self):
        pygame.font.init()
        self._font_big = _load_font(76, bold=True)
        self._font_sm  = _load_font(22)
        self._t = 0.0

    def update(self, dt):
        self._t += dt

    def draw(self, surface, time_str="", coin_count=0, secret_open=False):
        dim = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        dim.fill((4, 14, 26, 205))
        surface.blit(dim, (0, 0))

        col = (200, int(208 + 47 * pulse(self._t, 2.1)), 255)
        txt = self._font_big.render("EXPEDICIÓN COMPLETADA", True, col)
        tx  = SCREEN_W // 2 - txt.get_width() // 2
        ty  = SCREEN_H // 2 - 130
        surface.blit(txt, (tx, ty))

        if time_str:
            ts = self._font_sm.render(f"Tiempo: {time_str}", True, (220, 240, 255))
            surface.blit(ts, (SCREEN_W // 2 - ts.get_width() // 2, ty + 105))

        rel = self._font_sm.render(f"Reliquias: {coin_count}/3", True, (220, 240, 255))
        surface.blit(rel, (SCREEN_W // 2 - rel.get_width() // 2, ty + 140))

        sec     = "Secreto Completado ✦" if secret_open else "Secreto Bloqueado ◈"
        sec_col = (120, 245, 215) if secret_open else (200, 215, 230)
        ss      = self._font_sm.render(sec, True, sec_col)
        surface.blit(ss, (SCREEN_W // 2 - ss.get_width() // 2, ty + 175))

        hint = self._font_sm.render("ENTER Reiniciar   ESC Salir", True, (130, 200, 240))
        surface.blit(hint, (SCREEN_W // 2 - hint.get_width() // 2, SCREEN_H // 2 + 100))

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return ""
        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return "restart"
        if event.key == pygame.K_ESCAPE:
            return "quit"
        return ""
