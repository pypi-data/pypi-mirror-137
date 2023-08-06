import pygame

pygame.init()

display = None

def make_window(width, height):
    global display
    display = pygame.display.set_mode((width, height))
    return display

def fill_window(red, green, blue):
    global display
    pygame.Surface.fill((red, green, blue))

def getevent():
    return pygame.event.get()

def typeofevent(event):
    if event.type == pygame.QUIT:
        return quit