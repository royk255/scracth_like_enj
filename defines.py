BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
AQUA = (0, 255, 255)
FULL_SCREEN_WIDTH = 1920
FULL_SCREEN_HEIGHT = 1080
HALF_SCREEN_WIDTH =  FULL_SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = FULL_SCREEN_HEIGHT // 2
LINE_X = 1600
SAFE_BLOCKS_LOC = LINE_X + 50 

BLOCKS_TEXT = [
    "Move 10 Steps",
    "Jump",
    "Turn Left",
    "Turn Right",
    "Move Backward"
]


import pygame
import sys
import os
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)



types_colors = {
    "motion": BLUE,
    "look": PURPLE,
    "sound": PINK,
    "ebvent": YELLOW,
    "control": ORANGE,
    "sensing": AQUA,
    "operators": GREEN,
    "variables": RED
}