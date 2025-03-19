import pygame

pygame.init()

WIDTH = 800
HEIGHT = 480

screen = pygame.display.set_mode((800, 480))

COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)

rect_x = (WIDTH - 50) // 2 # if we just used WIDTH // 2, the left edge of the circle would be at the center of the screen.
                           # otherwise, it would we would've centered top-left corner of the circle
rect_y = (HEIGHT - 50) // 2 # same with height


clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP] and rect_y > 0: # if the UP arrow key is pressed and the coords are greater than 0 
            rect_y -= 20                         # move the rectangle by 20 pixels to the top
    if pressed_keys[pygame.K_DOWN] and rect_y < (HEIGHT - 50): # if the DOWN arrow key is pressed and coords are less than (HEIGHT - 50)
            rect_y += 20                                       # move the rectangle by 20 px to the bottom(HEIGHT - 50, because, otherwise, we would go out of boundaries)
    if pressed_keys[pygame.K_RIGHT] and rect_x < (WIDTH - 50): # if the RIGHT arrow key is pressed and coords are less than (WIDTH - 50)
            rect_x += 20                                       # move the rectangle by 20 px to the right
    if pressed_keys[pygame.K_LEFT] and rect_x > 0: # if the LEFT arrow key is pressed and coords are less than (WIDTH - 50)
            rect_x -= 20                           # move the rectangle by 20 px to the right   


    screen.fill(COLOR_WHITE)

    pygame.draw.circle(screen, COLOR_RED, (rect_x + 25, rect_y + 25), 25) # drawing the moved circle on the screen at the given positions
                                                                          # we write +25 because, we have to show
                                                                          # the x, y coordinates of the center of the ball
                                                                          # otherwise, if we write (rect_x, rect_y), we would've 
                                                                          # shown the coordinates of top-left corner of the circle

    pygame.display.flip()
    clock.tick(60)