import pygame
import defines
import os
import sys
import block_classes
import time


class Block:
    def __init__(self, x, y, text, type, size, color=defines.BLUE):
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.text = text
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.color = color
        self.type = type

    def dup(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        label = defines.FONT.render(self.text, True, defines.WHITE)
        surface.blit(label, (self.rect.x + 10, self.rect.y + 15))

    def handle_event(self, event, blocks):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.rect.x < defines.SAFE_BLOCKS_LOC:
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset_x = self.rect.x - mouse_x
                    self.offset_y = self.rect.y - mouse_y
                else:
                    #blocks.append(Block(defines.HALF_SCREEN_WIDTH, defines.HALF_SCREEN_HEIGHT, self.text, self.type, (150, 50), self.character, self.color))
                    new_block = self.dup()
                    new_block.update_position(defines.HALF_SCREEN_WIDTH, defines.HALF_SCREEN_HEIGHT)
                    blocks.append(new_block)
            return 3

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                #self.snap_to_blocks(blocks)
                self.dragging = False
                return 1
            self.dragging = False
            return 0

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                #mouse_x, mouse_y = event.pos
                #self.rect.x = mouse_x + self.offset_x
                #self.rect.y = mouse_y + self.offset_y
                return 2
            
    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    def get_position(self):
        return self.rect.x, self.rect.y

    def logic(self, target):
        pass

    def start(self):
        pass

    def get_skip(self):
        return False


class BlockType(Block):
    def __init__(self, x, y, text, type, size, color=defines.BLUE):
        super().__init__(x, y, text, type, size, defines.types_colors[type.lower()]) 
        self.type = type

    def logic(self):
        # Implement specific logic for different block types if needed
        pass

    def start(self):
        pass


class move_character(BlockType):
    def __init__(self, x, y, size):
        super().__init__(x, y, "move_character", "Motion", size)
        self.param1 = 100
        self.has_param = 1
    
    def get_par(self):
        return {"steps" : self.param1}
    
    def dup(self):
        return move_character(self.rect.x, self.rect.y, self.rect.size)

    def start(self, parm):
        self.param1 = parm["steps"]
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 100")
            self.param1 = 100
        print(self.param1)
    
    def logic(self, target):
        target.move(self.param1, 0)
        



class turn_character(BlockType):
    def __init__(self, x, y, size):
        super().__init__(x, y, "turn_character", "Motion", size)
        self.param1 = 10
        self.has_param = 1

    def dup(self):
        return turn_character(self.rect.x, self.rect.y, self.rect.size)

    def start(self):
        self.get_input()
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 10")
            self.param1 = 10
        print(self.param1)

    def logic(self, target):
        print(self.param1)
        pass


class jump_character(BlockType):
    def __init__(self, x, y, size):
        super().__init__(x, y, "jump_character", "Motion", size)
        self.param1 = 100
        self.has_param = 1

    def dup(self):
        return jump_character(self.rect.x, self.rect.y, self.rect.size)
    
    def get_par(self):
        return {"steps" : self.param1}

    def start(self):
        self.get_input()
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 100")
            self.param1 = 100
        #print(self.param1)

    def logic(self, target):
        #print(self.param1)
        for i in range(self.param1):
            target.move(0, 1)
        for i in range(self.param1):
            target.move(0, -1)

class wait_character(BlockType):
    def __init__(self, x, y, size):
        super().__init__(x, y, "wait_character", "Control", size)
        self.param1 = 1
        self.has_param = 1

    def get_par(self):
        return {"wait" : self.param1}

    def dup(self):
        return wait_character(self.rect.x, self.rect.y, self.rect.size)   

    def start(self, parm_dic):
        self.param1 = parm_dic["wait"]
        if self.param1.isdigit():
            self.param1 = int(self.param1)
        else:
            print("Invalid input, using default value of 1000")
            self.param1 = 1

    def logic(self, target):
        #time.sleep(self.param1)
        pygame.time.delay(self.param1 * 1000)




