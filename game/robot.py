"""Robot sprite logic for RescueBot."""

import pygame

from game.settings import ASSET_DIR, TILE_SIZE


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


    def move_to(self, row: int, col: int) -> None:
        """Move the robot to a new grid position.

        Args:
            row: The robot's new row.
            col: The robot's new column.
        """
        # Update the robot's logical grid position.
        self.row = row
        self.col = col

        # Update the robot's pixel position so Pygame draws it in the right spot.
        self.rect.topleft = (
            self.col * TILE_SIZE,
            self.row * TILE_SIZE
        )
