import pygame
import sys
import os
import defines
#from button_class import Button
import button_class
#import character_class
from character_class import Character
from button_class import Button
import new_block_class
from new_block_class import BlockType, move_character, turn_character
import other_functions


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((defines.FULL_SCREEN_WIDTH,  defines.FULL_SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Snapping Blocks")
clock = pygame.time.Clock()
#FONT = pygame.font.SysFont("Arial", 24)

# Define the action variable before use
action = False



green_button = button_class.Button(defines.HALF_SCREEN_WIDTH-300, 50, 50, 50, "Run")
red_button = button_class.Button(defines.HALF_SCREEN_WIDTH-225, 50, 50, 50, "Stop")
line = pygame.Rect(1600, 0, 20, 1080)

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
    list_of_characters = []
    list_of_characters.append(Character("C:\\Data\\roy\\my_projects\\game_enj_sc_like\\scracth_like_enj\\defult_character_2.png", 0, 0))
    character = list_of_characters[0]
    running = True
    side_blocks = []
    other_functions.add_blocks(side_blocks, character)
    while running:
        add_block = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for block in side_blocks:
                block.handle_event(event, add_block)
            if len(add_block) > 0:
                character.add_block_to_cmds(add_block)

            for li in character.cmds:
                for block in li:
                    if block.handle_event(event, add_block):
                        character.snap_to_blocks(block)
            

            action_button(event)

        screen.fill(defines.WHITE)
        for block in side_blocks:
            block.draw(screen)
        for character in list_of_characters:
            character.draw(screen)
        for li in character.cmds:
            for block in li:
                block.draw(screen)

        # Draw the vertical line
        #pygame.draw.rect(screen, defines.BLACK, line)
        other_functions.draw_other_blocks(line, screen, green_button, red_button)

        #play logic for each block

        if action:
            character.active_logic()
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