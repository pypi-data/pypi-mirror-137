from cProfile import run
from dis import dis
from webbrowser import get
import pygame

pygame.init()

display = None
running = False

def make_window(width, height):
    global display
    display = pygame.display.set_mode((width, height))
    return display

def fill_window(red, green, blue):
    global display
    pygame.Surface.fill((red, green, blue))

def start_game_loop():
    global running
    running = True

def end_game_loop():
    global running
    running = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False