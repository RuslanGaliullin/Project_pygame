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
mishen_image = load_image('mishen.png')


class Pushka(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(pushka_sprite, second_all_sprites)
        self.image = pushka_image
        self.rect = pygame.Rect(80, 400, 50, 50)
        self.angle = 0

    def update(self, angle):
        if 70 >= self.angle + angle >= 0:
            self.angle += angle
            self.image = pygame.transform.rotate(pushka_image, self.angle)
            self.rect.x = 100 + (54 * math.sin(math.radians(self.angle))) - self.angle
            self.rect.y = 450 - (54 * math.cos(math.radians(self.angle))) - self.angle


class Mishen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(mishen_sprite, second_all_sprites)
        self.image = mishen_image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 350
        self.mask = pygame.mask.from_surface(self.image)

    def check(self):
        pass


player_image = load_image('pushka.png')

running = True
flying = False
push = Pushka()
clock = pygame.time.Clock()
fon = pygame.transform.scale(load_image('fon_zap.jpg'), (600, 500))

v = 50  # пикселей в секунду
fps = 60
mishen = Mishen()
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
                        push.rect.x + int(math.cos(math.radians(push.angle)) * 100 + push.angle * 0.14),
                        push.rect.y - int(math.sin(math.radians(push.angle)) * 75) + push.angle * 0.84 + 10)
            flying = True
    if flying:
        ball.update(mishen_sprite)
        mishen.check()
        if ball.rect[0] >= 1000 or ball.rect[1] > (push.rect[1] + 75):
            second_all_sprites.remove(ball)
            flying = False
        elif ball.vresalsy:
            clock.tick(1)
            second_all_sprites.remove(ball)
            flying = False
    second_all_sprites.draw(screen)
    pygame.display.flip()
    d = v / fps
    clock.tick(fps)
