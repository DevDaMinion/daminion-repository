import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3-Level Platformer")
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)


PLAYER_WIDTH, PLAYER_HEIGHT = 50, 60
GRAVITY = 0.8
JUMP_SPEED = -15

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.vel_y = 0
        self.on_ground = False

    def reset_position(self):
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_HEIGHT - 100
        self.vel_y = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()

        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5

        self.vel_y += GRAVITY
        dy = self.vel_y

        self.rect.x += dx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if dx > 0:
                    self.rect.right = platform.rect.left
                elif dx < 0:
                    self.rect.left = platform.rect.right

        self.rect.y += dy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

level_data = [
    [
        (0, HEIGHT - 40, WIDTH, 40),
        (200, 450, 200, 20),
        (500, 350, 200, 20),
        (300, 250, 150, 20)
    ],
    [
        (0, HEIGHT - 40, WIDTH, 40),
        (100, 500, 150, 20),
        (300, 400, 150, 20),
        (550, 300, 200, 20),
        (700, 200, 80, 20)
    ],
    [
        (0, HEIGHT - 40, WIDTH, 40),
        (150, 500, 100, 20),
        (300, 450, 100, 20),
        (450, 400, 100, 20),
        (600, 350, 100, 20),
        (750, 300, 50, 20)
    ]
]

def create_platforms(level_index):
    platforms = pygame.sprite.Group()
    for plat_data in level_data[level_index]:
        platforms.add(Platform(*plat_data))
    return platforms

current_level = 0
platforms = create_platforms(current_level)
player = Player()

try:
    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(platforms)

        if player.rect.left > WIDTH:
            current_level += 1
            if current_level >= len(level_data):
                print("🎉 You completed all levels!")
                running = False
            else:
                platforms = create_platforms(current_level)
                player.reset_position()

        platforms.draw(screen)
        screen.blit(player.image, player.rect)
        pygame.display.flip()

except Exception as e:
    print("An error occurred:", e)
    pygame.quit()
    input("Press Enter to exit...")
    sys.exit()

pygame.quit()
sys.exit()
