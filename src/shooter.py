import pygame
import math
from bubble import Bubble, BubbleColor, BubbleState

class Shooter:
    def __init__(self, x, y, bubble_size=40):
        self.x = x
        self.y = y
        self.bubble_size = bubble_size
        self.angle = -90  # Start pointing straight up
        self.current_bubble = None
        self.next_bubble = None
        self.shoot_speed = 15
        self.prepare_bubbles()
    
    def prepare_bubbles(self):
        """Prepare current and next bubble"""
        if not self.current_bubble:
            self.current_bubble = Bubble(self.x, self.y)
        if not self.next_bubble:
            self.next_bubble = Bubble(self.x + self.bubble_size * 2, self.y)
    
    def update(self, mouse_pos):
        """Update shooter angle based on mouse position"""
        dx = mouse_pos[0] - self.x
        dy = self.y - mouse_pos[1]  # Inverted y-axis for upward aiming
        # Calculate angle in degrees
        self.angle = math.degrees(math.atan2(dy, dx))
        # Clamp angle between 30 and 150 degrees (for upward shooting)
        self.angle = max(30, min(150, self.angle))
        
        # Update current bubble position
        if self.current_bubble and self.current_bubble.state == BubbleState.FIXED:
            self.current_bubble.x = self.x
            self.current_bubble.y = self.y
    
    def draw(self, screen):
        """Draw the shooter and current/next bubbles"""
        # Draw shooter base (circle)
        pygame.draw.circle(screen, (100, 100, 100), (self.x, self.y), self.bubble_size // 2)
        
        # Draw shooter barrel
        angle_rad = math.radians(self.angle)
        barrel_length = self.bubble_size
        end_x = self.x + math.cos(angle_rad) * barrel_length
        end_y = self.y - math.sin(angle_rad) * barrel_length  # Subtract for upward direction
        pygame.draw.line(screen, (150, 150, 150), 
                        (self.x, self.y), (end_x, end_y), 4)
        
        # Draw current and next bubbles
        if self.current_bubble and self.current_bubble.state == BubbleState.FIXED:
            self.current_bubble.draw(screen)
        if self.next_bubble:
            self.next_bubble.draw(screen)
    
    def shoot(self):
        """Shoot the current bubble"""
        if self.current_bubble and self.current_bubble.state == BubbleState.FIXED:
            # Calculate velocity based on angle
            angle_rad = math.radians(self.angle)
            dx = math.cos(angle_rad) * self.shoot_speed
            dy = -math.sin(angle_rad) * self.shoot_speed  # Negative for upward movement
            
            # Set bubble in motion
            self.current_bubble.set_velocity(dx, dy)
            
            # Move next bubble to current and create new next bubble
            self.current_bubble = self.next_bubble
            self.next_bubble = Bubble(self.x + self.bubble_size * 2, self.y)
            
            # Position new current bubble at shooter
            self.current_bubble.x = self.x
            self.current_bubble.y = self.y
            return True
        return False 