import pygame
import sys


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


class Block:
    def __init__(self, x, y, text, type, size, color=BLUE):
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.text = text
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.color = color
        self.type = type

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
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

    def logic(self):
        pass
    

class BlockType(Block):
    def __init__(self, x, y, text, type, size, color=BLUE):
        super().__init__(x, y, text, type, size, color)
        self.type = type

    def logic(self):
        # Implement specific logic for different block types if needed
        pass



class character(BlockType):
    def __init__(self, x, y, text, size, color=BLUE):
        super().__init__(x, y, text, "character", size, color)

    def logic(self):
        # Implement specific logic for character block
        pass



class move_character(BlockType):
    def __init__(self, x, y, text, size, color=BLUE):
        super().__init__(x, y, text, "move_character", size, color)
        self.param1 = 10

    def get_input(self):
        screen = pygame.display.set_mode((640, 480))
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(100, 100, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(text)
                            self.param1 = text  # Store the input value in the block's parameter
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill((30, 30, 30))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def logic(self):
        self.get_input()
        print(self.param1)
        pass


pygame.init()
bla =  move_character(100, 100, "Move Character", (150, 50))
bla.logic()
pygame.quit()
sys.exit()