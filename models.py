import random

import pygame
from pygame.math import Vector2

CELL_SIZE = 40
CELL_NUMBER = 20

DIRECTIONS = {
    "UP": Vector2(0, -1),
    "DOWN": Vector2(0, 1),
    "LEFT": Vector2(-1, 0),
    "RIGHT": Vector2(1, 0),
}


class Fruit:
    def __init__(self, surface, image_path) -> None:
        self.randomize()
        self.surface = surface
        self.image = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(), (40, 40)
        )

    def draw(self):
        rect = pygame.Rect(
            self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE, CELL_SIZE, CELL_SIZE
        )
        self.surface.blit(self.image, rect)

    def randomize(self):
        self.x = random.randint(0, CELL_NUMBER - 1)
        self.y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self, surface):
        self.start()
        self.surface = surface
        self.head_up = pygame.transform.scale(
            pygame.image.load("assets/head_up.png").convert_alpha(), (40, 40)
        )
        self.head_down = pygame.transform.scale(
            pygame.image.load("assets/head_down.png").convert_alpha(), (40, 40)
        )
        self.head_left = pygame.transform.scale(
            pygame.image.load("assets/head_left.png").convert_alpha(), (40, 40)
        )
        self.head_right = pygame.transform.scale(
            pygame.image.load("assets/head_right.png").convert_alpha(), (40, 40)
        )

        self.tail_up = pygame.transform.scale(
            pygame.image.load("assets/tail_up.png").convert_alpha(), (40, 40)
        )
        self.tail_down = pygame.transform.scale(
            pygame.image.load("assets/tail_down.png").convert_alpha(), (40, 40)
        )
        self.tail_left = pygame.transform.scale(
            pygame.image.load("assets/tail_left.png").convert_alpha(), (40, 40)
        )
        self.tail_right = pygame.transform.scale(
            pygame.image.load("assets/tail_right.png").convert_alpha(), (40, 40)
        )

        self.body_horizontal = pygame.transform.scale(
            pygame.image.load("assets/body_horizontal.png").convert_alpha(), (40, 40)
        )
        self.body_vertical = pygame.transform.scale(
            pygame.image.load("assets/body_vertical.png").convert_alpha(), (40, 40)
        )

        self.body_tl = pygame.transform.scale(
            pygame.image.load("assets/body_topleft.png").convert_alpha(), (40, 40)
        )
        self.body_tr = pygame.transform.scale(
            pygame.image.load("assets/body_topright.png").convert_alpha(), (40, 40)
        )
        self.body_bl = pygame.transform.scale(
            pygame.image.load("assets/body_bottomleft.png").convert_alpha(), (40, 40)
        )
        self.body_br = pygame.transform.scale(
            pygame.image.load("assets/body_bottomright.png").convert_alpha(), (40, 40)
        )

    def start(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]
        self.direction = DIRECTIONS["LEFT"]
        self.new_block = False

    def draw(self):
        for index, block in enumerate(self.body):
            if block.x > CELL_NUMBER:
                block.x = 0
            if block.x < 0:
                block.x = CELL_NUMBER
            if block.y > CELL_NUMBER:
                block.y = 0
            if block.y < 0:
                block.y = CELL_NUMBER
            x_pos = block.x * CELL_SIZE
            y_pos = block.y * CELL_SIZE

            rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
            if index == 0:
                # Head
                self._get_head_direction()
                self.surface.blit(self.head, rect)
            elif index == len(self.body) - 1:
                # Tail
                self._get_tail_direction()
                self.surface.blit(self.tail, rect)
            else:
                # Other blocks of snake's body
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    self.surface.blit(self.body_vertical, rect)
                elif previous_block.y == next_block.y:
                    self.surface.blit(self.body_horizontal, rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (
                        previous_block.y == -1 and next_block.x == -1
                    ):
                        self.surface.blit(self.body_tl, rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (
                        previous_block.y == 1 and next_block.x == -1
                    ):
                        self.surface.blit(self.body_bl, rect)
                    elif (previous_block.y == -1 and next_block.x == 1) or (
                        previous_block.x == 1 and next_block.y == -1
                    ):
                        self.surface.blit(self.body_tr, rect)
                    elif (previous_block.y == 1 and next_block.x == 1) or (
                        previous_block.x == 1 and next_block.y == 1
                    ):
                        self.surface.blit(self.body_br, rect)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

    def change_direction(self, direction):
        if self._can_change_direction(direction):
            self.direction = direction

    def _can_change_direction(self, direction):
        return (
            (self.direction == DIRECTIONS["UP"] or self.direction == DIRECTIONS["DOWN"])
            and (direction in [DIRECTIONS["LEFT"], DIRECTIONS["RIGHT"]])
            or (
                self.direction == DIRECTIONS["LEFT"]
                or self.direction == DIRECTIONS["RIGHT"]
            )
            and (direction in [DIRECTIONS["UP"], DIRECTIONS["DOWN"]])
        )

    def _get_head_direction(self):
        if self.body[0] - self.body[1] == DIRECTIONS["UP"]:
            self.head = self.head_up
        elif self.body[0] - self.body[1] == DIRECTIONS["DOWN"]:
            self.head = self.head_down
        elif self.body[0] - self.body[1] == DIRECTIONS["LEFT"]:
            self.head = self.head_left
        elif self.body[0] - self.body[1] == DIRECTIONS["RIGHT"]:
            self.head = self.head_right

    def _get_tail_direction(self):
        if self.body[-1] - self.body[-2] == DIRECTIONS["UP"]:
            self.tail = self.tail_up
        elif self.body[-1] - self.body[-2] == DIRECTIONS["DOWN"]:
            self.tail = self.tail_down
        elif self.body[-1] - self.body[-2] == DIRECTIONS["LEFT"]:
            self.tail = self.tail_left
        elif self.body[-1] - self.body[-2] == DIRECTIONS["RIGHT"]:
            self.tail = self.tail_right


class Game:
    def __init__(self, surface):
        pygame.display.set_caption("SnAkE gAmE")
        self.game_font = pygame.font.Font("fonts/PEOPLE BOOK.otf", 45)

        self.eat_sound = pygame.mixer.Sound("sound/eat.wav")
        self.game_over_sound = pygame.mixer.Sound("sound/game_over.wav")

        self.snake = Snake(surface)
        self.fruit = Fruit(surface, "assets/apple.png")

        self.game_over = False

        self.surface = surface

    def update(self):
        self.snake.move()
        self._check_collision()
        self._check_fail()

    def draw(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw()
        self.snake.draw()

    def restart(self):
        self.snake.start()
        self.fruit.randomize()
        self.game_over = False

    def _check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.eat_sound.play()
            self.snake.new_block = True

    def _check_fail(self):
        self.game_over = self.snake.body[0] in self.snake.body[1:]
        if self.game_over:
            self.game_over_sound.play()

    def draw_grass(self):
        for col in range(0, CELL_NUMBER):
            for row in range(0, CELL_NUMBER):
                if (col % 2 == 0 and row % 2 == 0) or (col % 2 == 1 and row % 2 == 1):
                    grass_rect = pygame.Rect(
                        col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE
                    )
                    pygame.draw.rect(self.surface, (167, 209, 61), grass_rect)

    def draw_score(self):
        score = str(len(self.snake.body) - 3)
        score_font = self.game_font.render(f"SCORE: {score}", True, (100, 100, 100))
        score_rect = score_font.get_rect(center=((CELL_SIZE * CELL_NUMBER) / 2, 30))

        apple = pygame.transform.scale(
            pygame.image.load("assets/apple.png").convert_alpha(), (40, 40)
        )
        apple.set_alpha(64)
        apple_rect = apple.get_rect(midleft=(score_rect.right + 10, score_rect.centery))

        bg_rect = pygame.Rect(
            score_rect.left - 5,
            score_rect.top,
            apple_rect.width + score_rect.width + 20,
            score_rect.height,
        )

        self.surface.blit(score_font, score_rect)
        self.surface.blit(apple, apple_rect)
        pygame.draw.rect(self.surface, (100, 100, 100), bg_rect, 1, 5)

    def draw_game_over(self):
        game_over_font = self.game_font.render("GAME OVER", True, (100, 100, 100))
        game_over_rect = game_over_font.get_rect(
            center=((CELL_SIZE * CELL_NUMBER) / 2, (CELL_SIZE * CELL_NUMBER) / 2 - 100)
        )

        new_game_font = self.game_font.render(
            "PRESS 'SPACE' FOR NEW GAME", True, (100, 100, 100)
        )
        new_game_rect = new_game_font.get_rect(
            center=((CELL_SIZE * CELL_NUMBER) / 2, game_over_rect.bottom + 50)
        )

        quit_game_font = self.game_font.render(
            "PRESS 'Q' FOR EXIT", True, (100, 100, 100)
        )
        quit_game_rect = quit_game_font.get_rect(
            center=((CELL_SIZE * CELL_NUMBER) / 2, new_game_rect.bottom + 50)
        )

        bg_rect = pygame.Rect(
            new_game_rect.left - 10,
            game_over_rect.top - 10,
            new_game_rect.width + 40,
            game_over_rect.height + new_game_rect.height + quit_game_rect.height + 70,
        )

        self.surface.blit(game_over_font, game_over_rect)
        self.surface.blit(new_game_font, new_game_rect)
        self.surface.blit(quit_game_font, quit_game_rect)
        pygame.draw.rect(self.surface, (100, 100, 100), bg_rect, 1)
