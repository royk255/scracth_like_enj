import pygame
import defines
import new_block_class as block_classes






def add_blocks(blocks, current_character):
    for i in range(len(defines.BLOCKS_TEXT)):
        x = defines.SAFE_BLOCKS_LOC 
        y = 20 + (i * 60)  
        if defines.BLOCKS_TEXT[i] == "Move 10 Steps":
            blocks.append(block_classes.move_character(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Turn Left":
            blocks.append(block_classes.turn_character(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Turn Right":
            blocks.append(block_classes.turn_character(x, y, (150, 50), "right"))
        elif defines.BLOCKS_TEXT[i] == "Wait 1 Second":
            blocks.append(block_classes.wait_character(x, y, (150, 50)))
        else:
            blocks.append(block_classes.BlockType(x, y, defines.BLOCKS_TEXT[i], "Motion", (150, 50), current_character))


def draw_other_blocks(line, screen, green_button, red_button):
    pygame.draw.rect(screen, defines.BLACK, line)
    #pygame.draw.rect(screen, defines.GREEN, green_button)  # Green button
    #pygame.draw.rect(screen, defines.RED, red_button)    # Red button
    green_button.draw(screen)
    red_button.draw(screen)

"""
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
"""