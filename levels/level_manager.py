"""Loads and manages levels from level_data."""
import pygame
from levels.level_data import LEVELS
from entities import Platform, Spike, BouncePad, Goal, Player
from graphics import Camera


class Level:
    def __init__(self, data: dict):
        self.title = data.get("title", "Level")
        self.level_w = data["level_w"]
        self.level_h = data["level_h"]
        self.kill_y = data.get("kill_y", self.level_h - 50)
        self.spawn = data["spawn"]

        self.platforms = []
        self.spikes = []
        self.bounce_pads = []
        self.goal = None
        self.player = None

        self._load(data)

    def _load(self, data):
        for pd in data.get("platforms", []):
            kw = {k: v for k, v in pd.items() if k not in ("x", "y", "w", "h")}
            self.platforms.append(Platform(pd["x"], pd["y"], pd["w"], pd["h"], **kw))

        for sd in data.get("spikes", []):
            self.spikes.append(Spike(sd["x"], sd["y"], sd.get("w", 32), sd.get("h", 32), sd.get("flip", False)))

        for bd in data.get("bounce_pads", []):
            self.bounce_pads.append(BouncePad(bd["x"], bd["y"], bd.get("w", 64), bd.get("h", 16), bd.get("boost", -20)))

        gd = data.get("goal", {})
        if gd:
            self.goal = Goal(gd["x"], gd["y"], gd.get("size", 36))

        self.player = Player(*self.spawn)

    def update(self, keys, particles):
        if not self.player:
            return {"jumped": False, "landed": False, "died": False, "bounced": False, "goal": False}

        p = self.player
        was_buf = p._jump_buf
        p.handle_input(keys)
        jumped = was_buf > 0 and p._jump_buf == 0 and p.vy < 0

        p.apply_gravity()
        p.move()

        for plat in self.platforms:
            plat.update()
            p.resolve_platform(plat)

        for spike in self.spikes:
            spike.update()
            p.resolve_spike(spike)

        bounced = False
        for bp in self.bounce_pads:
            bp.update()
            if p.resolve_bounce_pad(bp):
                particles.emit_jump(p.x, p.y)
                bounced = True

        got_goal = False
        if self.goal:
            self.goal.update()
            if p.resolve_goal(self.goal):
                particles.emit_goal(p.x, p.y)
                got_goal = True

        landed = p.on_ground and not p.was_ground
        if landed:
            particles.emit_land(p.x, p.y + p.RADIUS)
        if abs(p.vx) > 2 and p.on_ground:
            particles.emit_roll(p.x, p.y + p.RADIUS, p.vx)

        died = False
        if p.y > self.kill_y and p.alive:
            p.alive = False
        if not p.alive and p.was_ground != "dead_done":
            particles.emit_death(p.x, p.y)
            p.was_ground = "dead_done"
            died = True

        return {"jumped": jumped, "landed": landed, "died": died, "bounced": bounced, "goal": got_goal}

    def draw(self, surface, cam):
        for plat in self.platforms:
            plat.draw(surface, cam)
        for spike in self.spikes:
            spike.draw(surface, cam)
        for bp in self.bounce_pads:
            bp.draw(surface, cam)
        if self.goal:
            self.goal.draw(surface, cam)
        if self.player:
            self.player.draw(surface, cam)


class LevelManager:
    def __init__(self):
        self._index = 0
        self.current = None
        self.camera = None
        self._load_current()

    @property
    def index(self):
        return self._index

    @property
    def total(self):
        return len(LEVELS)

    def _load_current(self):
        data = LEVELS[self._index]
        self.current = Level(data)
        self.camera = Camera(self.current.level_w, self.current.level_h)

    def next_level(self) -> bool:
        if self._index + 1 < len(LEVELS):
            self._index += 1
            self._load_current()
            return True
        return False

    def restart(self):
        self._load_current()

    def update(self, keys, particles):
        if not self.current:
            return {}
        p = self.current.player
        events = self.current.update(keys, particles)
        if p:
            self.camera.update(p.x, p.y)
        return events

    def draw(self, surface):
        if self.current:
            self.current.draw(surface, self.camera)
