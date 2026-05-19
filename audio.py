"""Lightweight procedural audio manager for arcade feedback."""
import math
import array
import pygame


class AudioSystem:
    def __init__(self):
        self.enabled = False
        self._sounds = {}
        self._music_phase = 0.0
        self._music_timer = 0.0
        self._music_interval = 0.28

        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=256)
            self.enabled = True
            self._build_sounds()
        except pygame.error:
            self.enabled = False

    def _tone(self, freq, duration=0.12, volume=0.4, decay=6.0):
        sample_rate = 22050
        count = max(1, int(sample_rate * duration))
        buf = array.array("h")
        for i in range(count):
            t = i / sample_rate
            env = math.exp(-decay * t)
            sample = math.sin(2 * math.pi * freq * t)
            val = int(32767 * volume * env * sample)
            buf.append(val)
        return pygame.mixer.Sound(buffer=buf)

    def _build_sounds(self):
        self._sounds = {
            "jump": self._tone(520, 0.11, 0.35, decay=7.5),
            "bounce": self._tone(330, 0.16, 0.40, decay=4.8),
            "land": self._tone(140, 0.09, 0.32, decay=8.5),
            "death": self._tone(95, 0.35, 0.45, decay=2.6),
            "goal": self._tone(780, 0.28, 0.42, decay=3.6),
            "ui": self._tone(680, 0.08, 0.28, decay=9.0),
        }

    def play(self, key):
        if not self.enabled:
            return
        snd = self._sounds.get(key)
        if snd:
            snd.play()

    def update_music(self, dt, active=True):
        if not self.enabled or not active:
            return
        self._music_timer += dt
        if self._music_timer < self._music_interval:
            return
        self._music_timer = 0.0
        self._music_phase += 1.0
        notes = [262, 294, 330, 392, 440, 392, 330, 294]
        idx = int(self._music_phase) % len(notes)
        self._tone(notes[idx], duration=0.1, volume=0.10, decay=8.0).play()
