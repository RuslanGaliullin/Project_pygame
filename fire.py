import pygame
import os
import math

from class_ball import Ball

pygame.init()

pygame.key.set_repeat(200, 70)
second_all_sprites = pygame.sprite.Group()
pushka_sprite = pygame.sprite.Group()
ground_sprite = pygame.sprite.Group()
mishen_sprite = pygame.sprite.Group()

screen = pygame.display.set_mode((600, 500))
screen2 = pygame.Surface(screen.get_size())


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


pushka_image = load_image('pushka.png')


class Pushka(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pushka_sprite, second_all_sprites)
        self.image = pushka_image
        self.rect = pygame.Rect(60, 400, 50, 50)
        self.angle = 0

    def update(self, angle):
        if 70 >= self.angle + angle >= 0:
            self.angle += angle
            self.image = pygame.transform.rotate(pushka_image, self.angle)
            self.rect.x = 74 + (36 * math.sin(math.radians(self.angle))) - self.angle * 0.89
            self.rect.y = 433 - (36 * math.cos(math.radians(self.angle))) - self.angle * 0.45911112


player_image = load_image('pushka.png')

running = True
flying = False
push = Pushka()
clock = pygame.time.Clock()
fon = pygame.transform.scale(load_image('fon_zap.jpg'), (600, 500))

v = 50  # пикселей в секунду
fps = 60

while running:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            push.update(-5)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            push.update(5)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not flying:
            if flying:
                second_all_sprites.remove(ball)
            ball = Ball(second_all_sprites, push.angle, v,
                        push.rect.x + int(math.cos(math.radians(push.angle)) * 50),
                        push.rect.y - int(math.sin(math.radians(push.angle)) * 50) + push.angle * 0.6)
            flying = True
    if flying:
        try:
            ball.update()
            if ball.rect[0] >= 1000 or ball.rect[1] > push.rect[1]:
                second_all_sprites.remove(ball)
                flying = False
        except Exception:
            print(0)
    second_all_sprites.draw(screen)
    pygame.display.flip()
    d = v / fps
    clock.tick(fps)
