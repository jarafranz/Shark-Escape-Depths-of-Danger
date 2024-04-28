import pygame
from game_states import main_menu

pygame.init()

FPS = 120

def main():
    pygame.init()
    win = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Shark Escape: Depths of Danger")
    pygame_icon = pygame.image.load("assets/logo (1).png")
    pygame.display.set_icon(pygame_icon)
    main_menu(win)

if __name__ == "__main__":
    main()

