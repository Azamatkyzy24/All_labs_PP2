import pygame, datetime

pygame.init()

WIDTH = 800
HEIGHT = 600

COLOR_WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

running = True

image = pygame.image.load('clock.png').convert_alpha() # loading the image of the mickey
                                                       # is crucial for correctly and efficiently displaying
                                                       # images with varying levels of transparency
image_min = pygame.image.load('min_hand.png').convert_alpha() # loading the image of a 'minute' hand
image_sec = pygame.image.load('sec_hand.png').convert_alpha() # loading the image of a 'second' hand

image_rect = image.get_rect(center = (WIDTH // 2, HEIGHT // 2)) # getting the size and shape of the image
                                                                # the get_rect() function helps to get the size 
                                                                # and shape of an image to blit() after 
                                                                # 'center' attribute is for positioning the 
                                                                # 'rect' object in the center of the screen

clock = pygame.time.Clock()

angle_sec = 0 # the angle of seconds
angle_min = 0 # the angle of minutes

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR_WHITE) # setting white background

    current = datetime.datetime.now() 
    angle_sec = current.second * 6  # 6 degrees per second for 'second hand' (I add 0.5 to 6 so that it would perfectly meet image's "second" positions, 
                     # but it is actually 6 degrees per second
    angle_min = current.minute * 6 + current.second * 0.1 # 0.1 degrees per second for 'second hand'

    # Minute hand 
    rotated_min = pygame.transform.rotate(image_min, -angle_min - 51.5) # rotating the 'minute hand' image clockwise by 'angle_min'
                                                                      # we subtract 51.5, because the original image
                                                                      # is rotated left to the 51.5 degrees initially
    rotated_min_rect = rotated_min.get_rect(center = (WIDTH // 2, HEIGHT // 2)) # getting the 'rect' of the 
                                                                                # rotated 'minute hand' image

    # Second hand 
    rotated_sec = pygame.transform.rotate(image_sec, -angle_sec + 51.5) # rotating the 'second' image clockwise by 'angle_sec'
                                                                      # we subtract 51.5, because the original image
                                                                      # is rotated left to the 51.5 degrees initially
    rotated_sec_rect = rotated_sec.get_rect(center = (WIDTH // 2, HEIGHT // 2)) # getting the 'rect' of the 
                                                                                # rotated 'second hand' image

    screen.blit(image, image_rect) # showing the 'mickey' image
    screen.blit(rotated_min, rotated_min_rect) # showing the rotated 'minute hand' image
    screen.blit(rotated_sec, rotated_sec_rect) # showing the rotated 'second hand' image

    # if angle_sec >= 360: # if the degrees of 'second hand' are above 360, reset it to 0
    #     angle_sec = 0
    # if angle_min >= 360: # if the degrees of 'minute hand' are above 360, reset it to 0
    #     angle_min = 0
    # we don't these 'if' statements, because we are not incrementing anything, but assigning values of the 
    # current time to variables of 'minute' and 'second'
        
    pygame.display.flip()
    clock.tick(60) # we set the FPS to 1, because, if we set it to 60, all the events would have been happening
                  # 60 times faster, meaning that our 1 hour would be 60 seconds, and 1 minute would be 1 second
