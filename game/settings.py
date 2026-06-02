"""Shared game settings for RescueBot.

This module contains constants used across the game, such as window size,
tile size, asset paths, tile IDs, colors, and image filenames.
"""

from pathlib import Path


# Size of each tile on the internal level surface.
# The full level surface is scaled later to fit the game window.
TILE_SIZE = 250

# Size of the actual window shown to the player.
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
WINDOW_TITLE = "RescueBot: Low Power"

# Frames per second.
FPS = 60

# Path to the project folder.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Path to the assets folder.
ASSET_DIR = PROJECT_ROOT / "assets"


# Tile types
FLOOR = 0
WALL = 1
CHARGER = 2
ROBOT_START = 3


# Temporary fallback colors if image files do not exist yet.
COLORS = {
    FLOOR: (225, 220, 205),
    WALL: (60, 68, 84),
    CHARGER: (80, 220, 140),
}


# Optional image filenames for each tile type.
TILE_IMAGES = {
    FLOOR: "magenta_tile.png",
    WALL: "pink_blob.png",
    CHARGER: "charger.png",
}
