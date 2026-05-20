# Frostbound Paws

A 2D pixel-art arctic platformer built with Python + Pygame.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Controls

- `← / A`: Move left
- `→ / D`: Move right
- `SPACE / ↑ / W`: Jump
- `R`: Restart current level
- `ESC`: Quit

## Campaign Structure

- Level 1: Tundra intro
- Level 2: Miniboss + relic 1
- Level 3: Miniboss + relic 2
- Level 4: Miniboss + relic 3
- Level 5: Final boss
- Secret Level: Unlocks if 3 relics were collected

## Notes

- Runtime architecture remains: `main.py -> GameLoop -> LevelManager`.
- Backgrounds are image/theme based and optimized to screen size.
- Included local backgrounds:
  - `assets/backgrounds/nivel_final.jpg`
  - `assets/backgrounds/nivel_final_secreto.jpg`
