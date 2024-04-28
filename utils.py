import pygame

def get_font(size):
    return pygame.font.Font("Fonts/upheavtt.ttf", size)

def blur_surface(surface, factor):
    scaled = pygame.transform.smoothscale(surface, (int(surface.get_width() / factor), int(surface.get_height() / factor)))
    return pygame.transform.smoothscale(scaled, (surface.get_width(), surface.get_height()))