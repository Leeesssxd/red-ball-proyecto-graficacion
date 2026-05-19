import pygame

from .sound_manager import SoundManager


class AudioSystem:
    """Compatibility adapter used by the current game loop."""

    def __init__(self):
        self.enabled = True
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
            }
            self.sm.play(mapping.get(key, key))

    def update_music(self, dt, active=True):
        # Music control is intentionally lightweight for compatibility.
        if not active or not self.enabled or not self.sm:
            return


__all__ = ["AudioSystem", "SoundManager"]
