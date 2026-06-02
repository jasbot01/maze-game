"""Level data and level helper logic for RescueBot."""

import pygame

from game.settings import FLOOR, ROBOT_START, TILE_SIZE, WALL
from game.tile import Tile


# Simple hardcoded test map
LEVEL = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


def build_tiles(level: list[list[int]]) -> pygame.sprite.Group:
    """Convert the level grid into a group of Tile sprites.

    Args:
        level: A 2D list containing tile type IDs.

    Returns:
        A Pygame sprite group containing every visible tile in the level.
    """
    tiles = pygame.sprite.Group()

    for row_index, row in enumerate(level):

        for col_index, tile_type in enumerate(row):

            # The robot start position should look like floor underneath.
            visible_tile_type = FLOOR if tile_type == ROBOT_START else tile_type

            tile = Tile(visible_tile_type, row_index, col_index)
            tiles.add(tile)

    return tiles


def get_level_size(level: list[list[int]]) -> tuple[int, int]:
    """Calculate the level surface size from the level size.

    Args:
        level: A 2D list containing tile type IDs.

    Returns:
        The level width and height in pixels.
    """
    rows = len(level)
    cols = len(level[0])

    return (cols * TILE_SIZE, rows * TILE_SIZE)


def get_scaled_level_rect(level_surface: pygame.Surface, screen: pygame.Surface) -> pygame.Rect:
    """Calculate where the scaled level should appear in the window.

    This keeps the maze's original aspect ratio, so the tiles do not stretch
    unevenly if the window is wider or taller than the maze.

    Args:
        level_surface: The offscreen surface where the maze is drawn.
        screen: The actual game window surface.

    Returns:
        A rectangle describing the scaled maze size and centered position.
    """
    level_width, level_height = level_surface.get_size()
    screen_width, screen_height = screen.get_size()

    # Pick the smaller scale factor so the whole maze fits inside the window.
    scale = min(screen_width / level_width, screen_height / level_height)

    # Calculate the scaled maze size.
    scaled_width = int(level_width * scale)
    scaled_height = int(level_height * scale)

    # Center the scaled maze inside the window.
    left = (screen_width - scaled_width) // 2
    top = (screen_height - scaled_height) // 2

    return pygame.Rect(left, top, scaled_width, scaled_height)


def find_tile(level: list[list[int]], target_tile: int) -> tuple[int, int]:
    """Find the first matching tile in the level.

    Args:
        level: A 2D list containing tile type IDs.
        target_tile: The tile type to find.

    Returns:
        The matching tile's row and column.

    Raises:
        ValueError: If the tile type is not found.
    """
    for row_index, row in enumerate(level):
        for col_index, tile_type in enumerate(row):
            if tile_type == target_tile:
                return row_index, col_index

    raise ValueError(f"Tile type {target_tile} was not found in the level.")


def can_move_to(level: list[list[int]], row: int, col: int) -> bool:
    """Check whether the robot can move to a tile.

    Args:
        level: A 2D list containing tile type IDs.
        row: The target row.
        col: The target column.

    Returns:
        True if the target tile is inside the map and not a wall.
    """
    is_inside_level = 0 <= row < len(level) and 0 <= col < len(level[0])

    if not is_inside_level:
        return False

    return level[row][col] != WALL
