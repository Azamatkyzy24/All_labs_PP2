import pygame 

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 480))

COLOR_WHITE = (255, 255, 255)


_songs = ['I_wanna_be_yours.mp3', 'Out_of_my_league.mp3', 'Who_says.mp3', 'Lover.mp3']


def next_song(): # function for next_song
    global _songs
    _songs = _songs[1:] + [_songs[0]] # putting current song to the back of the list
    pygame.mixer.music.load(_songs[0]) # loading the next song 
    pygame.mixer.music.play() # playing the loaded song

def previous_song():
    global _songs
    _songs = [_songs[-1]] + _songs[:-1] # putting the last-played song to the front of the list
    pygame.mixer.music.load(_songs[0]) # loading the last-played song
    pygame.mixer.music.play() # playing the loaded song

paused = False

def stopping(): # function for stopping the song
    global paused
    paused = not paused
    if paused:
        pygame.mixer.music.pause() # if the paused it True, call the pause() function 
    else:
        pygame.mixer.music.unpause() # if the paused is False, call unpause() function 

clock = pygame.time.Clock()
FPS = 60


# pygame has only 24([0-23]) events and to add a custom event we add 1(and more to have more) to USEREVENT
# USEREVENT has the value of 23
# so, our new event would have an index of 24, and if we wanted to add more custom events, we would do it 
# like this: NEW_EVENT = pygame.USEREVENT + 2
# whenever the song ends 'set_endevent' pushes new event 'SONG_END' to the event queue
# our game loop would detect the 'SONG_END' event and starts the 'next_song' function 
SONG_END = pygame.USEREVENT + 1 
pygame.mixer.music.set_endevent(SONG_END)

pygame.mixer.music.load(_songs[0]) # loading the current song 
pygame.mixer.music.play() # playing the loaded 'current' song right after the window opens

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: # next song
                next_song() # calling next_song function
            if event.key == pygame.K_LEFT: # previous song
                previous_song() # calling the previous_song function 
            if event.key == pygame.K_SPACE:
                stopping() # calling the stopping() function 
        if event.type == SONG_END:
            next_song()

    screen.fill(COLOR_WHITE) # filling the screen with white color

    pygame.display.flip()
    clock.tick(FPS)