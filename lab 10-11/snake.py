import pygame, random, time
from color_palette import *
import db_handler

pygame.init()

HEIGHT = 720
WIDTH = 720

clock = pygame.time.Clock()
FPS = 5

count_food = 0
count_level = 1

color_index = 1
color_random = COLOR_BLUE

username_entered = False
username = ''

paused = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))

font = pygame.font.Font('game_bubble.ttf', 30)
font_endgame = pygame.font.Font('game_bubble.ttf', 80)
font_enter_username = pygame.font.Font('game_bubble.ttf', 35)
sound_food = pygame.mixer.Sound('food_eating.wav')

CELL = 30

# Функция для ввода имени пользователя
def enter_username():
    global username_entered, username
    screen.fill(COLOR_LIGHTBLUE)
    image_enter_username = font_enter_username.render('Enter your username:', True, COLOR_GREEN)
    image_enter_username_rect = image_enter_username.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(image_enter_username, image_enter_username_rect)

    input_box_rect = pygame.Rect(WIDTH // 4 - 20, HEIGHT // 2 + 50, 400, 50)
    pygame.draw.rect(screen, COLOR_WHITE, input_box_rect, 4)

    user_input = ''
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(user_input) > 0:
                        username = user_input
                        username_entered = True
                        active = False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                    screen.fill(COLOR_LIGHTBLUE)
                    image_enter_username = font_enter_username.render('Enter your username:', True, COLOR_GREEN)
                    image_enter_username_rect = image_enter_username.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(image_enter_username, image_enter_username_rect)
                    input_box_rect = pygame.Rect(WIDTH // 4 - 20, HEIGHT // 2 + 50, 400, 50)
                    pygame.draw.rect(screen, COLOR_WHITE, input_box_rect, 4)
                    txt_surface = font_enter_username.render(user_input, True, COLOR_GREEN)
                    screen.blit(txt_surface, (input_box_rect.x + 5, input_box_rect.y + 5))
                else:
                    user_input += event.unicode

        txt_surface = font_enter_username.render(user_input, True, COLOR_GREEN)
        screen.blit(txt_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

        db_handler.input_user(username)

        pygame.display.flip()
        clock.tick(FPS)

# Оставшиеся функции для рисования, движения змеи и проверки столкновений:

def draw_chess_board():
    colors = [COLOR_GRAY, COLOR_WHITE]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(3, 10), Point(4, 10), Point(5, 10)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw_snake(self):
        head = self.body[0]
        pygame.draw.rect(screen, COLOR_RED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, COLOR_GREEN, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global FPS, count_food, count_level
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos()
            if color_index == 0:
                count_food += 3
            elif color_index == 1:
                count_food += 2
            elif color_index == 2:
                count_food += 1
            sound_food.play()
            if count_food % 5 == 0:
                count_level += 1
                FPS += 2

    def check_collision_wall(self):
        head = self.body[0]
        if head.x > WIDTH // CELL - 1 or head.x < 0:
            return True
        if head.y < 0 or head.y > HEIGHT // CELL - 1:
            return True
        return False

class Food:
    def __init__(self):
        self.pos = Point(10, 10)
        self.food_colors = [COLOR_PURPLE, COLOR_BLUE, COLOR_LIGHTBLUE]
        self.creation_time = time.time()
        self.food_lifetime = 5

    def generate_random_pos(self):
        temp_x = random.randint(0, WIDTH // CELL - 1)
        temp_y = random.randint(0, HEIGHT // CELL - 1)

        if all((segment.x != temp_x or segment.y != temp_y) for segment in snake.body):
            self.pos.x = temp_x
            self.pos.y = temp_y
            self.creation_time = time.time()
        else:
            self.generate_random_pos()

    def draw_food(self):
        pygame.draw.rect(screen, color_random, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_color(self):
        global color_index, color_random
        color_index = random.randint(0, 2)
        color_random = food.food_colors[color_index]

    def check_food_lifetime(self):
        if time.time() - self.creation_time > self.food_lifetime:
            return True
        return False

food = Food()
snake = Snake()

running = True
while running:
    if not username_entered:
        enter_username()

        if db_handler.check_user_exists(username):
            print(username + ', Your highest level is', db_handler.show_highest_level()[0][0])
        else:
            print(username + ', You have not played yet')
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and snake.dx != -1:
                    snake.dx = 1
                    snake.dy = 0
                if event.key == pygame.K_LEFT and snake.dx != 1:
                    snake.dx = -1
                    snake.dy = 0
                if event.key == pygame.K_DOWN and snake.dy != -1:
                    snake.dx = 0
                    snake.dy = 1
                if event.key == pygame.K_UP and snake.dy != 1:
                    snake.dx = 0
                    snake.dy = -1
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_s and paused:
                    db_handler.process_score(count_food, count_level)
                    print(username + ', Your highest level is', db_handler.show_highest_level()[0][0])

        if not paused:
            if snake.check_collision_wall():
                running = False
                screen.fill(COLOR_GREEN)

                image_endgame_score = font_endgame.render("Total Score: " + str(count_food), True, COLOR_BLACK)
                image_endgame_score_rect = image_endgame_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                image_endgame_level = font_endgame.render("Level: " + str(count_level), True, COLOR_BLACK)
                image_endgame_level_rect = image_endgame_level.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

                screen.blit(image_endgame_score, image_endgame_score_rect)
                screen.blit(image_endgame_level, image_endgame_level_rect)

                db_handler.process_score(count_food, count_level)
                print(username + ", Your highest level is", db_handler.show_highest_level()[0][0])

                pygame.display.flip()

                time.sleep(5)

            screen.fill(COLOR_BLACK)

            draw_chess_board()

            snake.move()
            snake.check_collision(food)

            if food.check_food_lifetime():
                food.generate_random_color()
                food.generate_random_pos()

            food.draw_food()
            snake.draw_snake()

            score_text = font.render(f"Score: {count_food}", True, COLOR_BLUE)
            level_text = font.render(f'Level: {count_level}', True, COLOR_RED)
            screen.blit(score_text, (10, 10))
            screen.blit(level_text, (600, 10))
        else:
            pass

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()