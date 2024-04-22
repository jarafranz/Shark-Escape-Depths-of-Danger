import pygame

NUM_BUBBLES = 10 

class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/bubble.png"), (32, 32))
        self.rect = self.image.get_rect(center=(x, y))
        self.value = 10  # Score value of the bubble
        self.original_position = (x, y)  # Store original position

    def reset_position(self):
        self.rect.center = self.original_position


level = [
            "####################",
            "#S     #           #",
            "# ### ### ######## #",
            "#   #       #   #  #",
            "### ####### # # # ##",
            "# # #       # # #  #",
            "# # # ### # # # ####",
            "# # #   # # # #    #",
            "# # ### # # # # #  #",
            "#     #   #   # #  E",
            "####################",

        ]


class Maze():
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Maze Game")
        self.clock = pygame.time.Clock()
        self.walls = []
        self.player_at_end = False
        self.end_rect = None
        self.bubbles = pygame.sprite.Group()
        self.original_bubble_positions = []
        
        x = y = 0
        end_rect = None
        for row in level:
            for col in row:
                if col == "#":
                    self.walls.append(Wall((x, y)))
                if col == "E":
                    end_rect = pygame.Rect(x, y, 64, 64)
                x += 64
            y += 64
            x = 0

        self.end_rect = end_rect

    def spawn_bubbles(self):
        for row_index, row in enumerate(level):
            for col_index, col in enumerate(row):
                if col != "#" and col != "E":
                    x = col_index * 64 + 32  # Adjust position to center within tile
                    y = row_index * 64 + 32  # Adjust position to center within tile
                    bubble = Bubble(x, y)
                    self.bubbles.add(bubble)
                    self.original_bubble_positions.append((x, y))

    def render(self, win):
        for wall in self.walls:
            wall.draw(self.screen)
        self.bubbles.draw(win)

    def check_end_collision(self, player_rect):
        if player_rect.colliderect(self.end_rect):
            self.player_at_end = True

    def is_player_at_end(self):
        return self.player_at_end
    
    def reset(self):
        self.player_at_end = False
        player.reset_pos((64, 64))

        for bubble in self.bubbles:
            bubble.reset_position()

    def check_bubble_collision(self, player_rect):
        # Check for collision between player and bubbles
        for bubble in self.bubbles:
            if player_rect.colliderect(bubble.rect):
                self.bubbles.remove(bubble)
                return bubble.value
        return 0

class Wall(object):
    def __init__(self, pos):
        self.image = pygame.image.load("assets/ph.png")
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


win = pygame.display.set_mode((1280, 720))

maze = Maze()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = None
        self.image = pygame.image.load('assets/idle (1).png')
        self.vel = 2
        self.score = 0
        self.hitbox = pygame.Rect(self.x, self.y, 54, 54)
        self.load_images()

    def reset_pos(self, initial_x, initial_y):
        self.x = initial_x
        self.y = initial_y

    def load_images(self):
        self.idle = pygame.image.load('assets/idle (1).png')
        self.walkRight = pygame.image.load('assets/right (1).png')
        self.walkLeft = pygame.image.load('assets/left (1).png')
        self.walkUp = pygame.image.load('assets/back (1).png')

        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    def draw(self, win, walls):
        if self.direction == "left":
            win.blit(self.walkLeft, (self.rect.x, self.rect.y))
        elif self.direction == "right":
            win.blit(self.walkRight, (self.rect.x, self.rect.y))
        elif self.direction == "up":
            win.blit(self.walkUp, (self.rect.x, self.rect.y))
        elif self.direction == "down":
            win.blit(self.idle, (self.rect.x, self.rect.y))
        else:
            win.blit(self.image, self.rect)

        # Update hitbox position
        self.hitbox.x = self.rect.x
        self.hitbox.y = self.rect.y

    def reset_pos(self, spawn_point):
        self.x, self.y = spawn_point

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        # Intelligent movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.vel
            self.direction = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.vel
            self.direction = "right"
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.vel
            self.direction = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.vel
            self.direction = "down"

        # Check for collisions in the direction of movement
        if dx != 0:
            self.move_intelligently(dx, 0, walls)
        elif dy != 0:
            self.move_intelligently(0, dy, walls)

    def move_intelligently(self, dx, dy, walls):
        # Check if the player is blocked in the direction of movement
        new_rect = self.rect.move(dx, dy)
        collides_with_walls = any(new_rect.colliderect(w.rect) for w in walls)

        if not collides_with_walls:
            # Update position if no collision occurs
            self.rect.x += dx
            self.rect.y += dy
        else:
            # Try orthogonal directions if blocked
            if dx != 0:
                self.move_intelligently(0, dy, walls)
            elif dy != 0:
                self.move_intelligently(dx, 0, walls)

    def score(self, value):
        self.score += value


# Initialize player
player = Player(64, 64, 54, 54)


pygame.display.flip()
