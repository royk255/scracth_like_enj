import pygame
import sys
import copy
# Setup


FULL_SCREEN_WIDTH = 1920
FULL_SCREEN_HEIGHT = 1080
HALF_SCREEN_WIDTH =  FULL_SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = FULL_SCREEN_HEIGHT // 2

pygame.init()
screen = pygame.display.set_mode((FULL_SCREEN_WIDTH,  FULL_SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snapping Blocks")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)

# Font
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)

blocks = []

line = pygame.Rect(1600, 0, 20, 1080)  # Vertical line on the right
SAFE_BLOCKS_LOC = line.x + 50 

# Block class
class Block:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, 150, 50)
        self.text = text
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=10)
        label = FONT.render(self.text, True, WHITE)
        surface.blit(label, (self.rect.x + 10, self.rect.y + 15))

    def handle_event(self, event, blocks):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.rect.x < SAFE_BLOCKS_LOC:
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
                else:
                    blocks.append(Block(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT, self.text))

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.snap_to_blocks(blocks)
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self.offset_x
                self.rect.y = mouse_y + self.offset_y

    def snap_to_blocks(self, blocks):
        for block in blocks:
            if block is not self:
                dx = abs(self.rect.x - block.rect.x)
                dy = abs(self.rect.y - (block.rect.y + block.rect.height))
                if dx < 20 and dy < 20:
                    self.rect.x = block.rect.x
                    self.rect.y = block.rect.y + block.rect.height

# Create blocks


# Draw the vertical line in the main loop
def draw_vertical_line(surface):
    pygame.draw.rect(surface, (0, 0, 0), line)
    #line_label = FONT.render("Vertical Line", True, WHITE)
    #surface.blit(line_label, (line.x + 10, line.y + 10))

# Add the draw function to the main loop
def draw_elements(surface):
    for block in blocks:
        block.draw(surface)
    draw_vertical_line(surface)

blocks_text = [
    "Move 10 Steps",
    "Jump",
    "Turn Left",
    "Turn Right",
    "Move Backward"
]

for i in range(len(blocks_text)):
    x = SAFE_BLOCKS_LOC   # Adjust x position for each block
    y = 20 + (i * 60)  # Fixed y position
    blocks.append(Block(x, y, blocks_text[i]))

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for block in blocks:
            block.handle_event(event, blocks)

    for block in blocks:
        block.draw(screen)
    draw_vertical_line(screen)
    
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
