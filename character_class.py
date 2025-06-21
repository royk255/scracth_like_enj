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
            print("cmd length:", len(cmd))
        print("-----------------------")
        print(self.cmds)