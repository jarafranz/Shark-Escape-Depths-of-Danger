import pygame
import sys
import time
from button import Button 
from utils import get_font
from game_objects import enemy
from maze import Maze, Player

pygame.init()

pygame.mixer.music.load("music/main menu.mp3")
main_menu_music = "music/main menu.mp3"

pygame.mixer.music.load("music/game music.mp3")
game_music = "music/game music.mp3"

collect_sound = pygame.mixer.Sound("music/bubble.mp3")
collect_sound.set_volume(0.2)

game_over_sound = pygame.mixer.Sound("music/game over music.mp3")
game_win_sound = pygame.mixer.Sound("music/victory.mp3")

FPS = 120
bg_width = 1280
bg_height = 720

bg = pygame.transform.scale(pygame.image.load("assets/ocean map.png"), (bg_width, bg_height))
BG = pygame.transform.scale(pygame.image.load("assets/menu.png"), (bg_width, bg_height))
level_bg = pygame.transform.scale(pygame.image.load("assets/level.png"), (bg_width, bg_height))
title = pygame.transform.scale(pygame.image.load("assets/title.png"), (550, 300))
win_img = pygame.transform.scale(pygame.image.load("assets/win.png"), (bg_width, bg_height))
dead_img = pygame.transform.scale(pygame.image.load("assets/ded.jpg"), (bg_width, bg_height))

paused = False

def play_music(music):
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(-1)

def collect_bubble():
    collect_sound.play()

def game_over_music():
    game_over_sound.play()

def game_win_music():
    game_win_sound.play()

def redrawGameWindow(player, enemy, win, bg, maze):
    win.blit(bg, (0, 0))  # Draw background

    for wall in maze.walls:
        wall.draw(win)  # Draw maze walls

    maze.render(win)
    
    player.draw(win, maze.walls)  # Draw player
    enemy.draw(win)  # Draw enemy
    maze.bubbles.draw(win)

    font = get_font(30)  # Choose a font and size
    score_text_outline = font.render("Score: " + str(player.score), True, (0, 0, 0))  # Black color
    win.blit(score_text_outline, (20 + 1, 20 + 1))  # Slightly offset for the outline

    # Render the actual score text
    score_text = font.render("Score: " + str(player.score), True, (255, 255, 255))  # White color
    win.blit(score_text, (20, 20))  # Original position


    # Update display
    pygame.display.update()

