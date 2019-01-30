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
        self.left = x
        self.top = y
        self.v = v
        self.a = a
        self.pos_x = 0

    def update(self):
        self.pos_x += 3
        self.rect.x = self.pos_x + self.left
        self.rect.y = self.top - (int(self.pos_x * math.tan(math.radians(self.a)) - (9.8 * self.pos_x ** 2) / (
                2 * self.v ** 2 * math.cos(math.radians(self.a)) ** 2)))

    def get_event(self, event):
        pass
