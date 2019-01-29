import math
import pygame
import os

h = 1000
w = 1000
running = True
screen = pygame.display.set_mode((h, w))


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

    def __init__(self, group, a, v, x, y):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.top = y
        self.rect.y = y
        self.v = v
        self.a = a

    def update(self):
        self.rect.x += 1
        self.rect.y = int(self.rect.x * math.tan(math.radians(self.a)) - (9.8 * self.rect.x ** 2) / (
                2 * self.v ** 2 * math.cos(math.radians(self.a)) ** 2)) + self.top

    # Поручим бомбочке получать событие и взрываться (поменяем картинку)
    def get_event(self, event):
        pass

