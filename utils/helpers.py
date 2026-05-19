"""Misc helper functions."""
import pygame
import math


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp(val, lo, hi):
    return max(lo, min(hi, val))


def draw_circle_pseudo3d(surface, cx, cy, radius, colour, shine, shade, shadow_surf=None):
    """Draw a filled circle with fake 3-D shading."""
    # shadow
    if shadow_surf:
        sx, sy = cx - radius, cy + radius * 0.6
        shadow_surf.fill((0, 0, 0, 0))
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 90),
                            (0, 0, int(radius * 2.2), int(radius * 0.6)))
        surface.blit(shadow_surf,
                     (int(sx - radius * 0.1), int(sy - radius * 0.15)),
                     special_flags=pygame.BLEND_RGBA_MULT)

    # body
    pygame.draw.circle(surface, colour, (cx, cy), radius)

    # dark hemisphere (bottom-right)
    for i in range(max(1, radius // 4), 0, -1):
        a = int(80 * (1 - i / (radius // 4 + 1)))
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, shade + (a,), (radius, radius), radius - i)
        surface.blit(s, (cx - radius, cy - radius),
                     special_flags=pygame.BLEND_RGBA_SUB)

    # shine (top-left)
    shine_r = max(2, radius // 3)
    shine_x = cx - radius // 3
    shine_y = cy - radius // 3
    shine_s = pygame.Surface((shine_r * 2, shine_r * 2), pygame.SRCALPHA)
    pygame.draw.circle(shine_s, shine + (180,), (shine_r, shine_r), shine_r)
    surface.blit(shine_s, (shine_x - shine_r, shine_y - shine_r))


def draw_platform(surface, rect, top_col, side_col, thickness=10):
    """Draw a platform with a pseudo-3D side face."""
    # side face (bottom)
    side_rect = pygame.Rect(rect.x + thickness // 2,
                            rect.bottom - 2,
                            rect.width - thickness,
                            thickness)
    pygame.draw.rect(surface, side_col, side_rect, border_radius=3)
    # top face
    pygame.draw.rect(surface, top_col, rect, border_radius=5)
    # bright top edge
    pygame.draw.line(surface, (min(top_col[0] + 60, 255),
                                min(top_col[1] + 60, 255),
                                min(top_col[2] + 60, 255)),
                     (rect.x + 4, rect.y + 2),
                     (rect.right - 4, rect.y + 2), 2)


def pulse(t: float, speed: float = 3.0) -> float:
    """Return 0..1 sine pulse."""
    return (math.sin(t * speed) + 1) / 2
