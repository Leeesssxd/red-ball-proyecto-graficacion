# RedBall – Arcade Futuristic

A pseudo-3D arcade platformer built with Python + Pygame.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| ← / A | Move left |
| → / D | Move right |
| SPACE / ↑ / W | Jump (coyote-time + jump buffer) |
| R | Restart current level |
| ESC | Quit |

## Levels

| # | Title | Key mechanic |
|---|-------|-------------|
| 1 | Launch Pad | Moving platforms, crumble tiles, bounce pad |
| 2 | Sky Bridge | Narrow jumps, vertical movers, crumble bridge |

## Architecture

```
redball_python/
├── main.py            Entry point
├── config.py          Global constants (physics, colours, screen)
├── core/
│   └── game_loop.py   State machine, main loop
├── entities/
│   ├── player.py      Ball physics + collision resolution
│   ├── platform.py    Static / moving / crumbling platforms
│   ├── obstacle.py    Spikes + bounce pads
│   └── goal.py        Animated star goal
├── graphics/
│   ├── camera.py      Smooth-follow camera
│   ├── background.py  Parallax grid + star field
│   └── particles.py   Jump dust, death burst, goal sparks
├── levels/
│   ├── level_data.py  Level definitions (pure data)
│   └── level_manager.py  Load, update, transition
├── ui/
│   ├── hud.py         Timer, progress bar, controls hint
│   └── menu.py        Title screen, win screen
└── utils/
    ├── vec2.py        2-D vector class
    └── helpers.py     lerp, clamp, draw helpers
```

## Extending

- **Add a level**: append a dict to `LEVELS` in `levels/level_data.py` and increment `TOTAL_LEVELS` in `config.py`.
- **Tweak physics**: edit constants in `config.py` (GRAVITY, JUMP_FORCE, ACCEL, MAX_SPEED …).
- **New entity**: create a class in `entities/`, register it in `entities/__init__.py`, add to `Level._load()` and `Level.update/draw()`.

## Assets

The game is fully procedural – no external images or audio required. All rendering uses `pygame.draw.*`.
