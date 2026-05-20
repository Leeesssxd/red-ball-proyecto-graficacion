"""Bucle principal del juego y máquina de estados — Garras Glaciares."""
import sys
import pygame

from config import SCREEN_W, SCREEN_H, FPS, TITLE, C_CYAN, VSYNC
from graphics import Background, ParticleSystem
from levels import LevelManager
from ui import HUD, MessageOverlay, TitleScreen, WinScreen
from audio import AudioSystem


class GameLoop:
    STATE_TITLE   = "title"
    STATE_PLAYING = "playing"
    STATE_DEAD    = "dead"
    STATE_ALL_WIN = "all_win"

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = self._create_display()
        self.clock  = pygame.time.Clock()

        self.bg      = Background()
        self.parts   = ParticleSystem()
        self.lm      = LevelManager()
        self.hud     = HUD()
        self.overlay = MessageOverlay()
        self.title   = TitleScreen()
        self.win_scr = WinScreen()
        self.audio   = AudioSystem()

        self._state     = self.STATE_TITLE
        self._timer     = 0.0
        self._run_timer = 0.0
        self._dead_wait = 0.0
        self._time_str  = ""

    def _create_display(self):
        try:
            return pygame.display.set_mode((SCREEN_W, SCREEN_H), vsync=1 if VSYNC else 0)
        except TypeError:
            return pygame.display.set_mode((SCREEN_W, SCREEN_H))

    def run(self):
        while True:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.05)
            self._handle_events()

            if self._state == self.STATE_TITLE:
                self._tick_title(dt)
            elif self._state == self.STATE_PLAYING:
                self._tick_playing(dt)
            elif self._state == self.STATE_DEAD:
                self._tick_dead(dt)
            elif self._state == self.STATE_ALL_WIN:
                self._tick_all_win(dt)

            pygame.display.flip()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self._state != self.STATE_ALL_WIN:
                    pygame.quit()
                    sys.exit()

                if self._state == self.STATE_TITLE and self.title.handle_event(event):
                    self.audio.play("ui")
                    self._start_game()

                elif self._state == self.STATE_PLAYING and event.key == pygame.K_r:
                    self.audio.play("ui")
                    self._restart_level()

                elif self._state == self.STATE_ALL_WIN:
                    action = self.win_scr.handle_event(event)
                    if action == "restart":
                        self.audio.play("ui")
                        self._start_game()
                    elif action == "quit":
                        pygame.quit()
                        sys.exit()

                elif self._state == self.STATE_DEAD and event.key == pygame.K_r:
                    self.audio.play("ui")
                    self._restart_level()

    def _start_game(self):
        self.lm      = LevelManager()
        self.parts   = ParticleSystem()
        self._timer  = 0.0
        self._run_timer = 0.0
        self._state  = self.STATE_PLAYING
        self.overlay.clear()

    def _restart_level(self):
        self.lm.restart()
        self.parts  = ParticleSystem()
        self._timer = 0.0
        self._state = self.STATE_PLAYING
        self.overlay.clear()

    # ------------------------------------------------------------------
    # Estados
    # ------------------------------------------------------------------
    def _tick_title(self, dt):
        self.audio.update_music(dt, active=True, in_menu=True)
        self.title.update(dt)
        # Dibuja el fondo ártico real (nivel 1) detrás del menú
        self.bg.set_theme("tundra_day")
        self.bg.draw(self.screen, 0, 0, self.title._t)
        self.title.draw(self.screen)

    def _tick_playing(self, dt):
        keys   = pygame.key.get_pressed()
        lvl    = self.lm.current
        cam    = self.lm.camera

        self._timer     += dt
        self._run_timer += dt
        self.hud.update(dt)
        self.overlay.update(dt)

        events = self.lm.update(keys, self.parts)
        self.parts.update()

        # SFX — cada uno protegido con cooldown en AudioSystem
        if events.get("jumped"):
            self.audio.play("jump")
        if events.get("landed"):
            self.audio.play("land")
        if events.get("bounced"):
            self.audio.play("bounce")
        if events.get("goal"):
            self.audio.play("goal")
        if events.get("died"):
            self.audio.play("death")
        if events.get("player_hit"):
            self.audio.play("hurt")

        if events.get("secret_locked"):
            self.overlay.show(
                "PUERTA SECRETA BLOQUEADA",
                f"Necesitas 3 reliquias ({len(self.lm.special_coins)}/3)",
                duration=1.8,
                colour=(220, 235, 255),
            )

        player = lvl.player if lvl else None
        if player and not player.alive:
            self._state     = self.STATE_DEAD
            self._dead_wait = 1.2
            self.overlay.show("CAÍDO", "R reiniciar   ESC salir", duration=999.0, colour=(210, 230, 255))

        if player and player.won:
            if self.lm.index == 4:
                self.lm.try_unlock_secret()
            advanced = self.lm.next_level()
            if advanced:
                self._timer = 0.0
                self.parts  = ParticleSystem()
                nxt = self.lm.current.biome if hasattr(self.lm.current, "biome") else self.lm.current.title
                if self.lm.index == 5:
                    self.overlay.show("SECRETO DESBLOQUEADO", f"Entrando: {nxt}", duration=2.0, colour=C_CYAN)
                else:
                    self.overlay.show("ÁREA SUPERADA", f"Siguiente: {nxt}", duration=1.8, colour=C_CYAN)
            else:
                mins = int(self._run_timer) // 60
                secs = int(self._run_timer) % 60
                self._time_str = f"{mins:02d}:{secs:02d}"
                self._state = self.STATE_ALL_WIN

        if lvl:
            self.bg.set_theme(lvl.theme)

        cam_x = cam.x if cam else 0
        cam_y = cam.y if cam else 0
        self.bg.draw(self.screen, cam_x, cam_y, self._run_timer)
        self.parts.draw(self.screen, cam_x, cam_y)
        self.lm.draw(self.screen)

        if lvl and player:
            self.hud.draw(self.screen, lvl.title, self.lm.index + 1, self.lm.total,
                          player, self._run_timer, len(self.lm.special_coins), self.lm.secret_unlocked)
            self.hud.draw_progress_bar(self.screen, player.x, lvl.level_w)

        self.overlay.draw(self.screen)
        self.audio.update_music(dt, active=True, in_menu=False)

    def _tick_dead(self, dt):
        lvl = self.lm.current
        cam = self.lm.camera
        if lvl:
            self.bg.set_theme(lvl.theme)
        cam_x = cam.x if cam else 0
        cam_y = cam.y if cam else 0
        self.bg.draw(self.screen, cam_x, cam_y, self._run_timer)
        self.parts.update()
        self.parts.draw(self.screen, cam_x, cam_y)
        self.lm.draw(self.screen)
        self.overlay.draw(self.screen)

        self._dead_wait -= dt
        if self._dead_wait <= 0 and not pygame.key.get_pressed()[pygame.K_r]:
            self._restart_level()

        # Música de combate también en estado muerto (transición suave)
        self.audio.update_music(dt, active=True, in_menu=False)

    def _tick_all_win(self, dt):
        lvl = self.lm.current
        cam = self.lm.camera
        if lvl:
            self.bg.set_theme(lvl.theme)
        cam_x = cam.x if cam else 0
        cam_y = cam.y if cam else 0
        self.bg.draw(self.screen, cam_x, cam_y, self._run_timer)
        self.parts.update()
        self.parts.draw(self.screen, cam_x, cam_y)
        self.lm.draw(self.screen)
        self.win_scr.update(dt)
        self.win_scr.draw(self.screen, self._time_str, len(self.lm.special_coins), self.lm.secret_unlocked)
        self.audio.update_music(dt, active=True, in_menu=False)
