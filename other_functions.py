import pygame
import defines
import new_block_class as block_classes






def add_blocks(blocks, current_character):
    for i in range(len(defines.BLOCKS_TEXT)):
        x = defines.SAFE_BLOCKS_LOC 
        y = 20 + (i * 60)  
        if defines.BLOCKS_TEXT[i] == "Move 10 Steps":
            blocks.append(block_classes.move_character(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Go to Mouse":
            blocks.append(block_classes.go_to_mouse(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Go to Random Position":
            blocks.append(block_classes.go_to_random(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Go to X: 0 Y: 0":
            blocks.append(block_classes.set_x_y_character(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Set X to 0":
            blocks.append(block_classes.set_x_character(x, y, (150, 50)))
        elif defines.BLOCKS_TEXT[i] == "Set Y to 0":
            blocks.append(block_classes.set_y_character(x, y, (150, 50)))
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

def transparentSurface(size):
    surface = pygame.Surface(size).convert_alpha()
    surface.fill((0, 0, 0, 0))
    return surface


def check_param(param, x=True):
    if isinstance(param, str):
        if param.isdigit() and int(param) > 0:
            if int(param) < defines.FULL_SCREEN_WIDTH and x:
                return True
            elif int(param) < defines.FULL_SCREEN_HEIGHT:
                return True
        return False


def pop_up(screen,parm, clock):
    for t in parm:
        alpha_surface =  transparentSurface(screen.get_size())
        pygame.draw.rect(alpha_surface, (100,100,100,100),pygame.Rect(0, 0, defines.FULL_SCREEN_WIDTH, defines.FULL_SCREEN_HEIGHT), border_radius=10)
        

        box = pygame.Rect(defines.HALF_SCREEN_WIDTH*0.75,defines.HALF_SCREEN_HEIGHT*0.75, defines.HALF_SCREEN_WIDTH//2, defines.HALF_SCREEN_HEIGHT//2)
        pygame.draw.rect(alpha_surface,defines.WHITE, box)
        #pygame.display.flip()
        font = pygame.font.Font(None, 32)

        input_box = pygame.Rect(defines.HALF_SCREEN_WIDTH*0.9, defines.HALF_SCREEN_HEIGHT*0.9+60, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        done = False
        text = ''
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
                            #print(text)
                            if check_param(text, t == "x"):
                                print(f"Parameter {t} set to {text}")
                                parm[t] = text
                            else:
                                print(f"Invalid input for {t}: {text}")
                            done = True
                            
                            
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            #alpha_surface.fill(defines.WHITE)
            #t = f"enter a value for {param1}"

            # Render and blit the label so it's visible
            label = defines.FONT.render(f"Enter a value for {t}:", True, defines.BLACK)
            alpha_surface.blit(label, (defines.HALF_SCREEN_WIDTH*0.9, defines.HALF_SCREEN_HEIGHT*0.9))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            alpha_surface.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(alpha_surface, color, input_box, 2)
            screen.blit(alpha_surface, (0,0))

            pygame.display.flip()
            clock.tick(30)
    return parm

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