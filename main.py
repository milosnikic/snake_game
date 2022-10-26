import sys
from telnetlib import GA

import pygame

from models import CELL_NUMBER, CELL_SIZE, Fruit, Game, Snake

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((CELL_NUMBER * CELL_SIZE, CELL_NUMBER * CELL_SIZE))
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

game = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE and not game.game_over:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game.game_over:
                game.restart()
            if event.key == pygame.K_q and game.game_over:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                game.snake.change_direction(pygame.Vector2(0, -1))
            if event.key == pygame.K_DOWN:
                game.snake.change_direction(pygame.Vector2(0, 1))
            if event.key == pygame.K_LEFT:
                game.snake.change_direction(pygame.Vector2(-1, 0))
            if event.key == pygame.K_RIGHT:
                game.snake.change_direction(pygame.Vector2(1, 0))

    screen.fill((175, 215, 70))
    if not game.game_over:
        game.draw()
    else:
        game.draw_game_over()
    pygame.display.update()
    clock.tick(60)
