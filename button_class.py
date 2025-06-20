import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.hovered = False
        self.on = False

    def draw(self, surface):
        color = (0, 128, 255) if self.hovered else (0, 100, 200)
        pygame.draw.rect(surface, color, self.rect)
        label = self.font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            print(f"Button '{self.text}' clicked!")

    def turn_on(self):
        self.on = True
        print(f"Button '{self.text}' turned on.")
        
    def turn_off(self):
        self.on = False
        print(f"Button '{self.text}' turned off.")