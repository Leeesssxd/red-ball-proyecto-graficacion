"""Simple 2-D vector helper."""
import math


class Vec2:
    __slots__ = ("x", "y")

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    # ── arithmetic ──────────────────────────────────────────
    def __add__(self, o):  return Vec2(self.x + o.x, self.y + o.y)
    def __sub__(self, o):  return Vec2(self.x - o.x, self.y - o.y)
    def __mul__(self, s):  return Vec2(self.x * s,   self.y * s)
    def __rmul__(self, s): return self.__mul__(s)
    def __truediv__(self, s): return Vec2(self.x / s, self.y / s)
    def __neg__(self):     return Vec2(-self.x, -self.y)
    def __repr__(self):    return f"Vec2({self.x:.2f}, {self.y:.2f})"

    def copy(self): return Vec2(self.x, self.y)

    def length(self): return math.hypot(self.x, self.y)

    def normalise(self):
        n = self.length()
        return Vec2(self.x / n, self.y / n) if n else Vec2()

    def lerp(self, target, t):
        return Vec2(self.x + (target.x - self.x) * t,
                    self.y + (target.y - self.y) * t)

    def as_tuple(self): return (self.x, self.y)
    def as_int(self):   return (int(self.x), int(self.y))
