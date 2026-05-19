import math
import random
from config import SCREEN_W, SCREEN_H, CAM_LERP, CAM_SHAKE_DECAY, CAM_ZOOM_LERP, CAM_ZOOM_DEFAULT


class Camera:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.zoom = CAM_ZOOM_DEFAULT
        self._tz = CAM_ZOOM_DEFAULT
        self._sx = 0.0
        self._sy = 0.0
        self._str = 0.0
        self.min_x = -math.inf
        self.max_x = math.inf
        self.min_y = -math.inf
        self.max_y = math.inf

    def set_bounds(self, min_x, max_x, min_y, max_y):
        self.min_x, self.max_x = min_x, max_x
        self.min_y, self.max_y = min_y, max_y

    def shake(self, strength):
        self._str = max(self._str, strength)

    def set_zoom(self, z):
        self._tz = z

    def snap_to(self, wx, wy):
        self.x, self.y = float(wx), float(wy)

    def update(self, dt, targets):
        if not targets:
            return
        if len(targets) == 1:
            tx, ty = targets[0]
        else:
            xs = [t[0] for t in targets]
            ys = [t[1] for t in targets]
            tx = (min(xs) + max(xs)) * 0.5
            ty = (min(ys) + max(ys)) * 0.5
            span_x = max(xs) - min(xs) + 300
            span_y = max(ys) - min(ys) + 200
            z = min(SCREEN_W / max(span_x, 1), SCREEN_H / max(span_y, 1))
            self._tz = max(0.5, min(1.0, z))

        alpha = 1.0 - math.exp(-CAM_LERP * dt)
        self.x += (tx - self.x) * alpha
        self.y += (ty - self.y) * alpha

        hw = (SCREEN_W * 0.5) / max(self.zoom, 1e-6)
        hh = (SCREEN_H * 0.5) / max(self.zoom, 1e-6)
        self.x = max(self.min_x + hw, min(self.max_x - hw, self.x))
        self.y = max(self.min_y + hh, min(self.max_y - hh, self.y))

        za = 1.0 - math.exp(-CAM_ZOOM_LERP * dt)
        self.zoom += (self._tz - self.zoom) * za

        if self._str > 0.5:
            angle = random.uniform(0, math.tau)
            self._sx = math.cos(angle) * self._str
            self._sy = math.sin(angle) * self._str
            self._str *= math.exp(-CAM_SHAKE_DECAY * dt)
        else:
            self._str = 0.0
            self._sx = self._sy = 0.0

    def world_to_screen(self, wx, wy):
        cx = (wx - self.x) * self.zoom + SCREEN_W * 0.5 + self._sx
        cy = (wy - self.y) * self.zoom + SCREEN_H * 0.5 + self._sy
        return cx, cy

    def screen_to_world(self, sx, sy):
        wx = (sx - SCREEN_W * 0.5 - self._sx) / self.zoom + self.x
        wy = (sy - SCREEN_H * 0.5 - self._sy) / self.zoom + self.y
        return wx, wy

    def scale(self, world_size):
        return world_size * self.zoom

    def rect_visible(self, wx, wy, w, h, margin=64):
        sx, sy = self.world_to_screen(wx, wy)
        return sx + w + margin > 0 and sx - margin < SCREEN_W and sy + h + margin > 0 and sy - margin < SCREEN_H
