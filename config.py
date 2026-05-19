# ============================================================
# config.py  –  Global constants for RedBall
# ============================================================

# ── Window ──────────────────────────────────────────────────
SCREEN_W      = 1280
SCREEN_H      = 720
FPS           = 60
TITLE         = "RedBall Ultimate – Neon Arcade"

# ── Physics ─────────────────────────────────────────────────
GRAVITY       = 0.60
JUMP_FORCE    = -14.2
MAX_FALL      = 19.5
FRICTION      = 0.84
AIR_FRICTION  = 0.94
ACCEL         = 0.95
MAX_SPEED     = 8.4

# ── Camera ──────────────────────────────────────────────────
CAM_SMOOTH    = 0.13
CAM_OFFSET_X  = SCREEN_W // 3
CAM_OFFSET_Y  = SCREEN_H // 2

# ── Colours ─────────────────────────────────────────────────
C_BG          = (7,  9,  20)
C_GRID        = (20, 35,  60)
C_GRID2       = (40, 90, 150)
C_PLATFORM    = (30, 160, 220)
C_PLAT_TOP    = (95, 225, 255)
C_PLAT_SIDE   = (18, 105, 160)
C_BALL        = (228,  40,  56)
C_BALL_SHINE  = (255, 150, 150)
C_BALL_SHADE  = (120,  10,  15)
C_BALL_SHADOW = (0,    0,   0, 80)
C_GOAL        = (255, 220,  30)
C_GOAL_GLOW   = (255, 180,   0)
C_SPIKE       = (255,  60,  80)
C_HUD_BG      = (10,  15,  30, 180)
C_HUD_TEXT    = (200, 230, 255)
C_WHITE       = (255, 255, 255)
C_CYAN        = (0,   220, 255)
C_MAGENTA     = (255,  40, 160)
C_ORANGE      = (255, 140,  20)

# ── Tile size ────────────────────────────────────────────────
TILE          = 48

# ── Parallax layers ─────────────────────────────────────────
PARALLAX_SPEEDS = [0.1, 0.25, 0.45]

# ── Levels ───────────────────────────────────────────────────
TOTAL_LEVELS  = 10
