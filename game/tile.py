"""Tile sprite logic for RescueBot."""

import pygame

from game.settings import ASSET_DIR, COLORS, TILE_IMAGES, TILE_SIZE


class Tile(pygame.sprite.Sprite):
    """One tile on the maze grid.

    A Tile is a visible square on the map, such as a floor tile, wall tile,
    or charging station tile.
    """

    def __init__(self, tile_type: int, row: int, col: int) -> None:
        """Create a tile at a specific grid position.

        Args:
            tile_type: The kind of tile, such as floor, wall, or charger.
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
