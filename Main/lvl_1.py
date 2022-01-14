import sys
import os

import pygame

from fire_1 import On

FPS = 50
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 70)

pygame.mixer.music.load('data/fon.mp3')
pygame.mixer.music.play(-1)


# sound1 = pygame.mixer.Sound('data/klk.mp3')
# sound1.play()


def load_image(name, colorkey=None):  # загрузка картинок
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


def load_level(filename):  # загрузка левлов
    pygame.init()
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
    'chel': load_image('chel.png'),
    'coin': load_image('coin.png'),
    'finish': load_image('finish_1.png')
}
tiles = {}
tile_width = tile_height = 40


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
    image = load_image('pushka_player_1.png')

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = Player.image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.rect.width = tile_width
        self.rect.height = tile_width

    def rotate(self, angle):
        self.image = pygame.transform.rotate(Player.image, angle)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.' or level[y][x] == 'c' or level[y][x] == 'p':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'f':
                Tile('finish', x, y)
            if level[y][x] == 'p':
                Tile('chel', x, y)
            if level[y][x] == 'c':
                Tile('coin', x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def start_screen():
    WIDTH, HEIGHT = 400, 400
    intro_text = ["       MINI GAME PUSHKA",
                  "       Press to start",
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '',
                  '                    Press 1, 2 or 3 to choose lvl']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 5
        intro_rect.top = text_coord
        intro_rect.x = 5
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    drawing = False
    second = False  # активация второго холста
    complete = (0, 0)  # смешение игрока при прохождении задания
    all_screens = {1: screen}
    running = True
    x_player_start = None
    y_player_start = None
    while running:  # основоной цикл
        # all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and not drawing:
                pole = load_level('level_1.txt')
                a = generate_level(pole)
                for i in range(len(pole)):
                    pole[i] = list(pole[i])
                player = a[0]
                x_player = player.rect.x // tile_width
                y_player = player.rect.y // tile_width
                x_player_start = x_player
                y_player_start = y_player
                coins = 0
                drawing = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and not drawing:
                from lvl_2 import start_screen as second_lvl
                second_lvl(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3 and not drawing:
                from lvl_3 import start_screen as third_lvl
                third_lvl(0, 0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and drawing:  # передвижение
                if x_player - 1 >= 0 and pole[y_player][x_player - 1] == 'p':
                    smth = On()  # наступил на мишень
                    second = True
                    complete = (-1, 0)
                    player.rotate(180)
                elif x_player - 1 >= 0 and pole[y_player][x_player - 1] == 'c':
                    coins += 1
                    pole[y_player][x_player] = '.'
                    pole[y_player][x_player - 1] = '@'
                    player.rect.x -= tile_width
                    x_player -= 1
                    tiles_group.remove(tiles[(x_player, y_player)])
                    player.rotate(180)
                elif x_player - 1 >= 0 and pole[y_player][x_player - 1] == 'f' and coins == 3:
                    from lvl_2 import start_screen as second_lvl
                    second_lvl(pygame.time.get_ticks() / 1000)
                elif x_player - 1 >= 0 and pole[y_player][x_player - 1] != '#':
                    if pole[y_player][x_player] != 'f':
                        pole[y_player][x_player] = '.'
                    if pole[y_player][x_player - 1] != 'f':
                        pole[y_player][x_player - 1] = '@'
                    player.rect.x -= tile_width
                    x_player -= 1
                    player.rotate(180)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and drawing:
                if x_player + 1 < len(pole[0]) and pole[y_player][x_player + 1] == 'p':
                    smth = On()
                    second = True
                    complete = (1, 0)
                    player.rotate(0)
                elif x_player + 1 < len(pole[0]) and pole[y_player][x_player + 1] == 'f' and coins == 3:
                    from lvl_2 import start_screen as second_lvl
                    second_lvl(pygame.time.get_ticks() / 1000)
                elif x_player + 1 < len(pole[0]) and pole[y_player][x_player + 1] == 'c':
                    coins += 1
                    pole[y_player][x_player] = '.'
                    pole[y_player][x_player + 1] = '@'
                    player.rect.x += tile_width
                    x_player += 1
                    tiles_group.remove(tiles[(x_player, y_player)])
                    player.rotate(0)
                elif x_player + 1 < len(pole[0]) and pole[y_player][x_player + 1] != '#':
                    if pole[y_player][x_player] != 'f':
                        pole[y_player][x_player] = '.'
                    if pole[y_player][x_player + 1] != 'f':
                        pole[y_player][x_player + 1] = '@'
                    player.rect.x += tile_width
                    x_player += 1
                    player.rotate(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and drawing:
                if y_player + 1 < len(pole) and pole[y_player + 1][x_player] == 'p':
                    smth = On()
                    second = True
                    complete = (0, 1)
                    player.rotate(-90)
                elif y_player + 1 < len(pole) and pole[y_player + 1][x_player] == 'f' and coins == 3:
                    from lvl_2 import start_screen as second_lvl
                    second_lvl(pygame.time.get_ticks() / 1000)
                elif y_player + 1 < len(pole) and pole[y_player + 1][x_player] == 'c':
                    coins += 1
                    pole[y_player][x_player] = '.'
                    pole[y_player + 1][x_player] = '@'
                    player.rect.y += tile_width
                    y_player += 1
                    tiles_group.remove(tiles[(x_player, y_player)])
                    player.rotate(-90)
                elif y_player + 1 < len(pole) and pole[y_player + 1][x_player] != '#':
                    if pole[y_player][x_player] != 'f':
                        pole[y_player][x_player] = '.'
                    if pole[y_player + 1][x_player] != 'f':
                        pole[y_player + 1][x_player] = '@'
                    player.rect.y += tile_width
                    y_player += 1
                    player.rotate(-90)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and drawing:
                if y_player - 1 >= 0 and pole[y_player - 1][x_player] == 'p':
                    smth = On()
                    second = True
                    complete = (0, -1)
                    player.rotate(90)
                elif y_player - 1 >= 0 and pole[y_player - 1][x_player] == 'f' and coins == 3:
                    from lvl_2 import start_screen as second_lvl
                    second_lvl(pygame.time.get_ticks() / 1000)
                elif y_player - 1 >= 0 and pole[y_player - 1][x_player] == 'c':
                    coins += 1
                    pole[y_player][x_player] = '.'
                    pole[y_player - 1][x_player] = '@'
                    player.rect.y -= tile_width
                    y_player -= 1
                    tiles_group.remove(tiles[(x_player, y_player)])
                    player.rotate(90)
                elif y_player - 1 >= 0 and pole[y_player - 1][x_player] != '#':
                    if pole[y_player][x_player] != 'f':
                        pole[y_player][x_player] = '.'
                    if pole[y_player - 1][x_player] != 'f':
                        pole[y_player - 1][x_player] = '@'
                    player.rect.y -= tile_width
                    y_player -= 1
                    player.rotate(90)
        tiles_group.draw(screen)
        player_group.draw(screen)

        if second:
            smth.polet()
            screen.blit(smth.screen, (0, 0))
            if smth.ball is not None and smth.ball.vresalsy:  # попал в мишень
                player.rect.x += tile_width * complete[0]
                player.rect.y += tile_width * complete[1]
                pole[y_player + complete[1]][x_player + complete[0]] = '.'
                pole[y_player + complete[1]][x_player + complete[0]] = '@'
                x_player += complete[0]
                y_player += complete[1]
                tiles_group.remove(tiles[(x_player, y_player)])
            else:
                smth.mishen.lvl_now = 1  # промахнулся в мишень
                player_group.remove(player)
                pole = load_level('level_1.txt')
                a = generate_level(pole)
                for i in range(len(pole)):
                    pole[i] = list(pole[i])
                player = a[0]
                x_player = player.rect.x // tile_width
                y_player = player.rect.y // tile_width
                coins = 0
            second = False
        else:
            screen.blit(all_screens[1], (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
# Остальные уровни работают аналогично
