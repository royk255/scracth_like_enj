import pygame
import sys
import os
import defines
#from button_class import Button
import button_class



os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((defines.FULL_SCREEN_WIDTH,  defines.FULL_SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snapping Blocks")
clock = pygame.time.Clock()

action = False

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height()), pygame.SRCALPHA).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)


# Font
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)

blocks = []
list_of_characters = []

line = pygame.Rect(1600, 0, 20, 1080)  # Vertical line on the right
SAFE_BLOCKS_LOC = line.x + 50 

#green_button = pygame.Rect(defines.HALF_SCREEN_WIDTH-300, 50, 50, 50)  # x, y, width, height
#red_button = pygame.Rect(defines.HALF_SCREEN_WIDTH-225, 50, 50, 50)

green_button = button_class.Button(defines.HALF_SCREEN_WIDTH-300, 50, 50, 50, "Run")
red_button = button_class.Button(defines.HALF_SCREEN_WIDTH-225, 50, 50, 50, "Stop")



class Block:
    def __init__(self, x, y, text, type, size, color=defines.BLUE):
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.text = text
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.color = color
        self.type = type

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        label = FONT.render(self.text, True, defines.WHITE)
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
                    blocks.append(Block(defines.HALF_SCREEN_WIDTH, defines.HALF_SCREEN_HEIGHT, self.text, self.type, (150, 50), self.color))

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
    
    def get_input(self):
        screen_input = pygame.display.set_mode((300, 200), pygame.RESIZABLE)
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(50, 100, 140, 32)
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
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            print(text)
                            self.param1 = text
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen_input.fill(defines.WHITE)
            # Render and blit the label so it's visible
            label = FONT.render("Enter a value:", True, defines.BLACK)
            screen_input.blit(label, (50, 50))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            screen_input.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(screen_input, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

    def logic(self):
        pass
    



class BlockType(Block):
    def __init__(self, x, y, text, type, size, color=defines.BLUE):
        super().__init__(x, y, text, type, size, color) 
        self.type = type

    def logic(self):
        # Implement specific logic for different block types if needed
        pass


class Character:
    def __init__(self, image_path, x=0, y=0, rotation=0, scale=1.0, facing_right=True):
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.character_name = os.path.splitext(os.path.basename(image_path))[0]
        self.scale = scale
        if scale != 1.0:
            w, h = self.image_original.get_size()
            self.image_original = pygame.transform.smoothscale(
                self.image_original, (int(w * scale), int(h * scale))
            )
        self.facing_right = facing_right
        self.image = self.image_original
        self.x = x
        self.y = y
        self.rotation = rotation
        self.update_rect()
        self.cmds = []

    def update_rect(self):
        img = pygame.transform.rotate(self.image_original, -self.rotation)
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)
        self.image = img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        self.image.set_alpha(255)
        if self.facing_right:
            #blit_alpha(surface, self.image, (self.x, self.y), 255)
            surface.blit(self.image, (self.x, self.y))
        else:
            #blit_alpha(surface, pygame.transform.flip(self.image, True, False), (self.x, self.y), 255)
            surface.blit(pygame.transform.flip(self.image, True, False), (self.x, self.y))
        #surface.blit(self.image, (self.x, self.y))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.update_rect()

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_rect()

    def set_rotation(self, angle):
        self.rotation = angle % 360
        self.update_rect()

    def flip(self):
        self.facing_right = not self.facing_right
        self.update_rect()

    def set_direction(self, right=True):
        self.facing_right = right
        self.update_rect()

    def get_direction(self):
        return "right" if self.facing_right else "left"

    def get_hitbox(self):
        return self.rect

    def collides_with(self, other_rect):
        return self.rect.colliderect(other_rect)

list_of_characters.append(Character("C:\\Data\\roy\\my_projects\\game_enj_sc_like\\scracth_like_enj\\defult_character_2.png", 0, 0))


class move_character(BlockType):
    def __init__(self, x, y, size, character, color=defines.BLUE):
        super().__init__(x, y, "move_character", "Motion", size, color)
        self.character = character
        self.param1 = 10
        self.has_param = 1

    def start(self):
        self.get_input()
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 10")
            self.param1 = 10
        print(self.param1)
    
    def logic(self):
        Character.move(self.character, self.param1, 0)
        



class turn_character(BlockType):
    def __init__(self, x, y, size, character, color=defines.BLUE):
        super().__init__(x, y, "turn_character", "Motion", size, color)
        self.character = character
        self.param1 = 10
        self.has_param = 1

    def start(self):
        self.get_input()
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 10")
            self.param1 = 10
        print(self.param1)

    def logic(self):
        print(self.param1)
        pass


blocks_text = [
    "Move 10 Steps",
    "Jump",
    "Turn Left",
    "Turn Right",
    "Move Backward"
]
def add_blocks():
    for i in range(len(blocks_text)):
        x = SAFE_BLOCKS_LOC 
        y = 20 + (i * 60)  
        if blocks_text[i] == "Move 10 Steps":
            blocks.append(move_character(x, y, (150, 50), list_of_characters[0]))
        elif blocks_text[i] == "Turn Left":
            blocks.append(turn_character(x, y, (150, 50), list_of_characters[0]))
        else:
            blocks.append(BlockType(x, y, blocks_text[i], "Motion", (150, 50)))


def draw_other_blocks():
    pygame.draw.rect(screen, defines.BLACK, line)
    #pygame.draw.rect(screen, defines.GREEN, green_button)  # Green button
    #pygame.draw.rect(screen, defines.RED, red_button)    # Red button
    green_button.draw(screen)
    red_button.draw(screen)

def action_button(event):
    green_button.handle_event(event)
    if green_button.on:
        global action
        action = True
        print("Action button pressed, starting logic execution.")
        green_button.turn_off()
        red_button.turn_off()
    red_button.handle_event(event)
    if red_button.on:
        action = False
        print("Action button released, stopping logic execution.")
        green_button.turn_off()
        red_button.turn_off()


def main():
    running = True
    add_blocks()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for block in blocks:
                block.handle_event(event, blocks)

            action_button(event)

        screen.fill(defines.WHITE)
        for block in blocks:
            block.draw(screen)
        for character in list_of_characters:
            character.draw(screen)

        # Draw the vertical line
        #pygame.draw.rect(screen, defines.BLACK, line)
        draw_other_blocks()

        #play logic for each block

        if action:
            for block in blocks:
                if isinstance(block, move_character):
                    block.logic()
                elif isinstance(block, turn_character):
                    block.logic()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
"""
pygame.init()
bla =  move_character(100, 100, (150, 50), list_of_characters[0])
bla.logic()
pygame.quit()
sys.exit()
"""
if __name__ == "__main__":
    main()