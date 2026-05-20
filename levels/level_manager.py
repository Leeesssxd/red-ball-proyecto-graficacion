"""Loads and manages levels from level_data."""
from levels.level_data import LEVELS
from entities import Platform, Spike, BouncePad, Goal, Player
from graphics import Camera
from boss.frost_guardian import FrostGuardian


class Level:
    def __init__(self, data: dict):
        self.data = data
        self.title = data.get("title", "Level")
        self.biome = data.get("biome", "")
        self.theme = data.get("theme", "tundra_day")
        self.level_w = data["level_w"]
        self.level_h = data["level_h"]
        self.kill_y = data.get("kill_y", self.level_h - 50)
        self.spawn = data["spawn"]
        self.secret_gate = data.get("secret_gate", False)
        self.is_secret = data.get("is_secret", False)

        self.platforms = []
        self.spikes = []
        self.bounce_pads = []
        self.goal = None
        self.player = None
        self.boss = None
        self._death_fx_done = False
        self._boss_defeated_once = False
        self.coin_id = None

        self._load(data)

    def _load(self, data):
        for pd in data.get("platforms", []):
            kw = {k: v for k, v in pd.items() if k not in ("x", "y", "w", "h")}
            self.platforms.append(Platform(pd["x"], pd["y"], pd["w"], pd["h"], **kw))

        for sd in data.get("spikes", []):
            self.spikes.append(Spike(sd["x"], sd["y"], sd.get("w", 32), sd.get("h", 32), sd.get("flip", False)))

        for bd in data.get("bounce_pads", []):
            bp = BouncePad(bd["x"], bd["y"], bd.get("w", 64), bd.get("h", 16), bd.get("boost", -20))
            bp.attach_platform = bd.get("attach_platform")
            self.bounce_pads.append(bp)

        gd = data.get("goal", {})
        if gd:
            self.goal = Goal(gd["x"], gd["y"], gd.get("size", 36))

        bd = data.get("boss")
        if bd:
            self.boss = FrostGuardian(bd["x"], bd["y"], bd.get("tier", "mini"))
            self.coin_id = bd.get("coin_id")

        self.player = Player(*self.spawn)

    def update(self, keys, particles, special_coins=0):
        if not self.player:
            return {"jumped": False, "landed": False, "died": False, "bounced": False, "goal": False, "shake": 0.0, "boss_coin": None, "player_hit": False, "secret_locked": False}

        p = self.player
        was_buf = p._jump_buf
        p.handle_input(keys)
        jumped = was_buf > 0 and p._jump_buf == 0 and p.vy < 0
        p.apply_gravity()
        p.move()

        for plat in self.platforms:
            plat.update()
            p.resolve_platform(plat)

        for bp in self.bounce_pads:
            ai = getattr(bp, "attach_platform", None)
            if ai is not None and 0 <= ai < len(self.platforms):
                ap = self.platforms[ai]
                bp.follow_delta(ap.dx, ap.dy)

        for spike in self.spikes:
            spike.update()
            p.resolve_spike(spike)

        bounced = False
        for bp in self.bounce_pads:
            bp.update()
            if p.resolve_bounce_pad(bp):
                particles.emit_jump(p.x, p.y)
                bounced = True

        shake = 0.0
        player_hit = False
        boss_coin = None

        if self.boss:
            self.boss.update(1 / 60, p)
            bh = self.boss.resolve_hits(p)
            if bh["boss_hit"]:
                particles.emit_goal(self.boss.x, self.boss.y - 30)
                shake = max(shake, 3.6)
            if bh["player_hit"]:
                player_hit = True
                shake = max(shake, 2.0)
            if bh["boss_dead"]:
                particles.emit_goal(self.boss.x, self.boss.y)
                shake = max(shake, 6.0)
                if self.coin_id and not self._boss_defeated_once:
                    self._boss_defeated_once = True
                    boss_coin = self.coin_id

        got_goal = False
        secret_locked = False
        if self.goal and (not self.boss or not self.boss.alive):
            self.goal.update()
            if p.resolve_goal(self.goal):
                if self.secret_gate and special_coins < 3:
                    p.won = False
                    self.goal.collected = False
                    secret_locked = True
                else:
                    particles.emit_goal(p.x, p.y)
                    got_goal = True

        landed = p.on_ground and not p.was_ground
        if landed:
            particles.emit_land(p.x, p.y + p.RADIUS)
            if abs(p.vy) > 5:
                shake = max(shake, 1.2)
        if abs(p.vx) > 2 and p.on_ground:
            particles.emit_roll(p.x, p.y + p.RADIUS, p.vx)

        died = False
        if p.y > self.kill_y and p.alive:
            p.alive = False

        if not p.alive and not self._death_fx_done:
            particles.emit_death(p.x, p.y)
            self._death_fx_done = True
            died = True
            shake = max(shake, 4.0)

        return {"jumped": jumped, "landed": landed, "died": died, "bounced": bounced, "goal": got_goal, "shake": shake, "boss_coin": boss_coin, "player_hit": player_hit, "secret_locked": secret_locked}

    def draw(self, surface, cam):
        for plat in self.platforms:
            plat.draw(surface, cam)
        for spike in self.spikes:
            spike.draw(surface, cam)
        for bp in self.bounce_pads:
            bp.draw(surface, cam)
        if self.goal:
            self.goal.draw(surface, cam)
        if self.boss:
            self.boss.draw(surface, cam)
        if self.player:
            self.player.draw(surface, cam)


class LevelManager:
    def __init__(self):
        self._index = 0
        self.current = None
        self.camera = None
        self.special_coins = set()
        self.secret_unlocked = False
        self._load_current()

    @property
    def index(self):
        return self._index

    @property
    def total(self):
        return 6

    def _load_current(self):
        data = LEVELS[self._index]
        self.current = Level(data)
        self.camera = Camera(self.current.level_w, self.current.level_h)

    def next_level(self) -> bool:
        if self._index == 4:
            if self.secret_unlocked:
                self._index = 5
                self._load_current()
                return True
            return False
        if self._index + 1 < 5:
            self._index += 1
            self._load_current()
            return True
        return False

    def try_unlock_secret(self):
        if len(self.special_coins) >= 3:
            self.secret_unlocked = True
            return True
        return False

    def restart(self):
        self._load_current()

    def update(self, keys, particles):
        if not self.current:
            return {}
        p = self.current.player
        events = self.current.update(keys, particles, special_coins=len(self.special_coins))
        if events.get("boss_coin") is not None:
            self.special_coins.add(events["boss_coin"])
        if p:
            self.camera.update(p.x, p.y)
            if events.get("shake", 0) > 0:
                self.camera.add_shake(events["shake"])
        return events

    def draw(self, surface):
        if self.current:
            self.current.draw(surface, self.camera)
