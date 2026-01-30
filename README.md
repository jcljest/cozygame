# Cozy Game Prototype

Simple pygame project with placeholder hitboxes and optional asset overrides.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install pygame
python src/main.py
```

## Assets

Drop your images into `assets/`:
- `assets/player.png` (defaults to 32x48)
- `assets/background.png` (defaults to 960x540)

If an asset is missing, a colored placeholder is used.

## Hitboxes

Placeholder rectangles live in `src/main.py` inside `World._build_colliders()`.
Replace with your own hitboxes or load them from a JSON/CSV file.
