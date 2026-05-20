# =============================================================
#  config.py  –  Global constants & tunable parameters
# =============================================================

import pygame

SCREEN_W, SCREEN_H = 1280, 720
TITLE = "Frostbound Paws"
FPS = 60
VSYNC = True

GRAVITY = 0.60
MAX_FALL = 19.5
JUMP_FORCE = -14.2
FRICTION = 0.84
AIR_FRICTION = 0.94
ACCEL = 0.95
MAX_SPEED = 8.4

GRAVITY_PPS = 1800.0
TERMINAL_VEL = 1200.0
COYOTE_TIME = 0.10
JUMP_BUFFER_TIME = 0.12

C_BG = (8, 8, 20)
C_GRID = (20, 20, 50)
C_GRID2 = (40, 90, 150)
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (255, 50, 50)
C_GREEN = (50, 220, 80)
C_BLUE = (50, 150, 255)
C_YELLOW = (255, 220, 30)
C_CYAN = (30, 220, 255)
C_MAGENTA = (220, 30, 255)
C_ORANGE = (255, 140, 20)

C_PLATFORM = (30, 160, 220)
C_PLAT_TOP = (95, 225, 255)
C_PLAT_SIDE = (18, 105, 160)
C_BALL = (228, 40, 56)
C_BALL_SHINE = (255, 150, 150)
C_BALL_SHADE = (120, 10, 15)
C_BALL_SHADOW = (0, 0, 0, 80)
C_GOAL = C_YELLOW
C_GOAL_GLOW = (255, 180, 0)
C_SPIKE = (255, 60, 80)
C_HUD_BG = (10, 15, 30, 180)
C_HUD_TEXT = (200, 230, 255)

NEON_PALETTE = [C_RED, C_CYAN, C_MAGENTA, C_GREEN, C_YELLOW, C_ORANGE, C_BLUE]

CHARACTERS = {
    "Balanced": {"color": C_RED, "glow": (255, 80, 80), "radius": 18, "speed": 380, "accel": 2200, "friction": 1800, "jump_vel": 700, "mass": 1.0, "desc": "Well-rounded fighter"}
}

CONTROLS_P1 = {"left": pygame.K_a, "right": pygame.K_d, "jump": pygame.K_w, "down": pygame.K_s}
CONTROLS_P2 = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "jump": pygame.K_UP, "down": pygame.K_DOWN}

CAM_LERP = 8.0
CAM_SHAKE_DECAY = 6.0
CAM_ZOOM_LERP = 4.0
CAM_ZOOM_DEFAULT = 1.0
CAM_ZOOM_SPEED = 1.2
CAM_SMOOTH = 0.13
CAM_OFFSET_X = SCREEN_W // 3
CAM_OFFSET_Y = SCREEN_H // 2

PARALLAX_FACTORS = [0.15, 0.30, 0.55]
PARALLAX_SPEEDS = [0.1, 0.25, 0.45]

PLATFORM_THICKNESS = 14
SHADOW_OFFSET_X = 6
SHADOW_OFFSET_Y = 8
TILE = 48

HUD_MARGIN = 16
HUD_BAR_W = 180
HUD_BAR_H = 14

VOL_MUSIC = 0.35
VOL_SFX = 0.70

BOSS_PHASES = 3
BOSS_HP_PER_PHASE = 100
MAX_PARTICLES = 600
TOTAL_LEVELS = 6
