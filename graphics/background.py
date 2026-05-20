"""Gestor de fondos con imágenes reales para cada nivel (sin sci-fi, sin grids)."""
import os
import pygame
import random

from config import SCREEN_W, SCREEN_H

# Directorio de fondos relativo al archivo actual
_BG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "backgrounds")


def _find_bg(name_stem):
    """Busca el archivo de fondo por stem de nombre (sin extensión), case-insensitive.
    Prioriza formatos soportados: PNG > JPG > WEBP > (evita AVIF sin soporte).
    """
    if not os.path.isdir(_BG_DIR):
        return None
    # Prioridad de extensiones soportadas por pygame/SDL
    PRIORITY = [".png", ".jpg", ".jpeg", ".webp", ".bmp"]
    candidates = []
    for f in os.listdir(_BG_DIR):
        stem = os.path.splitext(f)[0].lower().replace(" ", "")
        ext  = os.path.splitext(f)[1].lower()
        if stem == name_stem.lower().replace(" ", ""):
            candidates.append((f, ext))
    # Ordenar por prioridad de extensión
    def _prio(item):
        ext = item[1]
        return PRIORITY.index(ext) if ext in PRIORITY else 99
    candidates.sort(key=_prio)
    if candidates:
        return os.path.join(_BG_DIR, candidates[0][0])
    return None


# Mapeo theme → archivo de imagen real
_THEME_FILES = {
    "tundra_day":   _find_bg("1Nivel"),
    "forest_blue":  _find_bg("2Nivel"),
    "dusk_violet":  _find_bg("3nivel"),
    "sunset_ice":   _find_bg("4Nivel"),
    "final_image":  _find_bg("nivel_final"),
    "secret_image": _find_bg("nivel_final_secreto"),
}


class Background:
    def __init__(self):
        self._cache = {}
        self._theme = None
        # Copos de nieve: [x, y, velocidad_y, opacidad]
        self._snow = [
            [random.uniform(0, SCREEN_W),
             random.uniform(0, SCREEN_H),
             random.uniform(14, 52),
             random.uniform(0.25, 1.0)]
            for _ in range(110)
        ]

    def set_theme(self, theme):
        if self._theme != theme:
            self._theme = theme
            if theme not in self._cache:
                self._cache[theme] = self._build_theme(theme)

    # ------------------------------------------------------------------
    # Carga y escala inteligente de imagen
    # ------------------------------------------------------------------
    def _load_and_fit(self, path):
        """
        Carga imagen y la escala al tamaño de pantalla con letterbox/cover.
        Usa smoothscale para calidad. No deforma el pixel art: hace cover-fit.
        """
        img = pygame.image.load(path).convert()
        iw, ih = img.get_size()

        # Recorte mínimo inferior (strip de ruido/watermark)
        crop_h = max(1, int(ih * 0.97))
        img = img.subsurface(pygame.Rect(0, 0, iw, crop_h)).copy()
        iw, ih = img.get_size()

        # Estrategia cover-fit: escalar al mínimo que llena la pantalla entera
        scale = max(SCREEN_W / iw, SCREEN_H / ih)
        new_w = int(iw * scale)
        new_h = int(ih * scale)

        # Para imágenes pequeñas (pixel art) usar scale normal, no smooth
        if iw < 400 or ih < 300:
            scaled = pygame.transform.scale(img, (new_w, new_h))
        else:
            scaled = pygame.transform.smoothscale(img, (new_w, new_h))

        # Centrar y recortar al tamaño exacto de pantalla
        canvas = pygame.Surface((SCREEN_W, SCREEN_H))
        ox = (new_w - SCREEN_W) // 2
        oy = (new_h - SCREEN_H) // 2
        canvas.blit(scaled, (-ox, -oy))
        return canvas

    # ------------------------------------------------------------------
    # Paletas de respaldo (solo si la imagen no existe)
    # ------------------------------------------------------------------
    _FALLBACK_PALETTES = {
        "tundra_day":  ((154, 210, 248), (220, 243, 255), (82, 126, 170),  (34, 66, 102)),
        "forest_blue": ((72,  150, 208), (180, 228, 248), (58, 110, 150),  (20, 52, 90)),
        "dusk_violet": ((170, 126, 178), (244, 202, 220), (106, 72, 120),  (52, 36, 62)),
        "sunset_ice":  ((40,  132, 194), (255, 180, 120), (72,  86, 160),  (24, 36, 90)),
        "final_image": ((20,  60,  110), (100, 180, 255), (10,  40,  80),  (5,  20, 50)),
        "secret_image":((60,  20,  90),  (200, 140, 255), (40,  10,  70),  (20, 5,  40)),
    }

    def _build_fallback(self, theme):
        """Gradiente ártico de respaldo (sin grids ni sci-fi)."""
        surf = pygame.Surface((SCREEN_W, SCREEN_H))
        top, sun, m1, m2 = self._FALLBACK_PALETTES.get(theme, self._FALLBACK_PALETTES["tundra_day"])

        for y in range(SCREEN_H):
            t = y / SCREEN_H
            r = int(top[0] * (1 - t) + 12 * t)
            g = int(top[1] * (1 - t) + 30 * t)
            b = int(top[2] * (1 - t) + 60 * t)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W, y))

        pygame.draw.circle(surf, sun, (SCREEN_W - 220, 140), 74)

        pts_far  = [(0,380),(180,290),(360,360),(520,250),(700,340),(900,240),(1120,360),(1280,300),(1280,720),(0,720)]
        pts_near = [(0,470),(140,360),(280,430),(430,320),(620,455),(820,340),(1030,470),(1240,360),(1280,410),(1280,720),(0,720)]
        pygame.draw.polygon(surf, m1, pts_far)
        pygame.draw.polygon(surf, m2, pts_near)

        for x in range(0, SCREEN_W, 28):
            h = random.randint(24, 70)
            pygame.draw.polygon(surf, (26, 44, 58),
                                [(x, SCREEN_H-80),(x+12, SCREEN_H-80-h),(x+24, SCREEN_H-80)])
        return surf

    def _build_theme(self, theme):
        path = _THEME_FILES.get(theme)
        if path and os.path.isfile(path):
            try:
                return self._load_and_fit(path)
            except Exception:
                pass
        return self._build_fallback(theme)

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------
    def draw(self, surface, cam_x, cam_y, t):
        if self._theme is None:
            self.set_theme("tundra_day")
        base = self._cache[self._theme]
        surface.blit(base, (0, 0))

        # Nieve suave
        snow_layer = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        for fl in self._snow:
            fl[1] += fl[2] * fl[3] * (1 / 60)
            fl[0] += fl[3] * 0.22
            if fl[1] > SCREEN_H + 5:
                fl[1] = -5
                fl[0] = random.uniform(0, SCREEN_W)
            if fl[0] > SCREEN_W + 2:
                fl[0] = -2
            r = 1 if fl[3] < 0.75 else 2
            alpha = int(140 + fl[3] * 80)
            pygame.draw.circle(snow_layer, (235, 247, 255, alpha),
                               (int(fl[0]), int(fl[1])), r)
        surface.blit(snow_layer, (0, 0))
