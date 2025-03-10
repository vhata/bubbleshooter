import math
from typing import Optional

import pygame
from bubble import Bubble


class Grid:
    def __init__(self, width: int, height: int, bubble_size: int = 40) -> None:
        self.width = width
        self.height = height
        self.bubble_size = bubble_size
        self.grid_height = height // bubble_size
        self.grid_width = width // bubble_size
        self.bubbles: list[list[Optional[Bubble]]] = [
            [None] * self.grid_width for _ in range(self.grid_height)
        ]
        self.init_grid()

    def init_grid(self) -> None:
        """Initialize the top few rows with bubbles"""
        for row in range(4):  # Start with 4 rows of bubbles
            for col in range(self.grid_width):
                # Offset even rows
                x = col * self.bubble_size + (self.bubble_size // 2 if row % 2 else 0)
                y = row * (self.bubble_size - 10)  # Overlap bubbles vertically
                if x + self.bubble_size <= self.width:  # Ensure bubble fits in grid
                    self.bubbles[row][col] = Bubble(x, y)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw all bubbles in the grid"""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                bubble = self.bubbles[row][col]
                if bubble:
                    bubble.draw(screen)

    def get_grid_pos(self, x: float, y: float) -> tuple[int, int]:
        """Convert pixel coordinates to grid coordinates"""
        row = int(y / (self.bubble_size - 10))
        # Account for offset in even rows
        if row % 2 == 0:
            col = int(x / self.bubble_size)
        else:
            col = int((x - self.bubble_size // 2) / self.bubble_size)
        return row, col

    def add_bubble(self, bubble: Bubble) -> bool:
        """Add a bubble to the grid at the nearest valid position"""
        row, col = self.get_grid_pos(bubble.x, bubble.y)

        # Ensure position is within grid bounds
        if not (0 <= row < self.grid_height and 0 <= col < self.grid_width):
            return False

        # Adjust bubble position to grid
        x = col * self.bubble_size + (self.bubble_size // 2 if row % 2 else 0)
        y = row * (self.bubble_size - 10)

        # Update bubble position and state
        bubble.x = x
        bubble.y = y
        bubble.stop()

        # Add to grid
        self.bubbles[row][col] = bubble
        return True

    def check_matches(self, row: int, col: int) -> set[tuple[int, int]]:
        """Find all matching bubbles connected to the given position"""
        if not (0 <= row < self.grid_height and 0 <= col < self.grid_width):
            return set()

        bubble = self.bubbles[row][col]
        if not bubble:
            return set()

        color = bubble.color
        visited: set[tuple[int, int]] = set()
        matches: set[tuple[int, int]] = set()

        def flood_fill(r: int, c: int) -> None:
            if not (0 <= r < self.grid_height and 0 <= c < self.grid_width):
                return
            if (r, c) in visited:
                return
            visited.add((r, c))

            current = self.bubbles[r][c]
            if not current or current.color != color:
                return

            matches.add((r, c))

            # Check all 6 directions
            directions: list[tuple[int, int]] = [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 0),
                (1, -1),
                (0, -1),
            ]
            # Adjust for even/odd rows
            if r % 2 == 0:
                directions = [(-1, -1), (-1, 0), (0, 1), (1, -1), (1, 0), (0, -1)]

            for dr, dc in directions:
                flood_fill(r + dr, c + dc)

        flood_fill(row, col)
        return matches

    def remove_matches(self, matches: set[tuple[int, int]]) -> None:
        """Remove matched bubbles and handle floating bubbles"""
        if len(matches) >= 3:  # Only remove if 3 or more matches
            for row, col in matches:
                self.bubbles[row][col] = None
            self.handle_floating_bubbles()

    def handle_floating_bubbles(self) -> None:
        """Find and remove bubbles that are not connected to the top"""
        # First, find all bubbles connected to the top row
        anchored: set[tuple[int, int]] = set()

        def flood_fill_anchored(row: int, col: int) -> None:
            if not (0 <= row < self.grid_height and 0 <= col < self.grid_width):
                return
            if (row, col) in anchored:
                return
            if not self.bubbles[row][col]:
                return

            anchored.add((row, col))

            # Check all 6 directions
            directions: list[tuple[int, int]] = [
                (-1, 0),
                (-1, 1),
                (0, 1),
                (1, 0),
                (1, -1),
                (0, -1),
            ]
            # Adjust for even/odd rows
            if row % 2 == 0:
                directions = [(-1, -1), (-1, 0), (0, 1), (1, -1), (1, 0), (0, -1)]

            for dr, dc in directions:
                flood_fill_anchored(row + dr, col + dc)

        # Start from top row
        for col in range(self.grid_width):
            if self.bubbles[0][col]:
                flood_fill_anchored(0, col)

        # Remove unanchored bubbles
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.bubbles[row][col] and (row, col) not in anchored:
                    bubble = self.bubbles[row][col]
                    if bubble:
                        bubble.start_falling()
                    self.bubbles[row][col] = None

    def update(self) -> None:
        """Update all bubbles in the grid"""
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                bubble = self.bubbles[row][col]
                if bubble:
                    bubble.update()

    def check_collision(self, bubble: Bubble) -> tuple[bool, Optional[tuple[int, int]]]:
        """
        Check if a moving bubble collides with any bubbles in the grid.
        Returns (collision_detected, grid_position)
        where grid_position is the nearest empty grid position to place the bubble.
        """
        # First check if we hit the top of the grid
        if bubble.y < self.bubble_size:
            row = 0
            col = int(bubble.x / self.bubble_size)
            if row % 2 == 1:
                col = int((bubble.x - self.bubble_size / 2) / self.bubble_size)
            return True, (row, max(0, min(col, self.grid_width - 1)))

        # Check collision with existing bubbles
        radius = int(
            (self.bubble_size - 4) / 2
        )  # Slightly smaller than bubble size for better gameplay
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                grid_bubble = self.bubbles[row][col]
                if grid_bubble is not None:
                    # Calculate distance between centers
                    dx = bubble.x - grid_bubble.x
                    dy = bubble.y - grid_bubble.y
                    distance = math.sqrt(dx * dx + dy * dy)

                    if distance < radius * 2:  # Collision detected
                        # Find the nearest empty grid position
                        return True, self._find_nearest_empty_position(row, col, bubble)

        return False, None

    def _find_nearest_empty_position(
        self, row: int, col: int, bubble: Bubble
    ) -> tuple[int, int]:
        """Find the nearest empty grid position to place a bubble after collision."""
        # Check all six adjacent positions
        directions = [(-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1), (0, -1)]
        if row % 2 == 0:
            directions = [(-1, -1), (-1, 0), (0, 1), (1, -1), (1, 0), (0, -1)]

        # Find the closest empty position
        min_distance = float("inf")
        best_position = (row, col)  # Default to current position if no empty spots

        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc

            if (
                0 <= new_row < self.grid_height
                and 0 <= new_col < self.grid_width
                and self.bubbles[new_row][new_col] is None
            ):

                # Calculate position in pixels
                x = new_col * self.bubble_size
                if new_row % 2 == 1:
                    x += int(self.bubble_size / 2)
                y = new_row * (self.bubble_size - 10)

                # Calculate distance to bubble's current position
                dx = x - bubble.x
                dy = y - bubble.y
                distance = dx * dx + dy * dy  # No need for sqrt here

                if distance < min_distance:
                    min_distance = distance
                    best_position = (new_row, new_col)

        return best_position
