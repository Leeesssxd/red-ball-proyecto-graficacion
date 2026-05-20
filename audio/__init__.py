"""Sistema de audio: música real con loop limpio + SFX con cooldowns anti-spam."""
import os
import pygame

from .sound_manager import SoundManager

# Ruta base del proyecto (audio/ está dentro del repo)
_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas reales de las canciones (case-insensitive search al iniciar)
def _find_music(name_lower):
    audio_dir = os.path.join(_BASE, "audio")
    for f in os.listdir(audio_dir):
        if f.lower() == name_lower:
            return os.path.join(audio_dir, f)
    return None

_MUSIC_MENU   = _find_music("cancion_menu.mp3")
_MUSIC_COMBAT = _find_music("cancion_combate.mp3")


class AudioSystem:
    """Sistema de audio principal: música real + SFX con cooldowns."""

    # Cooldowns en segundos por tipo de SFX (evita spam por frame)
    _COOLDOWNS = {
        "land":   0.25,
        "bounce": 0.20,
        "hurt":   0.40,
        "jump":   0.12,
        "death":  2.0,
        "goal":   1.0,
        "ui":     0.10,
    }

    def __init__(self):
        self.enabled = True
        self._current_track = None   # "menu" | "combat" | None
        self._sfx_timers = {}        # cooldown acumulado por clave SFX

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=1024)
            self.sm = SoundManager()
        except pygame.error:
            self.enabled = False
            self.sm = None

    # ------------------------------------------------------------------
    # SFX
    # ------------------------------------------------------------------
    def play(self, key):
        if not self.enabled or not self.sm:
            return
        now = pygame.time.get_ticks() / 1000.0
        last = self._sfx_timers.get(key, 0.0)
        cd = self._COOLDOWNS.get(key, 0.05)
        if now - last < cd:
            return                     # todavía en cooldown → ignorar
        self._sfx_timers[key] = now

        mapping = {
            "jump":   "jump",
            "bounce": "bounce",
            "land":   "land",
            "death":  "death",
            "goal":   "victory",
            "ui":     "menu_click",
            "hurt":   "hurt",
        }
        self.sm.play(mapping.get(key, key))

    # ------------------------------------------------------------------
    # Música
    # ------------------------------------------------------------------
    def _play_track(self, path, track_id):
        """Carga y reproduce una pista con loop. No reinicia si ya está activa."""
        if self._current_track == track_id:
            # Ya está sonando esta pista → no interrumpir
            if pygame.mixer.music.get_busy():
                return
            # Si terminó por algún motivo, reiniciar
            pygame.mixer.music.play(-1)
            return

        self._current_track = track_id
        if path and os.path.isfile(path):
            try:
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(0.38)
                pygame.mixer.music.play(-1)   # -1 = loop infinito
            except pygame.error:
                pass

    def play_menu_music(self):
        """Reproducir música de menú."""
        if self.enabled:
            self._play_track(_MUSIC_MENU, "menu")

    def play_combat_music(self):
        """Reproducir música de combate/gameplay."""
        if self.enabled:
            self._play_track(_MUSIC_COMBAT, "combat")

    def stop_music(self):
        if self.enabled:
            pygame.mixer.music.stop()
            self._current_track = None

    def update_music(self, dt, active=True, in_menu=False):
        """Llamado cada frame: arranca la pista correcta si no está sonando."""
        if not self.enabled:
            return
        if in_menu:
            self.play_menu_music()
        elif active:
            self.play_combat_music()


__all__ = ["AudioSystem", "SoundManager"]
