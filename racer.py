import pygame, random, time

pygame.init()

WIDTH = 400
HEIGHT = 600

COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
SCORE = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))

image_background = pygame.image.load('AnimatedStreet.png')
image_player = pygame.image.load('Player.png')
image_enemy = pygame.image.load('Enemy.png')
image_coin = pygame.image.load('coin.png')

scaled_image_coin = pygame.transform.scale(image_coin, (50, 50)) # scaling our coin

font = pygame.font.Font('game_bubble.ttf', 60) # getting the font
font_score = pygame.font.Font('game_bubble.ttf', 20)
font_small = pygame.font.Font('game_bubble.ttf', 20)
image_game_over = font.render('Game Over', True, COLOR_BLACK) # getting the text with our font
image_game_over_rect = image_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2)) # getting the rect object of our text

pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1) # -1 is for playing the music infinitely
sound_crash = pygame.mixer.Sound('crash.wav')

image_background_rect = image_background.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.centerx = WIDTH // 2
        self.rect.top = HEIGHT - self.rect.h

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10

    def generate_coord(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT: # if the top of the image is greater than the HEIGHT of the screen
            self.generate_coord()  # we generate the new random coord for our image to appear
                                   # at the top of the screen

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = scaled_image_coin
        self.rect = self.image.get_rect()
        self.positions = [70, 140, 210]
        self.rect.top = 10
        self.speed = 5
        self.random_pos() # setting the initial random position 

    def random_pos(self):
        self.rect.left = self.positions[random.randint(0, 2)]
        self.rect.top = 10

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.random_pos()

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group() # grouping all sprites in one place
all_sprites.add(player, enemy, coin)
enemy_sprites = pygame.sprite.Group()
enemy_sprites.add(enemy)
coin_sprites = pygame.sprite.Group()
coin_sprites.add(coin)

clock = pygame.time.Clock()
FPS = 60

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(image_background, image_background_rect)
    scores = font_small.render(str(SCORE), True, COLOR_BLUE)
    screen.blit(scores, (WIDTH - 40, 10))
    
    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemy_sprites): # first parameter is the sprite that will be
                                                              # checked if it's collided with the group of sprites
                                                              # in the second parameters
        sound_crash.play()
        screen.fill(COLOR_RED)
        screen.blit(image_game_over, image_game_over_rect)
        image_total_score = font_score.render('Your Score: ' + str(SCORE), True, COLOR_GREEN)
        image_total_score_rect = image_total_score.get_rect()
        image_total_score_rect.center = (WIDTH // 2, HEIGHT // 2 + 100)
        screen.blit(image_total_score, image_total_score_rect) # showing the total score

        for entity in all_sprites: # entity.kill() effectively makes the sprite no longer be drawn or updated 
            entity.kill() # by those groups
        pygame.display.flip()
        time.sleep(5)
        running = False
    
    if pygame.sprite.spritecollideany(player, coin_sprites):
        SCORE += 10
        coin.random_pos() # repositioning the coin


    pygame.display.flip()
    clock.tick(FPS)