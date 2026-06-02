"""Program entry point for RescueBot.

This file stays intentionally small. Its job is only to create the game object
and start the main game loop.
"""

import sys

import pygame

from game.level import (
    LEVEL,
    build_tiles,
    can_move_to,
    find_tile,
    get_level_size,
    get_scaled_level_rect,
)
from game.robot import Robot
from game.settings import (
    FPS,
    ROBOT_START,
    WINDOW_HEIGHT,
    WINDOW_TITLE,
    WINDOW_WIDTH,
)


#-------------------------------------------------------------------------------


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


def get_move_direction(key: int) -> tuple[int, int] | None:
    """Convert a keyboard key into a row/column movement direction.

    Args:
        key: The Pygame key constant from a KEYDOWN event.

    Returns:
        A tuple of (row_change, col_change), or None if the key is not movement.
    """
    if key in (pygame.K_UP, pygame.K_w):
        return (-1, 0)

    if key in (pygame.K_DOWN, pygame.K_s):
        return (1, 0)

    if key in (pygame.K_LEFT, pygame.K_a):
        return (0, -1)

    if key in (pygame.K_RIGHT, pygame.K_d):
        return (0, 1)

    return None


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

                else:
                    direction = get_move_direction(event.key)

                    if direction is not None:
                        row_change, col_change = direction

                        next_row = robot.row + row_change
                        next_col = robot.col + col_change

                        if can_move_to(LEVEL, next_row, next_col):
                            robot.move_to(next_row, next_col)

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
