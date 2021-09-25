import pygame
import time
import random

pygame.init()

pygame.mixer.music.load("sounds/bg.mp3")  # добавление музыки на фон
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.4)

food_sound = pygame.mixer.Sound("sounds/food.wav")  # добавление звуков при поедании еды и столкновении с краями экрана
kick_sound = pygame.mixer.Sound("sounds/kick.wav")
record_sound = pygame.mixer.Sound("sounds/record.wav")

width = 800
height = 600
dispaly = pygame.display.set_mode((width, height))
pygame.display.set_caption('змейка')  # установка названия для приложения
font = pygame.font.SysFont("None", 35)
icon = pygame.image.load('img/snake.png')  # установка иконки для приложения
pygame.display.set_icon(icon)

blue = (148, 237, 255)
black = (0, 0, 0)
red = (168, 0, 28)
orange = (255, 109, 51)
size = 20
snake_speed = 10

head_x = width // 2 // size * size
head_y = height // 2 // size * size

def get_random_point():
    x = random.randint(0, width - size) // size * size
    y = random.randint(0, height - size) // size * size
    return x, y

def show_snake(snake):
    for x in snake:
        pygame.draw.rect(dispaly, black, [x[0], x[1], size, size])

def show_score(score):
    value = font.render("очки: " + str(score), True, black)
    dispaly.blit(value, [10, 0])


f = open("record.txt", "r+")
first_record = f.read()
f2 = open("record.txt", "w")
i = 0

food_x, food_y = get_random_point()  # определение координат еды

snake = []  # список для длины змейки
snake_length = 1

vx = 0
vy = 0

clock = pygame.time.Clock()

while True:
    if head_x < 0 or head_x > width - size or head_y < 0 or head_y > height - size: # случай пройгрыша
        if snake_length - 1 > int(first_record):  # записб рекорда в файл, если он больше счета в данной игре
            f2.write(str(snake_length - 1))
        else:
            f2.write(first_record)

        message = font.render("вы проиграли!", True, black)
        dispaly.blit(message, [width / 2, height / 2])
        pygame.display.flip()
        kick_sound.play()

        time.sleep(2) # задержка перед выходом в случае пройгрыша

        pygame.quit()
        quit()


    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: # закрытие окна после нажатия на крестик
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN: # обработка событий(нажатий клавиш)
            if event.key == pygame.K_DOWN:
                vy = size
                vx = 0
            elif event.key == pygame.K_UP:
                vy = -size
                vx = 0
            elif event.key == pygame.K_RIGHT:
                vx = size
                vy = 0
            elif event.key == pygame.K_LEFT:
                vx = -size
                vy = 0

    head_x += vx
    head_y += vy

    dispaly.fill(blue) # отрисовка фона
    pygame.draw.rect(dispaly, red, [food_x, food_y, size, size])  # отрисовка еды
    snake.append((head_x, head_y))
    if len(snake) > snake_length:
        del snake[0]
    
    record0 = font.render("рекорд: " + first_record, True, black)
    dispaly.blit(record0, [10, 22])

    if snake_length - 1 > int(first_record) and int(first_record) != 0 and i < 1:  # звук при новом рекорде
        record_sound.play()
        i += 1

    show_snake(snake)
    show_score(snake_length - 1)

    if head_x == food_x and head_y == food_y:
        food_x, food_y = get_random_point()  # определение координат еды
        snake_length += 1 # увеличение длины змейки при съедании еды
        food_sound.play()
        

    pygame.display.flip() # обновление содержимого
    clock.tick(snake_speed) # установление времени обновдения экрана
