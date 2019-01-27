import sys
import os

import pygame

from board import Board

FPS = 50
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 70)


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
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
    filename = "pictures/" + filename
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
    'empty': load_image('flor.jpg')
}
player_image = load_image('pushka.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
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
                drawing = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and drawing:
                if pole[player.rect.y // 50][player.rect.x // 50 - 1] != '#':
                    pole[player.rect.y // 50][player.rect.x // 50] = '.'
                    pole[player.rect.y // 50][player.rect.x // 50 - 1] = '@'
                    player.rect.x -= 50
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and drawing:
                if pole[player.rect.y // 50][player.rect.x // 50 + 1] != '#':
                    pole[player.rect.y // 50][player.rect.x // 50] = '.'
                    pole[player.rect.y // 50][player.rect.x // 50 + 1] = '@'
                    player.rect.x += 50
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and drawing:
                if pole[player.rect.y // 50 + 1][player.rect.x // 50] != '#':
                    pole[player.rect.y // 50][player.rect.x // 50] = '.'
                    pole[player.rect.y // 50 + 1][player.rect.x // 50] = '@'
                    player.rect.y += 50
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and drawing:
                if pole[player.rect.y // 50 - 1][player.rect.x // 50] != '#':
                    pole[player.rect.y // 50][player.rect.x // 50] = '.'
                    pole[player.rect.y // 50 - 1][player.rect.x // 50] = '@'
                    player.rect.y -= 50
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
