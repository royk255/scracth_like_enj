import pygame
import os
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
    
    def print_cmds(self):
        print(f"Commands for {self.character_name}:")
        for cmd in self.cmds:
            print(cmd)
            #print("cmd length:", len(cmd))
        #print("-----------------------")
        print(self.cmds)

    def snap_to_blocks(self, block):
        blocks = []
        for li in self.cmds:
            _block = li[-1]
            if _block == block:
                continue
            dx = abs(block.rect.x - _block.rect.x)
            dy = abs(block.rect.y - (_block.rect.y + _block.rect.height))
            if dx < 20 and dy < 20:
                block.rect.x = _block.rect.x
                block.rect.y = _block.rect.y + _block.rect.height
                #self.character.cmds[0].append #----
                self.stack_block(block,_block, True)
                return
        self.stack_block(block)

    def stack_block(self, block, t_block=None, snap=False):
        follwing = self.get_following(block)
        self.remove_list(follwing)
        if t_block is None:
            self.join_list(0, follwing, snap)
        else:
            li, place = self.find_block(t_block)
            self.join_list(li, follwing, snap)
        self.clean_up()
        self.print_cmds()

    def find_block(self, block):
        for li in self.cmds:
            for blo in li:
                if blo is block:
                    return (li,blo)
        return None

    def join_list(self, li, following, snap):
        if snap:
            li += following
        else:
            self.cmds.append(following)

    def remove_list(self, following):
        li,place = self.find_block(following[0])
        if li[0] == following[0]:
            li[:] = []
            return
        li[:] = li[:li.index(place)]
        

    def get_following(self, block):
        li,place = self.find_block(block)
        following = li[li.index(place):]      
        return following
            
    def clean_up(self):
        for li in self.cmds:
            if len(li) == 0:
                self.cmds.remove(li)

    def add_block_to_cmds(self, block):
        self.cmds.append(block)
        #self.character.print_cmds()

    def active_logic(self):
        for li in self.cmds:
            for block in li:
                block.logic(self)


    def ret_len_list(self):
        list_len = [len(i) for i in self.cmds]
        return max(list_len)

    def handle_list(self,lis):
        for a in lis:
            a.logic(self)
            yield

    def start(self):
        self.list_of_gen = [self.handle_list(i) for i in self.cmds]
        self.x = 100
        self.y = 100

    def handle_character(self):
        temp = []
        for g in self.list_of_gen:
            try:
                res = next(g)
                temp.append(g)
            except:
                pass
        self.list_of_gen = temp
        return len(self.list_of_gen)



    def update_following_offset(self, following,event):
            #li, place = self.find_block(following[0])
            for i,block in enumerate(following):
                mouse_x, mouse_y = event.pos
                block.offset_x = block.rect.x - mouse_x
                block.offset_y = block.rect.y - mouse_y# + i *50


    def update_following_pos(self, following, event):
        for i,block in enumerate(following):
            mouse_x, mouse_y = event.pos
            block.rect.x = mouse_x + block.offset_x
            block.rect.y = mouse_y + block.offset_y
