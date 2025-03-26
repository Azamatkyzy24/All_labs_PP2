import pygame, math

pygame.init()

WIDTH = 800
HEIGHT = 480

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHTBLUE = (173, 216, 255)
COLOR_GRAY = (128, 128, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font('game_bubble.ttf', 15)
e_key_message = font.render("Press 'E' to erase", True, COLOR_BLACK)
d_key_message = font.render("Press D to draw", True, COLOR_BLACK)

base_layer = pygame.Surface((WIDTH, HEIGHT))

LMB_pressed = False
THICKNESS = 5
eraser_thickness = 10

curr_x = 0
curr_y = 0
prev_x = 0
prev_y = 0

center = (0, 0)
radius = 0

clock = pygame.time.Clock()
FPS = 60

def radius(x1, y1, x2, y2):
    return int(math.sqrt((x1 - x2)**2 + (y1 - y2)**2)) // 2 # getting the radius 

def center(x1, y1, x2, y2):
    return ((x1 + x2) // 2, (y1 + y2) // 2) # getting the center of the circle

eraser = False

base_layer.fill(COLOR_WHITE)
screen.blit(base_layer, (0, 0))

def draw_menu():
    pygame.draw.rect(base_layer, COLOR_GRAY, (0, 0, WIDTH, 70))
    pygame.draw.line(base_layer, COLOR_BLACK, (0, 70), (WIDTH, 70))
    base_layer.blit(e_key_message, (10, 14))
    base_layer.blit(d_key_message, (10, 42))

running = True
while running:

    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMB_pressed = True
            prev_x = event.pos[0]
            prev_y = event.pos[1]
        
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMB_pressed = False
            if not eraser:
                curr_x = event.pos[0]
                curr_y = event.pos[1]
                pygame.draw.circle(base_layer, COLOR_BLUE, center(curr_x, curr_y, prev_x, prev_y), radius(curr_x, curr_y, prev_x, prev_y), THICKNESS)
            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                eraser = True
            if event.key == pygame.K_d:
                eraser = False
            
        screen.blit(base_layer, (0, 0))

        if event.type == pygame.MOUSEMOTION:
            if LMB_pressed:
                if eraser:
                    curr_x = event.pos[0]
                    curr_y = event.pos[1]
                    pygame.draw.line(base_layer, COLOR_WHITE, (prev_x, prev_y), (curr_x, curr_y), eraser_thickness)
                elif not eraser:
                    curr_x = event.pos[0]
                    curr_y = event.pos[1]
                    pygame.draw.circle(screen, COLOR_BLUE, center(curr_x, curr_y, prev_x, prev_y), radius(curr_x, curr_y, prev_x, prev_y), THICKNESS)

    pygame.display.flip()
    clock.tick(FPS)