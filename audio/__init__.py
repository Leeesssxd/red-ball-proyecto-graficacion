import pygame

from .sound_manager import SoundManager


class AudioSystem:
    """Compatibility adapter used by the current game loop."""

    def __init__(self):
        self.enabled = True
        self._amb_t = 0.0
        self._amb_cycle = ["powerup", "menu_click", "jump"]
        self._amb_i = 0
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.sm = SoundManager()
        except pygame.error:
            self.enabled = False
            self.sm = None

    def play(self, key):
        if self.enabled and self.sm:
            mapping = {
                "jump": "jump",
                "bounce": "bounce",
                "land": "land",
                "death": "death",
                "goal": "victory",
                "ui": "menu_click",
                "hurt": "hurt",
            }
            self.sm.play(mapping.get(key, key))

    def update_music(self, dt, active=True):
        if not active or not self.enabled or not self.sm:
            return
        self._amb_t += dt
        if self._amb_t > 3.8:
            self._amb_t = 0.0
            k = self._amb_cycle[self._amb_i % len(self._amb_cycle)]
            self._amb_i += 1
            self.sm.play(k, volume_override=0.06)


__all__ = ["AudioSystem", "SoundManager"]
