import math
import random
import pygame
from config import VOL_MUSIC, VOL_SFX


def _gen_wave(freq=440, duration=0.15, volume=0.6, wave_type="sine", sample_rate=44100, envelope=(0.01, 0.0, 0.8, 0.05), pitch_sweep=0.0):
    n_samples = int(sample_rate * duration)
    a, d, s, r = envelope
    frames = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        t_norm = t / max(duration, 1e-6)

        if t_norm < a:
            env = t_norm / max(a, 1e-6)
        elif t_norm < a + d:
            env = 1.0 - (1.0 - s) * (t_norm - a) / max(d, 1e-6)
        elif t_norm < 1.0 - r:
            env = s
        else:
            env = s * (1.0 - (t_norm - (1.0 - r)) / max(r, 1e-6))
        env = max(0.0, env)

        f = freq * (2 ** (pitch_sweep * t / 12.0))
        phase = (t * f) % 1.0
        if wave_type == "sine":
            sample = math.sin(phase * math.tau)
        elif wave_type == "square":
            sample = 1.0 if phase < 0.5 else -1.0
        elif wave_type == "saw":
            sample = 2.0 * phase - 1.0
        elif wave_type == "noise":
            sample = random.uniform(-1, 1)
        elif wave_type == "tri":
            sample = 4.0 * abs(phase - 0.5) - 1.0
        else:
            sample = 0.0

        val = int(max(-32768, min(32767, sample * env * volume * 32767)))
        frames += int(val).to_bytes(2, "little", signed=True)
        frames += int(val).to_bytes(2, "little", signed=True)

    return pygame.mixer.Sound(buffer=bytes(frames))


class SoundManager:
    def __init__(self):
        self._sfx = {}
        self._muted = False
        pygame.mixer.set_num_channels(16)
        self._build_sfx()

    def _build_sfx(self):
        defs = {
            "jump": dict(freq=380, duration=0.14, wave_type="sine", pitch_sweep=6, volume=0.5, envelope=(0.01, 0.05, 0.4, 0.3)),
            "land": dict(freq=120, duration=0.12, wave_type="noise", volume=0.4, envelope=(0.001, 0.05, 0.2, 0.5)),
            "bounce": dict(freq=500, duration=0.2, wave_type="sine", pitch_sweep=8, volume=0.6, envelope=(0.01, 0.1, 0.5, 0.2)),
            "death": dict(freq=220, duration=0.5, wave_type="square", pitch_sweep=-18, volume=0.5, envelope=(0.01, 0.1, 0.7, 0.1)),
            "checkpoint": dict(freq=660, duration=0.35, wave_type="sine", pitch_sweep=5, volume=0.5, envelope=(0.02, 0.1, 0.6, 0.2)),
            "victory": dict(freq=880, duration=0.6, wave_type="sine", pitch_sweep=12, volume=0.5, envelope=(0.02, 0.1, 0.8, 0.1)),
            "menu_click": dict(freq=600, duration=0.06, wave_type="sine", volume=0.3, envelope=(0.005, 0.05, 0.3, 0.5)),
            "boss_hit": dict(freq=160, duration=0.2, wave_type="noise", volume=0.7, envelope=(0.001, 0.05, 0.6, 0.3)),
            "boss_die": dict(freq=80, duration=1.0, wave_type="square", pitch_sweep=-24, volume=0.7, envelope=(0.01, 0.2, 0.7, 0.1)),
            "powerup": dict(freq=440, duration=0.3, wave_type="tri", pitch_sweep=18, volume=0.5, envelope=(0.01, 0.1, 0.7, 0.2)),
            "hurt": dict(freq=200, duration=0.2, wave_type="noise", volume=0.5, envelope=(0.001, 0.08, 0.4, 0.4)),
        }
        for name, kwargs in defs.items():
            try:
                snd = _gen_wave(**kwargs)
                snd.set_volume(VOL_SFX)
                self._sfx[name] = snd
            except Exception:
                pass

    def play(self, name, volume_override=None):
        if self._muted:
            return
        snd = self._sfx.get(name)
        if snd is None:
            return
        if volume_override is not None:
            snd.set_volume(volume_override)
        ch = pygame.mixer.find_channel(True)
        if ch:
            ch.play(snd)

    def toggle_mute(self):
        self._muted = not self._muted
        if self._muted:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

    def play_music(self, theme="game"):
        import os
        path_map = {
            "game": "assets/music_game.ogg",
            "boss": "assets/music_boss.ogg",
            "menu": "assets/music_menu.ogg",
        }
        path = path_map.get(theme, "")
        if os.path.exists(path):
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(VOL_MUSIC)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()
