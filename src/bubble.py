import math
import random
from enum import Enum
from typing import Optional

import pygame


class BubbleColor(Enum):
    RED = (255, 50, 50)
    BLUE = (50, 50, 255)
    GREEN = (50, 255, 50)
    YELLOW = (255, 255, 50)
    PURPLE = (255, 50, 255)
    CYAN = (50, 255, 255)


class BubbleState(Enum):
    FIXED = "fixed"  # Bubble is fixed in the grid
    FALLING = "falling"  # Bubble is falling (after group pop)
    MOVING = "moving"  # Bubble is moving (shot from cannon)


class Bubble:
    def __init__(
        self, x: float, y: float, color: Optional[BubbleColor] = None, size: int = 40
    ) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.color = color if color else random.choice(list(BubbleColor))
        self.state = BubbleState.FIXED
        self.velocity: list[float] = [0, 0]  # For moving bubbles [dx, dy]

    def draw(self, screen: pygame.Surface) -> None:
        # Draw filled bubble
        points = self.calculate_hexagon()
        pygame.draw.polygon(screen, self.color.value, points)
        # Draw outline slightly darker than the fill color
        darker_color = tuple(max(0, c - 50) for c in self.color.value)
        pygame.draw.polygon(screen, darker_color, points, 2)

    def calculate_hexagon(self) -> list[tuple[float, float]]:
        """Calculate the points for a hexagonal bubble"""
        points: list[tuple[float, float]] = []
        # Size is slightly smaller than grid size for visual spacing
        radius = (self.size // 2) - 2
        for i in range(6):
            angle_deg = 60 * i - 30  # -30 to point hexagon upward
            angle_rad = math.pi / 180 * angle_deg
            points.append(
                (
                    self.x + radius * math.cos(angle_rad),
                    self.y + radius * math.sin(angle_rad),
                )
            )
        return points

    def update(self) -> None:
        """Update bubble position based on state and velocity"""
        if self.state == BubbleState.MOVING:
            self.x += self.velocity[0]
            self.y += self.velocity[1]
        elif self.state == BubbleState.FALLING:
            self.velocity[1] += 0.5  # Add gravity
            self.x += self.velocity[0]
            self.y += self.velocity[1]

    def set_velocity(self, dx: float, dy: float) -> None:
        """Set the bubble's velocity for moving bubbles"""
        self.velocity = [dx, dy]
        self.state = BubbleState.MOVING

    def stop(self) -> None:
        """Stop the bubble's movement and fix it in place"""
        self.velocity = [0, 0]
        self.state = BubbleState.FIXED

    def start_falling(self) -> None:
        """Make the bubble start falling"""
        self.state = BubbleState.FALLING
        self.velocity = [
            random.uniform(-2, 2),
            0,
        ]  # Add slight random horizontal movement
