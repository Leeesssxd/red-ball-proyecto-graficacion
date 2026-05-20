import os
import pygame


class PolarBearSpriteSet:
    STATES = ["idle", "walk", "jump", "fall", "hurt", "death", "win"]

    def __init__(self, scale=3):
        self.scale = scale
        self.frame_w = 16
        self.frame_h = 16
        self.anim_fps = {
            "idle": 4,
            "walk": 10,
            "jump": 1,
            "fall": 1,
            "hurt": 8,
            "death": 6,
            "win": 5,
        }
        self.frames = {s: [] for s in self.STATES}
        self._load_or_build_sheet()

    def _sheet_path(self):
        return os.path.join("assets", "sprites", "player", "polar_bear_sheet.png")

    def _load_or_build_sheet(self):
        path = self._sheet_path()
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            self._build_placeholder_sheet(path)
        sheet = pygame.image.load(path).convert_alpha()
        for i, st in enumerate(self.STATES):
            row = []
            for f in range(4):
                r = pygame.Rect(f * self.frame_w, i * self.frame_h, self.frame_w, self.frame_h)
                frame = pygame.Surface((self.frame_w, self.frame_h), pygame.SRCALPHA)
                frame.blit(sheet, (0, 0), r)
                row.append(pygame.transform.scale(frame, (self.frame_w * self.scale, self.frame_h * self.scale)))
            self.frames[st] = row

    def _build_placeholder_sheet(self, path):
        pygame.init()
        s = pygame.Surface((self.frame_w * 4, self.frame_h * len(self.STATES)), pygame.SRCALPHA)

        def px(surf, x, y, c):
            surf.fill(c, pygame.Rect(x, y, 1, 1))

        white = (238, 246, 255, 255)
        dark = (130, 160, 180, 255)
        nose = (20, 30, 40, 255)
        blush = (200, 220, 235, 255)
        ice = (180, 240, 255, 255)

        for row, st in enumerate(self.STATES):
            for f in range(4):
                ox = f * self.frame_w
                oy = row * self.frame_h
                bob = 1 if (st == "walk" and f % 2) else 0
                for y in range(6, 14):
                    for x in range(3, 13):
                        if (x in (3, 12) and y < 9) or (y == 6 and x in (3, 4, 11, 12)):
                            continue
                        px(s, ox + x, oy + y - bob, white)
                for x in (4, 11):
                    px(s, ox + x, oy + 5 - bob, white)
                    px(s, ox + x, oy + 4 - bob, dark)
                px(s, ox + 6, oy + 9 - bob, nose)
                px(s, ox + 9, oy + 9 - bob, nose)
                px(s, ox + 7, oy + 10 - bob, dark)
                px(s, ox + 8, oy + 10 - bob, dark)
                px(s, ox + 7, oy + 11 - bob, nose)
                px(s, ox + 8, oy + 11 - bob, nose)
                px(s, ox + 5, oy + 11 - bob, blush)
                px(s, ox + 10, oy + 11 - bob, blush)
                if st in ("jump", "fall"):
                    px(s, ox + 5, oy + 13 - bob, dark)
                    px(s, ox + 10, oy + 13 - bob, dark)
                else:
                    leg_shift = 1 if (st == "walk" and f % 2) else 0
                    px(s, ox + 5 + leg_shift, oy + 13 - bob, dark)
                    px(s, ox + 10 - leg_shift, oy + 13 - bob, dark)
                if st == "hurt" and f % 2 == 0:
                    px(s, ox + 6, oy + 8 - bob, (255, 100, 100, 255))
                    px(s, ox + 9, oy + 8 - bob, (255, 100, 100, 255))
                if st == "win":
                    px(s, ox + 2, oy + 5 - bob, ice)
                    px(s, ox + 13, oy + 5 - bob, ice)
                if st == "death":
                    for x in range(4, 12):
                        px(s, ox + x, oy + 13, dark)

        pygame.image.save(s, path)

    def frame(self, state, t):
        arr = self.frames.get(state, self.frames["idle"])
        fps = self.anim_fps.get(state, 6)
        idx = int(t * fps) % max(1, len(arr))
        return arr[idx]
