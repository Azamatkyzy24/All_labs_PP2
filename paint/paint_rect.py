import pygame

pygame.init()

COLOR_RED = (255, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_LIGHTBLUE = (173, 216, 255)

WIDTH = 800
HEIGHT = 480

screen = pygame.display.set_mode((WIDTH, HEIGHT))

base_layer = pygame.Surface((WIDTH, HEIGHT)) # giving the size for the surface that would track and store 
                                             # everything being drawn on the screen

LMB_pressed = False
THICKNESS = 5

curr_x = 0
curr_y = 0

prev_x = 0
prev_y = 0

clock = pygame.time.Clock()
FPS = 60

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)) # this enables us to draw a rectangle
    # dragging from right to left and left to right

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMB_pressed = True
            prev_x = event.pos[0] # the x coord of the pressed point
            prev_y = event.pos[1] # the y coord of the pressed point

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMB_pressed = False
            curr_x = event.pos[0] # the x coord of the released point
            curr_y = event.pos[1] # the y coord of the released point
            pygame.draw.rect(screen, COLOR_LIGHTBLUE, calculate_rect(curr_x, curr_y, prev_x, prev_y), THICKNESS)
            base_layer.blit(screen, (0, 0)) # pasting base_layer into screen

        screen.blit(base_layer, (0, 0)) # saving every rect that's being calculated before actually drawing it
        # why in MOUSEBUTTONUP I have 'base_layer.blit(screen, (0, 0))' and screen.blit(base_layer, (0, 0)) outside of it, in the game loop?
        # Because, while holding the LMB and moving my mouse, my current x, y coords change always and I draw a rectangle for every curr_x and curr_y
        # when I release the LMB, I draw the 'last' rectangle of this particular mouse movement on the screen, and save it in the base_layer
        # I have this 'screen.blit(base_layer, (0, 0))', to draw every 'done'✅ rectangle on the screen from the base_layer
        # It's outside of the 'event if statements', because, the rectangles of the 'MOUSEMOTION' event, are drawn on top of the base_layer. This is helpful, because the rectangle drawn on the last coord of the MOUSEMOTION will not be on the next coord of the MOUSEMOTION
        
        if event.type == pygame.MOUSEMOTION:
            if LMB_pressed:
                curr_x = event.pos[0]
                curr_y = event.pos[1]
                pygame.draw.rect(screen, COLOR_LIGHTBLUE, calculate_rect(curr_x, curr_y, prev_x, prev_y), THICKNESS)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]: # if the SHIFT + '=' is pressed 
            if pressed_keys[pygame.K_EQUALS]:                              # add thickness, otherwise decrease
                THICKNESS = min(25, THICKNESS + 1) # we get the min() to limit the upper bound of thickness to be 25
        if pressed_keys[pygame.K_MINUS]:
            THICKNESS = max(1, THICKNESS - 1) # we get the max() to limit the lower bound of thickness to be 1

    pygame.display.flip()
    clock.tick(FPS)