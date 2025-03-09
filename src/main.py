import pygame
import sys
import math
from bubble import Bubble, BubbleColor

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

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BACKGROUND_COLOR = (30, 30, 50)  # Dark blue-ish
GRID_COLOR = (50, 50, 70)  # Slightly lighter than background
SHOOTER_AREA_COLOR = (40, 40, 60)  # Medium blue-ish

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Calculate grid offset to center it
        self.grid_offset_x = (WINDOW_WIDTH - (GRID_COLS * GRID_SIZE)) // 2
        self.grid_offset_y = 20  # Small margin from top
        
        # Initialize grid with some test bubbles
        self.bubbles = []
        self.initialize_test_bubbles()

    def initialize_test_bubbles(self):
        # Add some test bubbles in the first few rows
        for row in range(5):  # First 5 rows
            for col in range(GRID_COLS):
                # Calculate bubble position
                x = self.grid_offset_x + col * GRID_SIZE
                if row % 2 == 1:
                    x += GRID_SIZE // 2
                y = self.grid_offset_y + row * (GRID_SIZE - 10)
                
                # Create bubble with random color
                bubble = Bubble(x + GRID_SIZE//2, y + GRID_SIZE//2)
                self.bubbles.append(bubble)

    def draw_grid(self):
        # Draw the hexagonal grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                # Offset every other row
                x = self.grid_offset_x + col * GRID_SIZE
                if row % 2 == 1:
                    x += GRID_SIZE // 2
                y = self.grid_offset_y + row * (GRID_SIZE - 10)  # Overlap rows slightly
                
                # Draw hexagon outline
                points = self.calculate_hexagon(x + GRID_SIZE//2, y + GRID_SIZE//2, GRID_SIZE//2 - 2)
                pygame.draw.polygon(self.screen, GRID_COLOR, points, 1)

    def calculate_hexagon(self, x, y, size):
        points = []
        for i in range(6):
            angle_deg = 60 * i - 30  # -30 to point hexagon upward
            angle_rad = math.pi / 180 * angle_deg
            points.append((x + size * math.cos(angle_rad),
                         y + size * math.sin(angle_rad)))
        return points

    def draw_shooter_area(self):
        # Draw shooter area at bottom
        shooter_rect = pygame.Rect(0, WINDOW_HEIGHT - SHOOTER_HEIGHT,
                                 WINDOW_WIDTH, SHOOTER_HEIGHT)
        pygame.draw.rect(self.screen, SHOOTER_AREA_COLOR, shooter_rect)
        # Draw a line to separate shooter area
        pygame.draw.line(self.screen, GRID_COLOR,
                        (0, WINDOW_HEIGHT - SHOOTER_HEIGHT),
                        (WINDOW_WIDTH, WINDOW_HEIGHT - SHOOTER_HEIGHT), 2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        # Update all bubbles
        for bubble in self.bubbles:
            bubble.update()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid()
        # Draw all bubbles
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        self.draw_shooter_area()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 