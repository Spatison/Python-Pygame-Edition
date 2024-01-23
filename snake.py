import pygame
import os
import random
import sys

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.flip()
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def terminate():
    pygame.quit()
    sys.exit()


def game():
    board = Board(16, 18)
    BG()
    r = 0
    font = pygame.font.Font(None, 30)
    text_coord = (25, 90)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[119] and r % 4 != 2:
                    if r % 4 == 3:
                        board.rotat = 1
                    elif r % 4 == 1:
                        board.rotat = -1
                    r = 0
                elif pygame.key.get_pressed()[115] and r % 4 != 0:
                    if r % 4 == 1:
                        board.rotat = 1
                    elif r % 4 == 3:
                        board.rotat = -1
                    r = 2
                elif pygame.key.get_pressed()[100] and r % 4 != 3:
                    if r % 4 == 0:
                        board.rotat = 1
                    elif r % 4 == 2:
                        board.rotat = -1
                    r = 1
                elif pygame.key.get_pressed()[97] and r % 4 != 1:
                    if r % 4 == 2:
                        board.rotat = 1
                    elif r % 4 == 0:
                        board.rotat = -1
                    r = 3
        screen.fill((0, 0, 0))
        if board.update() == 'Game Over':
            return
        all_BG.draw(screen)
        all_snake.draw(screen)
        all_snake.update()
        string_rendered = font.render(str(board.snake_size - 4), 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord[0]
        intro_rect.x = text_coord[1]
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(7)


def game_over():
    Gover()
    gv = Gover()
    gv.rect.y = 300
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0, 0, 255))
        all_BG.draw(screen)
        all_BG.update()
        clock.tick(200)
        pygame.display.flip()


