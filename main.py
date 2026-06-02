"""Program entry point for RescueBot.

This file stays intentionally small. Its job is only to create the game object
and start the main game loop.
"""

import sys
from pathlib import Path

import pygame

## Do these later ##
# from tile import Tile
# from player import Player


## Basic settings

# Size of each tile in the actual game/grid logic.
# Adjust so tile img becomes clearer
TILE_SIZE = 250

# Size of the actual window shown to the player.
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
WINDOW_TITLE = "RescueBot: Low Power"

FPS = 60

PROJECT_ROOT = Path(__file__).resolve().parent
ASSET_DIR = PROJECT_ROOT / "assets"


# Tile types
FLOOR = 0
WALL = 1
CHARGER = 2
ROBOT_START = 3


# Simple hardcoded test map
LEVEL = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 2, 1],
    [1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]


# Temporary fallback colors if image files do not exist yet
COLORS = {
    FLOOR: (225, 220, 205),
    WALL: (60, 68, 84),
    CHARGER: (80, 220, 140),
}


# Optional image filenames for each tile type
TILE_IMAGES = {
    FLOOR: "magenta_tile.png",
    WALL: "pink_blob.png",
    CHARGER: "charger.png",
}


#-------------------------------------------------------------------------------

class Tile(pygame.sprite.Sprite):
    """One tile on the maze grid.

    A Tile is a visible square on the map, such as a floor tile, wall tile,
    or charging station tile.
    """

    def __init__(self, tile_type: int, row: int, col: int) -> None:
        """Create a tile at a specific grid position.

        Args:
            tile_type: The kind of tile, such as FLOOR, WALL, or CHARGER.
            row: The tile's row in the level grid.
            col: The tile's column in the level grid.
        """
        super().__init__()

        # Store the logical tile type so we can check it later.
        self.tile_type = tile_type

        # Store the tile's grid position.
        self.row = row
        self.col = col

        # Load the tile image, or create a fallback colored square.
        self.image = self._load_image()

        # Pygame uses rect to know where to draw the sprite.
        self.rect = self.image.get_rect(
            topleft=(self.col * TILE_SIZE, self.row * TILE_SIZE)
        )

    def _load_image(self) -> pygame.Surface:
        """Load this tile's image, or create a simple fallback surface.

        Returns:
            A Pygame Surface used as this tile's visual image.
        """
        image_name = TILE_IMAGES[self.tile_type]
        image_path = ASSET_DIR / image_name

        # If the image exists, use it.
        if image_path.exists():
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

        # Otherwise, create a temporary placeholder square.
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        surface.fill(COLORS[self.tile_type])

        # Draw a thin border so the grid is visible.
        pygame.draw.rect(surface, (140, 145, 155), surface.get_rect(), width=1)

        return surface


#-------------------------------------------------------------------------------

class Robot(pygame.sprite.Sprite):
    """The player-controlled robot.

    The robot is separate from the tilemap because it will eventually move,
    while floor/wall/charger tiles stay in fixed positions.
    """

    def __init__(self, row: int, col: int) -> None:
        """Create the robot at a specific grid position.

        Args:
            row: The robot's starting row in the level grid.
            col: The robot's starting column in the level grid.
        """
        super().__init__()

        # Store the robot's current grid position.
        self.row = row
        self.col = col

        # Load the robot image from assets/robot.png.
        self.image = self._load_image()

        # Position the robot sprite on top of its starting tile.
        self.rect = self.image.get_rect(
            topleft=(self.col * TILE_SIZE, self.row * TILE_SIZE)
        )

    def _load_image(self) -> pygame.Surface:
        """Load the robot image, or create a fallback placeholder.

        Returns:
            A Pygame Surface used as the robot sprite image.
        """
        image_path = ASSET_DIR / "robot.png"

        if image_path.exists():
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        surface.fill((72, 160, 255))
        pygame.draw.rect(surface, (245, 247, 250), surface.get_rect(), width=2)

        return surface


#-------------------------------------------------------------------------------


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

    return ( cols * TILE_SIZE, rows * TILE_SIZE )


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


def setup_game_window() -> pygame.Surface:
    """Create and configure the Pygame display window."""
    # Create the actual game window using the configured window size.
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    ## NOTE: USE THIS TO MAKE THE GAME USE THE CURRENT MONITOR SIZE BY DEFAULT
    # display_info = pygame.display.Info()
    # screen = pygame.display.set_mode((display_info.current_w, display_info.current_h))

    ## NOTE: USE THIS FOR "TRUE" FULLSCREEN
    # display_info = pygame.display.Info()
    # screen = pygame.display.set_mode(
    #     (display_info.current_w, display_info.current_h),
    #     pygame.FULLSCREEN
    # )

    # Set the window's title.
    pygame.display.set_caption(WINDOW_TITLE)

    return screen


#-------------------------------------------------------------------------------


def main() -> None:
    """Run the basic tile-rendering prototype."""
    pygame.init()

    # Create & setup the game window.
    screen = setup_game_window()

    # Create an offscreen surface that matches the maze's true grid size.
    # The tile sprites are drawn here first, then this surface is scaled up.
    level_surface = pygame.Surface(get_level_size(LEVEL))

    clock = pygame.time.Clock()

    # Build all tile sprites once at startup.
    tiles = build_tiles(LEVEL)

    # Find the robot's starting tile in the level.
    robot_row, robot_col = find_tile(LEVEL, ROBOT_START)

    # # Create one robot sprite and store it in a sprite group.
    # robot = pygame.sprite.GroupSingle(Robot(robot_row, robot_col)) # NOTE: Pylance didn't like this...

    # Create one robot sprite.
    robot = Robot(robot_row, robot_col)

    _game_is_running = True

    while _game_is_running:
        # Process window/input events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _game_is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    _game_is_running = False

        # Clear the actual window.
        screen.fill((18, 23, 34))

        # Clear the offscreen maze surface.
        level_surface.fill((18, 23, 34))

        # Draw every tile sprite onto the offscreen maze surface.
        tiles.draw(level_surface)

        # Draw the robot on top of the maze tiles.
        level_surface.blit(robot.image, robot.rect)

        # Figure out how large the maze should appear inside the window.
        scaled_level_rect = get_scaled_level_rect(level_surface, screen)

        # Scale the maze surface to fit inside the actual window.
        scaled_level_surface = pygame.transform.scale(
            level_surface,
            scaled_level_rect.size
        )

        #scaled_level_surface = pygame.transform.scale_by(
        #level_surface,
        #scaled_level_rect.width // level_surface.get_width()
        #)


        # Draw the scaled maze surface onto the centered position in the window.
        screen.blit(scaled_level_surface, scaled_level_rect)

        # Show the completed frame.
        pygame.display.flip()

        # Keep the loop from running too fast.
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
