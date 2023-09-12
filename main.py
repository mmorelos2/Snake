import pygame
import random
import time
from collections import deque
import itertools
pygame.init()

WIDTH, HEIGHT = 601, 351
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
FONT = pygame.font.SysFont(None, 40)

FPS = 12

unused_var = 24


class Snake:
    def __init__(self, coords):
        self.body = deque([coords])
        self.dir = ""

    def update_coords(self, food):
        x = 0
        y = 0
        if self.dir == pygame.K_LEFT:
            x = -1
        elif self.dir == pygame.K_RIGHT:
            x = 1
        elif self.dir == pygame.K_UP:
            y = -1
        elif self.dir == pygame.K_DOWN:
            y = 1

        self.body.appendleft((self.body[0][0] + x, self.body[0][1] + y))
        if self.body[0] not in food:
            self.body.pop()
        else:
            food.remove(self.body[0])
        return

    def update_dir(self, key, prev_key):
        opposite = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT
        }
        if opposite[key] == self.dir or opposite[prev_key] == key:
            return
        # CHANGE ME
        self.dir = key
        return

    def check_loss(self):
        if (self.body[0] in list(itertools.islice(self.body, 1, len(self.body))) or
            self.body[0][0] == 0 or
            self.body[0][0] == WIDTH // 25 - 1 or
            self.body[0][1] == 0 or
            self.body[0][1] == HEIGHT // 25 - 1):
            return 1
        return 0


def draw_grid_border():
    pygame.draw.line(WIN, (0, 0, 0), [0, 0], [WIDTH, 0], 50)
    pygame.draw.line(WIN, (0, 0, 0), [0, HEIGHT], [WIDTH, HEIGHT], 51)
    pygame.draw.line(WIN, (0, 0, 0), [0, 0], [0, HEIGHT], 50)
    pygame.draw.line(WIN, (0, 0, 0), [WIDTH, 0], [WIDTH, HEIGHT], 51)

    for h in range(0, HEIGHT + 1, 25):
        pygame.draw.line(WIN, (0, 0, 0), [0, h], [WIDTH, h], 1)
    for r in range(0, WIDTH + 1, 25):
        pygame.draw.line(WIN, (0, 0, 0), [r, 0], [r, HEIGHT], 1)
    return


def draw_snake(snake):
    pygame.draw.rect(WIN, (0, 128, 0), pygame.Rect(snake.body[0][0] * 25, snake.body[0][1] * 25, 25, 25))
    for x, y in list(itertools.islice(snake.body, 1, len(snake.body))):
        pygame.draw.rect(WIN, (50, 205, 50), pygame.Rect(x * 25, y * 25, 25, 25))
    return


def draw_food(food):
    for x, y in food:
        pygame.draw.rect(WIN, (255, 100, 20), pygame.Rect(x * 25, y * 25, 25, 25))


def draw_window(snake, food):
    WIN.fill((255,255,224))
    draw_snake(snake)
    draw_food(food)
    draw_grid_border()
    textsurface = FONT.render('Score: ' + str(len(snake.body)), False, (0, 150, 200))
    WIN.blit(textsurface, (0, 0))
    pygame.display.update()
    return


def create_food(food, snake):
    x = random.randint(1, WIDTH//25 - 2)
    y = random.randint(1, HEIGHT//25 - 2)
    if (x, y) not in snake.body and (x, y) not in food:
        food.add((x, y))
    return


def main():
    clock = pygame.time.Clock()
    snake = Snake((WIDTH // 50, HEIGHT // 50))
    # Press key to start
    textsurface = FONT.render('Press any arrow key to start', False, (255, 255, 255))
    WIN.blit(textsurface, (0, 0))
    pygame.display.update()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or
                    event.key == pygame.K_RIGHT or
                    event.key == pygame.K_UP or
                    event.key == pygame.K_DOWN):
                    snake.dir = event.key
                    run = False
            if event.type == pygame.QUIT:
                pygame.quit()

    run = True
    food = set()
    while run:
        clock.tick(FPS)
        while len(food) < 5:
            create_food(food, snake)

        prev_key = snake.dir
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or
                        event.key == pygame.K_RIGHT or
                        event.key == pygame.K_UP or
                        event.key == pygame.K_DOWN):
                    snake.update_dir(event.key, prev_key)
            if event.type == pygame.QUIT:
                pygame.quit()

        snake.update_coords(food)
        if snake.check_loss():
            print("YOU LOST! SCORE:",len(snake.body))
            textsurface = FONT.render('YOU LOST! SCORE: ' + str(len(snake.body)), False, (255, 0, 0))
            WIN.blit(textsurface, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
            pygame.display.update()
            time.sleep(3)
            break
        draw_window(snake, food)
    pygame.quit()


if __name__ == "__main__":
    main()
