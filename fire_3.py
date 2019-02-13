import math
from random import randint
import pygame
import os

pygame.init()

pygame.key.set_repeat(200, 70)
second_all_sprite = pygame.sprite.Group()
pushka_sprite = pygame.sprite.Group()
ground_sprite = pygame.sprite.Group()
mishen_sprite = pygame.sprite.Group()
screen = pygame.display.set_mode((420, 420))
width = height = 420


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


class Ball(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, a, v, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(second_all_sprite)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.left = x
        self.top = y
        self.v = v
        self.a = a
        self.pos_x = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.vresalsy = False

    def update(self, mishen_sprite):
        if not pygame.sprite.collide_mask(self, On().mishen):
            self.pos_x += 3
            self.rect.x = self.pos_x + self.left
            self.rect.y = self.top - (int(self.pos_x * math.tan(math.radians(self.a)) - (9.8 * self.pos_x ** 2) / (
                    2 * self.v ** 2 * math.cos(math.radians(self.a)) ** 2)))
        else:
            self.vresalsy = True
            On.mishen.new_lvl()

    def get_event(self, event):
        pass


class Pushka(pygame.sprite.Sprite):
    imagee = load_image('pushka.png')

    def __init__(self):
        super().__init__(pushka_sprite, second_all_sprite)
        self.image = Pushka.imagee
        self.rect = pygame.Rect(-50, height - 104, 50, 50)
        self.angle = 0
        self.defult = (50, self.rect.y + 54)
        self.came = False

    def update(self, angle):
        if 70 >= self.angle + angle >= 0:
            self.angle += angle
            self.image = pygame.transform.rotate(Pushka.imagee, self.angle)
            self.rect.x = self.defult[0] + (54 * math.sin(math.radians(self.angle))) - self.angle
            self.rect.y = self.defult[1] - (54 * math.cos(math.radians(self.angle))) - self.angle

    def coming(self):
        if self.rect.x != 50 and not self.came:
            self.rect.x += 2
        else:
            self.came = True


class Mishen(pygame.sprite.Sprite):
    image = load_image('mishen.png')
    lvl = {1: (randint(150, 350), randint(100, 272)), 2: (randint(150, 350), randint(100, 272)),
           3: (randint(150, 350), randint(100, 272)), 4: (randint(150, 350), randint(100, 272)),
           5: (randint(150, 350), randint(100, 272)), 6: (randint(150, 350), randint(100, 272))}
    lvl_now = 1

    def __init__(self):
        super().__init__(mishen_sprite, second_all_sprite)
        self.image = Mishen.image
        self.rect = self.image.get_rect()
        self.rect.x = Mishen.lvl[self.lvl_now][0]
        self.rect.y = Mishen.lvl[self.lvl_now][1]
        self.mask = pygame.mask.from_surface(self.image)

    def new_lvl(self):
        self.rect.x = randint(150, 350)
        self.rect.y = randint(100, 272)


class Heart(pygame.sprite.Sprite):
    imagee = load_image('heart.png')

    def __init__(self, pos_x):
        super().__init__(pushka_sprite, second_all_sprite)
        self.image = Heart.imagee
        self.rect = pygame.Rect(pos_x, 50, 30, 26)


class On:
    push = Pushka()
    mishen = Mishen()
    screen = screen
    ball = None

    def __init__(self):
        pass

    def polet(self):

        self.hearts = []  # создание сердец
        x_pos = 300
        for i in range(3):
            c = Heart(x_pos)
            x_pos += 30
            self.hearts.append(c)

        self.push.came = False
        self.push.rect.x = -50
        flying = False  # снаряд летит
        running = True
        clock = pygame.time.Clock()
        fon = pygame.transform.scale(load_image('fon_zap.jpg'), (width, height))
        v = 55  # пикселей в секунду
        fps = 60
        lifes = 3
        while running:
            self.screen.blit(fon, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or lifes == 0:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and self.push.came:
                    self.push.update(-5)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and self.push.came:
                    self.push.update(5)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not flying and self.push.came and lifes != 0:
                    self.ball = Ball(self.push.angle, v,
                                     self.push.rect.x + int(
                                         math.cos(math.radians(self.push.angle)) * 100 + self.push.angle * 0.14),
                                     self.push.rect.y - int(
                                         math.sin(math.radians(self.push.angle)) * 75) + self.push.angle * 0.84 + 10)
                    flying = True
            if flying:
                self.ball.update(mishen_sprite)
                if self.ball.rect[0] >= 1000 or self.ball.rect[1] > (self.push.rect[1] + 50):
                    second_all_sprite.remove(self.ball)
                    flying = False
                    lifes -= 1
                    second_all_sprite.remove(self.hearts[-1])
                    self.hearts.pop(-1)
                elif self.ball.vresalsy:
                    self.push.update(self.push.angle * -1)
                    clock.tick(2)
                    flying = False
                    second_all_sprite.remove(self.ball)
                    running = False
                    for i in self.hearts:
                        second_all_sprite.remove(i)
                clock.tick(2000)
            if lifes == 0:
                self.push.update(self.push.angle * -1)
                running = False
            self.push.coming()
            second_all_sprite.draw(self.screen)
            pygame.display.flip()
            clock.tick(fps)
