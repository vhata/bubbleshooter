import pygame
import math
from typing import Optional
from bubble import Bubble, BubbleColor, BubbleState

class Shooter:
    def __init__(self, x: float, y: float, bubble_size: int = 40) -> None:
        self.x = x
        self.y = y
        self.bubble_size = bubble_size
        self.angle = 0.0  # Angle in radians
        self.current_bubble: Optional[Bubble] = None
        self.next_bubble: Optional[Bubble] = None
        self.shoot_speed = 15
        self.prepare_bubbles()
    
    def prepare_bubbles(self) -> None:
        """Prepare current and next bubble"""
        if self.current_bubble is None:
            self.current_bubble = Bubble(self.x, self.y)
        if self.next_bubble is None:
            self.next_bubble = Bubble(self.x + self.bubble_size * 2, self.y)
    
    def update(self, mouse_pos: tuple[int, int]) -> None:
        """Update shooter angle based on mouse position"""
        dx = mouse_pos[0] - self.x
        dy = self.y - mouse_pos[1]  # Subtract for upward direction
        self.angle = math.atan2(dy, dx)
        
        # Clamp angle to prevent shooting downward
        min_angle = -math.pi * 0.8  # About -145 degrees
        max_angle = math.pi * 0.8   # About 145 degrees
        self.angle = max(min_angle, min(self.angle, max_angle))
        
        # Update current bubble position
        if self.current_bubble is not None and self.current_bubble.state == BubbleState.FIXED:
            self.current_bubble.x = self.x
            self.current_bubble.y = self.y
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the shooter and current/next bubbles"""
        # Draw shooter base (circle)
        pygame.draw.circle(screen, (100, 100, 100), (int(self.x), int(self.y)), self.bubble_size // 2)
        
        # Draw shooter barrel
        end_x = self.x + self.bubble_size * math.cos(self.angle)
        end_y = self.y - self.bubble_size * math.sin(self.angle)  # Subtract for upward direction
        pygame.draw.line(screen, (150, 150, 150), 
                        (int(self.x), int(self.y)), 
                        (int(end_x), int(end_y)), 4)
        
        # Draw current and next bubbles
        if self.current_bubble is not None and self.current_bubble.state == BubbleState.FIXED:
            self.current_bubble.draw(screen)
        if self.next_bubble is not None:
            self.next_bubble.draw(screen)
    
    def shoot(self) -> Optional[Bubble]:
        """Shoot the current bubble"""
        if self.current_bubble is not None and self.current_bubble.state == BubbleState.FIXED:
            # Calculate velocity based on angle
            speed = self.shoot_speed
            dx = speed * math.cos(self.angle)
            dy = -speed * math.sin(self.angle)  # Negative for upward movement
            
            # Set bubble in motion
            self.current_bubble.set_velocity(dx, dy)
            
            # Move next bubble to current and create new next bubble
            shot_bubble = self.current_bubble
            self.current_bubble = self.next_bubble
            self.next_bubble = Bubble(self.x + self.bubble_size * 2, self.y)
            
            # Position new current bubble at shooter
            if self.current_bubble is not None:
                self.current_bubble.x = self.x
                self.current_bubble.y = self.y
            return shot_bubble
        return None 