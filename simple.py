import pygame

pygame.init()

screen = pygame.display.set_mode((800, 480))

COLOR_BLUE = (0, 0, 255)

running = True
is_blue = True

x = 30
y = 30

clock = pygame.time.Clock()
FPS = 60

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: 
        y -= 3
    if pressed[pygame.K_DOWN]:
        y += 3
    if pressed[pygame.K_RIGHT]:
        x += 3
    if pressed[pygame.K_LEFT]:
        x -= 3


    screen.fill((0, 0, 0))
    if is_blue:
        pygame.draw.rect(screen, COLOR_BLUE, pygame.Rect(x, y, 60, 60))
    else:
        color = (255, 100, 0)
        pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))

    # pygame.draw.rect(screen, COLOR_BLUE, pygame.Rect(30, 30, 60, 60))

    
    pygame.display.flip()
    clock.tick(FPS)