# Function to handle game over
def game_over(win):

    while True:
        # Get mouse position
        GAMEOVER_MOUSE_POS = pygame.mouse.get_pos()

        # Render "GAME OVER" text
        GAMEOVER_TEXT = get_font(150).render("GAME OVER", True, "Black")
        GAMEOVER_OUTLINE = get_font(150).render("GAME OVER", True, "White")
        GAMEOVER_RECT = GAMEOVER_TEXT.get_rect(center=(640, 130))

        # Create buttons
        RESTART_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                                text_input="RESTART", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 450), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 600), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        win.blit(GAMEOVER_OUTLINE, (GAMEOVER_RECT.x - 2, GAMEOVER_RECT.y - 2))  # Draw outline first
        win.blit(GAMEOVER_OUTLINE, (GAMEOVER_RECT.x + 2, GAMEOVER_RECT.y - 2))
        win.blit(GAMEOVER_OUTLINE, (GAMEOVER_RECT.x - 2, GAMEOVER_RECT.y + 2))
        win.blit(GAMEOVER_OUTLINE, (GAMEOVER_RECT.x + 2, GAMEOVER_RECT.y + 2))
        win.blit(GAMEOVER_TEXT, GAMEOVER_RECT)

        for button in [RESTART_BUTTON, BACK_BUTTON, QUIT_BUTTON]:
            button.changeColor(GAMEOVER_MOUSE_POS)
            button.update(win)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if buttons are clicked
                if RESTART_BUTTON.checkForInput(GAMEOVER_MOUSE_POS):
                    game_over_sound.stop()
                    maze.reset()
                    maze.spawn_bubbles()
                    return easy(win, bg, maze)
                if BACK_BUTTON.checkForInput(GAMEOVER_MOUSE_POS):
                    game_over_sound.stop()
                    return play(win)
                if QUIT_BUTTON.checkForInput(GAMEOVER_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.update()

def game_win(win, player_score):
    while True:
        # Get mouse position
        WIN_MOUSE_POS = pygame.mouse.get_pos()

        # Render "YOU WIN" text
        WIN_TEXT = get_font(150).render("YOU ESCAPED!", True, "Black")
        WIN_OUTLINE = get_font(150).render("YOU ESCAPED!", True, "White")
        WIN_RECT = WIN_TEXT.get_rect(center=(640, 90))

        SCORE_TEXT = get_font(50).render("Your Score: " + str(player_score), True, "Black")
        SCORE_OUTLINE = get_font(50).render("Your Score: " + str(player_score), True, "White")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(640, 190))

        # Create buttons
        RESTART_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                                text_input="RESTART", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 450), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 600), 
                                text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        win.blit(WIN_OUTLINE, (WIN_RECT.x - 2, WIN_RECT.y - 2))  
        win.blit(WIN_OUTLINE, (WIN_RECT.x + 2, WIN_RECT.y - 2))
        win.blit(WIN_OUTLINE, (WIN_RECT.x - 2, WIN_RECT.y + 2))
        win.blit(WIN_OUTLINE, (WIN_RECT.x + 2, WIN_RECT.y + 2))
        win.blit(WIN_TEXT, WIN_RECT)

        win.blit(SCORE_OUTLINE, (SCORE_RECT.x - 2, SCORE_RECT.y - 2))
        win.blit(SCORE_OUTLINE, (SCORE_RECT.x + 2, SCORE_RECT.y - 2))
        win.blit(SCORE_OUTLINE, (SCORE_RECT.x - 2, SCORE_RECT.y + 2))
        win.blit(SCORE_OUTLINE, (SCORE_RECT.x + 2, SCORE_RECT.y + 2))
        win.blit(SCORE_TEXT, SCORE_RECT)

        for button in [RESTART_BUTTON, BACK_BUTTON, QUIT_BUTTON]:
            button.changeColor(WIN_MOUSE_POS)
            button.update(win)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if buttons are clicked
                if RESTART_BUTTON.checkForInput(WIN_MOUSE_POS):
                    game_win_sound.stop()
                    maze.spawn_bubbles()
                    maze.reset()
                    return easy(win, bg, maze)
                if BACK_BUTTON.checkForInput(WIN_MOUSE_POS):
                    game_win_sound.stop()
                    play_music(main_menu_music)
                    return play(win)
                if QUIT_BUTTON.checkForInput(WIN_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        # Update display
        pygame.display.update()


# Function to handle main menu
def main_menu(win):
    pygame.display.set_caption("Main Menu")

    play_music(main_menu_music)

    while True:
        win.blit(BG, (0, 0))
        win.blit(title, (400, 50))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(win) 
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play(win):
    pygame.display.set_caption("Levels")

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        win.blit(level_bg, (0, 0))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 150), 
                            text_input="EASY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                            text_input="MEDIUM", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 450), 
                            text_input="HARD", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        PLAY_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 600), 
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, PLAY_BACK]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu(win)
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    maze.spawn_bubbles()
                    maze.reset()
                    easy(win, bg, maze)
                if MEDIUM_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    medium(win)
                if HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    hard(win)

        pygame.display.update()

