import pygame
import random
import math
from collections import deque

class enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, end):
            super().__init__()
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 1  # Initial velocity
            self.direction = random.choice(['up', 'down', 'left', 'right'])  # Initial direction
            self.image = pygame.image.load("assets/sharkIdle (1).png")
            self.rect = self.image.get_rect()
            self.chase_distance = 200  # Distance threshold for chasing the player
            self.hitbox = pygame.Rect(self.x, self.y, 64, 64)
            self.prev_x = x
            self.prev_y = y
            self.load_images()

    def load_images(self):
        # Load different images for shark movement directions
        self.sharkLeft = pygame.image.load('assets/sharkLeft (1).png')
        self.sharkRight = pygame.image.load('assets/sharkRight (1).png')
        self.sharkUp = pygame.image.load('assets/sharkBack (1).png')
        self.sharkDown = pygame.image.load('assets/sharkFront (1).png')
        self.sharkIdle = pygame.image.load('assets/sharkIdle (1).png')

    def draw(self, win):
        # Draw the enemy's image
        if self.direction == 'right':
            win.blit(self.sharkRight, (self.x, self.y))
        elif self.direction == 'left':
            win.blit(self.sharkLeft, (self.x, self.y))
        elif self.direction == 'up':
            win.blit(self.sharkUp, (self.x, self.y))
        elif self.direction == 'down':
            win.blit(self.sharkDown, (self.x, self.y))
        else:
            win.blit(self.sharkIdle, (self.x, self.y))

        self.hitbox = pygame.Rect(self.x, self.y, 64, 64)

    def move(self, player, walls):
        # Calculate distance to the player
        dx = player.hitbox.centerx - self.hitbox.centerx
        dy = player.hitbox.centery - self.hitbox.centery
        distance_to_player = math.sqrt(dx ** 2 + dy ** 2)

        # Check if the player is within the chase distance
        if distance_to_player < self.chase_distance:
            # Calculate angle to the player
            angle = math.atan2(dy, dx)

            # Attempt to move towards the player along the x-axis
            dx_movement = self.vel * math.cos(angle)
            new_x = self.x + dx_movement
            new_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            if not any(new_rect_x.colliderect(w.rect) for w in walls):
                self.x = new_x
                # Update direction based on successful movement along x-axis
                if dx_movement > 0:
                    self.direction = 'right'
                elif dx_movement < 0:
                    self.direction = 'left'

            # Attempt to move towards the player along the y-axis
            dy_movement = self.vel * math.sin(angle)
            new_y = self.y + dy_movement
            new_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            if not any(new_rect_y.colliderect(w.rect) for w in walls):
                self.y = new_y
                # Update direction based on successful movement along y-axis
                if dy_movement > 0:
                    self.direction = 'down'
                elif dy_movement < 0:
                    self.direction = 'up'

        else:
            # Move aimlessly along pathways
            self.move_aimlessly(walls)

        # Update the hitbox position
        self.hitbox.x = self.x
        self.hitbox.y = self.y


    def move_aimlessly(self, walls):
        # Store the old position
        old_x, old_y = self.x, self.y

        # Move in the current direction
        if self.direction == 'right':
            self.x += self.vel
        elif self.direction == 'left':
            self.x -= self.vel
        elif self.direction == 'down':
            self.y += self.vel
        elif self.direction == 'up':
            self.y -= self.vel

        # Update the rect object for collision detection
        self.rect.x = self.x
        self.rect.y = self.y

        # Check for collisions with walls
        collided = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Revert to the old position
                self.x, self.y = old_x, old_y
                # Mark collision
                collided = True
                break

        # Change direction only if collided with a wall
        if collided:
            # Randomly choose a new direction (excluding opposite direction)
            new_directions = ['up', 'down', 'left', 'right']
            opposite_directions = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
            new_directions.remove(opposite_directions[self.direction])
            self.direction = random.choice(new_directions)