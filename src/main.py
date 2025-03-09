import pygame
import sys
from typing import Optional
from bubble import Bubble, BubbleState
from grid import Grid
from shooter import Shooter

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 40  # Size of each bubble
GRID_ROWS = 12
GRID_COLS = 15
SHOOTER_HEIGHT = 100  # Height of the shooter area at bottom
TITLE = "Bubble Shooter"
FPS = 60

# Colors (type: tuple[int, int, int])
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (30, 30, 50)  # Dark blue-ish
GRID_COLOR = (50, 50, 70)  # Slightly lighter than background
SHOOTER_AREA_COLOR = (40, 40, 60)  # Medium blue-ish

class Game:
    def __init__(self, width: int = 800, height: int = 600) -> None:
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Bubble Shooter")
        
        # Create game objects
        self.grid = Grid(width, height - 100)  # Reserve bottom 100px for shooter
        self.shooter = Shooter(width // 2, height - 50, GRID_SIZE)
        
        # Game state
        self.moving_bubbles: list[Bubble] = []
        self.falling_bubbles: list[Bubble] = []
        self.clock = pygame.time.Clock()
        self.running = True

    def handle_events(self) -> None:
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    shot_bubble = self.shooter.shoot()
                    if shot_bubble:
                        self.moving_bubbles.append(shot_bubble)

    def update(self) -> None:
        """Update game state"""
        # Update shooter
        mouse_pos = pygame.mouse.get_pos()
        self.shooter.update(mouse_pos)
        
        # Update moving bubbles
        for bubble in self.moving_bubbles[:]:
            bubble.update()
            
            # Check for collisions with walls
            if bubble.x < 20 or bubble.x > self.width - 20:
                bubble.velocity[0] *= -1  # Reverse horizontal direction
            
            # Check for collisions with grid bubbles
            collision, grid_pos = self.grid.check_collision(bubble)
            if collision and grid_pos is not None:
                # Add bubble to grid at the nearest empty position
                self.moving_bubbles.remove(bubble)
                self.grid.add_bubble(bubble)
                self.check_matches(bubble)
                
        # Update falling bubbles
        for bubble in self.falling_bubbles[:]:
            bubble.update()
            if bubble.y > self.height:
                self.falling_bubbles.remove(bubble)

    def check_matches(self, bubble: Bubble) -> None:
        """Check for matching bubbles after a collision"""
        grid_pos = self.grid.get_grid_pos(bubble.x, bubble.y)
        matches = self.grid.check_matches(grid_pos[0], grid_pos[1])
        self.grid.remove_matches(matches)

    def draw(self) -> None:
        """Draw game state"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw grid
        self.grid.draw(self.screen)
        
        # Draw shooter
        self.shooter.draw(self.screen)
        
        # Draw moving bubbles
        for bubble in self.moving_bubbles:
            bubble.draw(self.screen)
            
        # Draw falling bubbles
        for bubble in self.falling_bubbles:
            bubble.draw(self.screen)
        
        # Update display
        pygame.display.flip()

    def run(self) -> None:
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

def main() -> None:
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 