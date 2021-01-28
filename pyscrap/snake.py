import pygame
import random
from _collections import deque

N = 20
D = 20


pygame.init()
screen = pygame.display.set_mode([N*D, N*D])

snake = deque([(0,0),(D,0)])
direction = 'right'
snake_alive = True

def new_food():
    return(random.randint(0,N-1)*D, random.randint(0,N-1)*D)
food = new_food()

running = True

def move_snake():
    global food
    head = head_x, head_y = snake[-1][0], snake[-1][1]


    if direction == 'down':

        if head_y == N*D-D:
            snake.append((head_x, 0))
        else:
            snake.append((head_x, head_y+D))

        
    if direction == 'up':

        if head_y == 0:
            snake.append((head_x, N*D-D))
        else:
            snake.append((head_x, head_y-D))

    if direction == 'left':

        if head_x == 0:
            snake.append((N*D-D, head_y))
        else:
            snake.append((head_x-D, head_y))

    if direction == 'right':

        if head_x == N*D-D:
            snake.append((0, head_y))
        else:
            snake.append((head_x+D, head_y))

    if head != food:
        snake.popleft()
    else:
        food = new_food()



while running:

    if len(snake) != len(set(snake)):
        snake_alive = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT or not snake_alive:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and snake[-1][1] == snake[-2][1]:
                direction = 'down'
            if event.key == pygame.K_w and snake[-1][1] == snake[-2][1]:
                direction = 'up'
            if event.key == pygame.K_a and snake[-1][0] == snake[-2][0]:
                direction = 'left'
            if event.key == pygame.K_d and snake[-1][0] == snake[-2][0]:
                direction = 'right'

    if snake_alive:
        move_snake()

    pygame.time.wait(50)


    screen.fill((0,0,0))
    for e in snake:
        pygame.draw.rect(screen, (255, 255, 255), (e[0],e[1], D, D))

    pygame.draw.rect(screen, (0, 255, 0), (food[0], food[1], D, D))

    pygame.display.flip()

if not snake_alive:
    print('snake ded')
pygame.quit()