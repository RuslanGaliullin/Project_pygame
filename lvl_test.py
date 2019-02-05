import sys
import os

import pygame

from Camer import Camera
from fire import On

FPS = 50
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 70)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tile_images = {
    'wall': load_image('wall.jpg'),
    'empty': load_image('flor.jpg'),
    'comp': load_image('complete_chel.png')
}
tiles = {}
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        tiles[(pos_x, pos_y)] = self

    def change(self, new):
        self.image = new


class Player(pygame.sprite.Sprite):
    image = load_image('pushka_player.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def rotate(self, angle):
        self.image = pygame.transform.rotate(Player.image, angle)


def generate_level(level):
    global chellenges
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#' or level[y][x] == 'p':
                c = Tile('wall', x, y)
                chellenges[(x, y)] = c
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    WIDTH, HEIGHT = 500, 500
    intro_text = ["МИНИ ИГРА ПУШКА", "",
                  "Никаких правил",
                  "Я старался"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    drawing = False
    second = False  # активация второго холста
    complete = (0, 0)  # смешение игрока при прохождении задания
    all_screens = {1: screen}
    while True:
        # all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and not drawing:
                pole = load_level('level.txt')
                a = generate_level(pole)
                for i in range(len(pole)):
                    pole[i] = list(pole[i])
                player = a[0]
                x_player = player.rect.x // 50
                y_player = player.rect.y // 50
                drawing = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and drawing:
                if pole[y_player][x_player - 1] == 'p':
                    smth = On()
                    second = True
                    complete = (-1, 0)
                elif pole[y_player][x_player - 1] != '#':
                    pole[y_player][x_player] = '.'
                    pole[y_player][x_player - 1] = '@'
                    player.rect.x -= 50
                    x_player -= 1
                    player.rotate(180)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and drawing:
                if pole[y_player][x_player + 1] == 'p':
                    smth = On()
                    second = True
                    complete = (1, 0)
                elif pole[y_player][x_player + 1] != '#':
                    pole[y_player][x_player] = '.'
                    pole[y_player][x_player + 1] = '@'
                    player.rect.x += 50
                    x_player += 1
                    player.rotate(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and drawing:
                if pole[y_player + 1][x_player] == 'p':
                    smth = On()
                    second = True
                    complete = (0, 1)
                elif pole[y_player + 1][x_player] != '#':
                    pole[y_player][x_player] = '.'
                    pole[y_player + 1][x_player] = '@'
                    player.rect.y += 50
                    y_player += 1
                    player.rotate(-90)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and drawing:
                if pole[y_player - 1][x_player] == 'p':
                    smth = On()
                    second = True
                    complete = (0, 1)
                elif pole[y_player - 1][x_player] != '#':
                    pole[y_player][x_player] = '.'
                    pole[y_player - 1][x_player] = '@'
                    player.rect.y -= 50
                    y_player -= 1
                    player.rotate(90)
        if drawing and not second:
            if 5 <= y_player < len(pole) - 6:
                flag_y = True
            else:
                flag_y = False
            if 4 <= x_player < len(pole[0]) - 5:
                flag_x = True
            else:
                flag_x = False
            camera.update(player, flag_x, flag_y)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        if second:
            smth.polet()
            screen.blit(smth.screen, (0, 0))
            if smth.ball is not None and smth.ball.vresalsy:
                player.rect.x += 50 * complete[0]
                player.rect.y += 50 * complete[1]
                pole[y_player + complete[1]][x_player + complete[0]] = '.'
                pole[y_player + complete[1]][x_player + complete[0]] = '@'
                x_player += complete[0]
                y_player += complete[1]
                tiles[(x_player, y_player)].change(load_image('flor.jpg'))
            second = False
        pygame.display.flip()
        clock.tick(FPS)


camera = Camera()
start_screen()