def start_screen():
    fon = pygame.transform.scale(load_image('start_screen.png'), (600, 600))
    screen.blit(fon, (0, 0))
    play = Play()
    exit = Exit()
    all_button.draw(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit.update(event):
                terminate()
            elif play.update(event):
                return
        pygame.display.flip()
        clock.tick(60)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[8][7] = 2
        self.board[8][8] = 3
        self.board[8][9] = 4
        self.board[8][10] = 5
        self.left = 31
        self.top = 95
        self.cell_size = 32
        self.snake_size = 4
        self.rotat = 0
        self.apple = False

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (0, 255, 0), (self.left + self.cell_size * j, self.top + self.cell_size * i
                                                           , self.cell_size, self.cell_size), 1)

    def get_cord(self, pos):
        board_width = self.width * self.cell_size
        board_height = self.height * self.cell_size
        if self.left < pos[0] < self.left + board_width:
            if self.top < pos[1] < self.top + board_height:
                cord = (pos[1] - self.left) // self.cell_size, (pos[0] - self.top) // self.cell_size
                return cord
        return None

    def update(self):
        board_new = [[0] * self.width for _ in range(self.height)]
        for item in all_snake:
            if True:
                item.kill()
                all_snake.clear(screen, BG.image)
        for i in range(self.width):
            for j in range(self.height):
                a = self.board[j][i]
                b = (0, 1, self.snake_size + 1)
                try:
                    if a == 2:
                        if self.rotat == 0:
                            if self.board[j][i + 1] == 3 and self.board[j][i - 1] in b:
                                Snake(0, j, i)
                                board_new[j][i - 1] = 2
                                if self.board[j][i - 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j][i - 1] == 3 and self.board[j][i + 1] in b:
                                Snake(1, j, i)
                                board_new[j][i + 1] = 2
                                if self.board[j][i + 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j + 1][i] == 3 and self.board[j - 1][i] in b:
                                Snake(2, j, i)
                                board_new[j - 1][i] = 2
                                if self.board[j - 1][i] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j - 1][i] == 3 and self.board[j + 1][i] in b:
                                Snake(3, j, i)
                                board_new[j + 1][i] = 2
                                if self.board[j + 1][i] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            else:
                                return 'Game Over'
                        elif self.rotat == 1:
                            if self.board[j][i + 1] == 3 and self.board[j + 1][i] in b:
                                Snake(0, j, i)
                                board_new[j + 1][i] = 2
                                if self.board[j + 1][i] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j][i - 1] == 3 and self.board[j - 1][i] in b:
                                Snake(1, j, i)
                                board_new[j - 1][i] = 2
                                if self.board[j - 1][i] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j + 1][i] == 3 and self.board[j][i - 1] in b:
                                Snake(2, j, i)
                                board_new[j][i - 1] = 2
                                if self.board[j][i - 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j - 1][i] == 3 and self.board[j][i + 1] in b:
                                Snake(3, j, i)
                                board_new[j][i + 1] = 2
                                if self.board[j][i + 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            else:
                                return 'Game Over'
                        else:
                            if self.board[j][i + 1] == 3 and self.board[j - 1][i] in b:
                                Snake(0, j, i)
                                board_new[j - 1][i] = 2
                                if self.board[j - 1][i] == 1:
                                    self.snake_size + 1
                                    self.apple = False
                            elif self.board[j][i - 1] == 3 and self.board[j + 1][i] in b:
                                Snake(1, j, i)
                                board_new[j + 1][i] = 2
                                if self.board[j + 1][i] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j + 1][i] == 3 and self.board[j][i + 1] in b:
                                Snake(2, j, i)
                                board_new[j][i + 1] = 2
                                if self.board[j][i + 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            elif self.board[j - 1][i] == 3 and self.board[j][i - 1] in b:
                                Snake(3, j, i)
                                board_new[j][i - 1] = 2
                                if self.board[j][i - 1] == 1:
                                    self.snake_size += 1
                                    self.apple = False
                            else:
                                return 'Game Over'
                        board_new[j][i] = 3
                        self.rotat = 0
                    elif a - 1 == self.snake_size:
                        if self.board[j][i - 1] == a - 1:
                            Snake(10, j, i)
                        elif self.board[j][i + 1] == a - 1:
                            Snake(11, j, i)
                        elif self.board[j - 1][i] == a - 1:
                            Snake(12, j, i)
                        else:
                            Snake(13, j, i)
                    elif a > 2:
                        if (self.board[j][i + 1] == a - 1 or self.board[j][i + 1] == a + 1) and \
                            (self.board[j][i - 1] == a - 1 or self.board[j][i - 1] == a + 1):
                            Snake(4, j, i)
                        elif (self.board[j + 1][i] == a - 1 or self.board[j + 1][i] == a + 1) and \
                            (self.board[j - 1][i] == a - 1 or self.board[j - 1][i] == a + 1):
                            Snake(5, j, i)
                        elif (self.board[j][i - 1] == a - 1 or self.board[j][i - 1] == a + 1) and \
                            (self.board[j + 1][i] == a - 1 or self.board[j + 1][i] == a + 1):
                            Snake(6, j, i)
                        elif (self.board[j][i + 1] == a - 1 or self.board[j][i + 1] == a + 1) and \
                            (self.board[j + 1][i] == a - 1 or self.board[j + 1][i] == a + 1):
                            Snake(7, j, i)
                        elif (self.board[j][i + 1] == a - 1 or self.board[j][i + 1] == a + 1) and \
                            (self.board[j - 1][i] == a - 1 or self.board[j - 1][i] == a + 1):
                            Snake(8, j, i)
                        elif (self.board[j][i - 1] == a - 1 or self.board[j][i - 1] == a + 1) and \
                            (self.board[j - 1][i] == a - 1 or self.board[j - 1][i] == a + 1):
                            Snake(9, j, i)
                        board_new[j][i] = a + 1
                except:
                    return 'Game Over'
                if a == 1 and self.board[j][i] == 1 and board_new[j][i] == 0:
                    board_new[j][i] = 1
                    Apple(j, i)
        if not self.apple:
            x, y = random.randint(0, 14), random.randint(0, 16)
            while board_new[y][x] != 0:
                x, y = random.randint(0, 14), random.randint(0, 16)
            self.apple = True
            board_new[y][x] = 1
        self.board = board_new


class BG(pygame.sprite.Sprite):
    image = load_image("BG.png")

    def __init__(self):
        super().__init__(all_BG)
        self.image = BG.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 0
        self.rect.y = 0


class Play(pygame.sprite.Sprite):
    image = load_image('start.png', color_key=-1)
    def __init__(self):
        super().__init__(all_button)
        self.image = Play.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 130
        self.rect.y = 250

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True


class Exit(pygame.sprite.Sprite):
    image = load_image('Exit.png', color_key=-1)
    def __init__(self):
        super().__init__(all_button)
        self.image = Exit.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 180
        self.rect.y = 450

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            return True


class Gover(pygame.sprite.Sprite):
    image = load_image('gameover.png')

    def __init__(self):
        super().__init__(all_BG)
        self.image = Gover.image
        self.rect = self.image.get_rect()
        self.spead = 1
        self.rect.x = -600
        self.rect.y = 0

    def update(self):
        self.rect = self.rect.move(self.spead, 0)
        if self.rect.x == 0:
            self.spead = 0


class Snake(pygame.sprite.Sprite):
    snake_head_top = load_image("snake_head_top.png", color_key=-1)
    snake_head_down = load_image("snake_head_down.png", color_key=-1)
    snake_head_right = load_image("snake_head_right.png", color_key=-1)
    snake_head_left = load_image("snake_head_left.png", color_key=-1)
    snake_end_top = load_image("snake_end_top.png", color_key=-1)
    snake_end_down = load_image("snake_end_down.png", color_key=-1)
    snake_end_right = load_image("snake_end_right.png", color_key=-1)
    snake_end_left = load_image("snake_end_left.png", color_key=-1)
    snake_body_horizont = load_image("snake_body_horizont.png", color_key=-1)
    snake_body_vertical = load_image("snake_body_vertical.png", color_key=-1)
    snake_body_TR = load_image("snake_body_TR.png", color_key=-1)
    snake_body_DR = load_image("snake_body_DR.png", color_key=-1)
    snake_body_DL = load_image("snake_body_DL.png", color_key=-1)
    snake_body_TL = load_image("snake_body_TL.png", color_key=-1)

    def __init__(self, id, x, y):
        super().__init__(all_snake)
        if id == 0:
            self.image = Snake.snake_head_top
        elif id == 1:
            self.image = Snake.snake_head_down
        elif id == 2:
            self.image = Snake.snake_head_left
        elif id == 3:
            self.image = Snake.snake_head_right
        elif id == 4:
            self.image = Snake.snake_body_vertical
        elif id == 5:
            self.image = Snake.snake_body_horizont
        elif id == 6:
            self.image = Snake.snake_body_TR
        elif id == 7:
            self.image = Snake.snake_body_DR
        elif id == 8:
            self.image = Snake.snake_body_DL
        elif id == 9:
            self.image = Snake.snake_body_TL
        elif id == 10:
            self.image = Snake.snake_end_top
        elif id == 11:
            self.image = Snake.snake_end_down
        elif id == 12:
            self.image = Snake.snake_end_left
        elif id == 13:
            self.image = Snake.snake_end_right
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x * 32 + 31
        self.rect.y = y * 32 + 95


class Apple(pygame.sprite.Sprite):
    gamepad = load_image('gamepad.png', color_key=-1)
    def __init__(self, x, y):
        super().__init__(all_snake)
        self.image = Apple.gamepad
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x * 32 + 31
        self.rect.y = y * 32 + 95


if __name__ == "__main__":
    all_snake = pygame.sprite.Group()
    all_BG = pygame.sprite.Group()
    all_button = pygame.sprite.Group()
    clock = pygame.time.Clock()
    start_screen()
    while True:
        game()
        game_over()
        for item in all_snake:
            if True:
                item.kill()
                all_snake.clear(screen, BG.image)
        for item in all_button:
            if True:
                item.kill()
                all_button.clear(screen, BG.image)
        for item in all_BG:
            if True:
                item.kill()
                all_BG.clear(screen, BG.image)