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
import threading
import time

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
screen = pygame.display.set_mode((defines.FULL_SCREEN_WIDTH,  defines.FULL_SCREEN_HEIGHT-50), pygame.RESIZABLE)
pygame.display.set_caption("Snapping Blocks")
clock = pygame.time.Clock()
#FONT = pygame.font.SysFont("Arial", 24)

# Define the action variable before use
action = False

#screen_2 = pygame.display.set_mode((defines.FULL_SCREEN_WIDTH,  defines.FULL_SCREEN_HEIGHT-50), pygame.RESIZABLE)



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

def draw_blocks(blocks, screen):
    for block in blocks:
        block.draw(screen)

def main():
    list_of_characters = []
    list_of_characters.append(Character("C:\\Data\\roy\\my_projects\\game_enj_sc_like\\scracth_like_enj\\defult_character_2.png", 100, 100))
    character = list_of_characters[0]
    running = True
    side_blocks = []
    global action
    l_t = []
    l_b = None
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
                    res = block.handle_event(event, add_block)
                    if res == 1:  #up
                        character.snap_to_blocks(block)
                    elif res == 2: #move
                        character.update_following_pos(character.get_following(block),event)
                    elif res == 3: #down
                        character.update_following_offset(character.get_following(block), event)
                        if len(l_t) < 2:
                            l_t.append(time.time())
                            print(l_t[-1])
                        if len(l_t) == 2:
                            print(l_t[1] - l_t[0], "--------")
                            if l_t[1] - l_t[0] < 0.4 and l_b == block:
                                #block.start()
                                dic = block.get_par()
                                dic = other_functions.pop_up(screen,dic,clock)
                                block.start(dic)
                                print("d - clip - active")
                            l_t[:] = []


                        l_b = block

            action_button(event)

        screen.fill(defines.WHITE)
        draw_blocks(side_blocks, screen)
        draw_blocks(list_of_characters, screen)
        for li in character.cmds:
            for block in li:
                block.draw(screen)

        # Draw the vertical line
        #pygame.draw.rect(screen, defines.BLACK, line)
        other_functions.draw_other_blocks(line, screen, green_button, red_button)
        
        #play logic for each block


        if action:

            lis_ch=[]
            for c in list_of_characters:
                c.start()
                lis_ch.append(c)
            screen.fill(defines.WHITE)
            draw_blocks(list_of_characters, screen)
            pygame.display.flip()

            #character.active_logic(screen)
            
            time.sleep(1)
            while len(lis_ch) > 0 and action:
                lis_ch_temp = []
                for c in lis_ch:
                    try:
                        if c.handle_character() > 0:
                            lis_ch_temp.append(c)
                    except:
                        pass
                lis_ch = lis_ch_temp
                screen.fill(defines.WHITE)
                draw_blocks(list_of_characters, screen)
                pygame.display.flip()
                action_button(event)

            """for li in character.cmds:
                for block in li:
                    block.logic(character)
                    screen.fill(defines.WHITE)
                    draw_blocks(list_of_characters, screen)
                    draw_blocks(side_blocks, screen)
                    pygame.display.flip()"""

            action = False
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