def easy(win, bg, maze):

    pygame.mixer.music.stop()  # Stop any playing music
    play_music(game_music)

    pygame.display.set_caption("Shark Escape: Depths of Danger") 

    while True:
        gameover = False  # Reset game over flag

        clock = pygame.time.Clock()

        # Redraw background image
        win.blit(bg, (0, 0))

        man = Player(70, 64, 54, 54)  # Create player object
        shark = enemy(500, 575, 12, 12, (800, 600))  # Create enemy object

        run = True
        # Inside the game loop
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            keys = pygame.key.get_pressed()
            
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and man.x > man.vel:
                man.x -= man.vel
                man.direction = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and man.x < 1280 - man.width - man.vel:
                man.x += man.vel
                man.direction = "right"
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and man.y > man.vel:
                man.y -= man.vel
                man.direction = "up"
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and man.y < 720 - man.height - man.vel:
                man.y += man.vel
                man.direction = "down"

            # Update player and check for collision with end
            man.update(maze.walls)
            shark.move(man, maze.walls)
            maze.check_end_collision(man.rect)


            if maze.is_player_at_end():
                pygame.mixer.music.stop()
                pygame.time.delay(1000)
                game_win_music()
                fade_in(win, win_img, 10)
                game_win(win, man.score)  # Call game win screen function
                break  # Exit from the game loop after game win screen
                
            bubble_score = maze.check_bubble_collision(man.rect)
            man.score += bubble_score

            if bubble_score > 0:
                collect_bubble()

            # Update player and enemy positions
            man.update(maze.walls)
            shark.move(man, maze.walls)
            redrawGameWindow(man, shark, win, bg, maze)  # Redraw game window

            # Inside the game loop after updating player and shark positions
            player_rect = pygame.Rect(man.x, man.y, man.width, man.height)
            shark_rect = pygame.Rect(shark.x, shark.y, shark.width, shark.height)

            if man.hitbox.colliderect(shark.hitbox):
                pygame.mixer.music.stop()
                print("Player collided with shark!")
                pygame.time.delay(1500)
                game_over_music()
                fade_in(win, dead_img, 21)
                gameover = True

            # Check game over condition
            if gameover:
                game_over(win)  # Call game over screen function
                break  # Exit from the game loop after game over screen

            # Update display
            pygame.display.update()


# Function for medium level
def medium(win):
    while True: 
        # Fill window with white background
        win.fill((255, 255, 255))

        MEDIUM_MOUSE_POS = pygame.mouse.get_pos()
        MEDIUM_TEXT = get_font(45).render("Coming Soon.", True, "Black")
        MEDIUM_RECT = MEDIUM_TEXT.get_rect(center=(640, 260))

        MEDIUM_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 600), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        MEDIUM_BACK.changeColor(MEDIUM_MOUSE_POS)
        MEDIUM_BACK.update(win)

        win.blit(MEDIUM_TEXT, MEDIUM_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MEDIUM_BACK.checkForInput(MEDIUM_MOUSE_POS):
                    play(win)

        pygame.display.update()

# Function for hard level
def hard(win):
    while True: 
        # Fill window with white background
        win.fill((255, 255, 255))

        HARD_MOUSE_POS = pygame.mouse.get_pos()
        HARD_TEXT = get_font(45).render("Coming Soon.", True, "Black")
        HARD_RECT = HARD_TEXT.get_rect(center=(640, 260))

        HARD_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 600), 
                                text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        
        HARD_BACK.changeColor(HARD_MOUSE_POS)
        HARD_BACK.update(win)

        win.blit(HARD_TEXT, HARD_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if HARD_BACK.checkForInput(HARD_MOUSE_POS):
                    play(win)

        pygame.display.update()

def fade_in(win, img, delay_time):
    alpha_surface = pygame.Surface((bg_width, bg_height))  # Create a surface for transparency
    alpha_surface.fill((0, 0, 0))  # Fill the surface with black
    alpha = 255  # Initial alpha value (fully opaque)

    # Fade in the image
    while alpha > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        win.blit(img, (0, 0))  # Draw image
        alpha_surface.set_alpha(alpha)  # Set alpha value for surface
        win.blit(alpha_surface, (0, 0))  # Draw black surface with transparency
        alpha -= 3  # Decrease alpha value

        if alpha < 0:
            alpha = 0

        pygame.display.update()  # Update display
        pygame.time.delay(delay_time)  # Delay for smooth animation

# Create maze object
maze = Maze()
maze.spawn_bubbles()

# Run main menu
main_menu(pygame.display.set_mode((bg_width, bg_height)))
