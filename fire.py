import pygame
import os
import math

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
        self.mask = pygame.mask.from_surface(self.image)
        self.vresalsy = False

    def update(self, mishen_sprite):
        if not pygame.sprite.collide_mask(self, mishen):
            self.pos_x += 3
            self.rect.x = self.pos_x + self.left
            self.rect.y = self.top - (int(self.pos_x * math.tan(math.radians(self.a)) - (9.8 * self.pos_x ** 2) / (
                    2 * self.v ** 2 * math.cos(math.radians(self.a)) ** 2)))
        else:
            self.vresalsy = True

    def get_event(self, event):
        pass


class Pushka(pygame.sprite.Sprite):
    image = load_image('pushka.png')

    def __init__(self):
        super().__init__(pushka_sprite, second_all_sprites)
        self.image = Pushka.image
        self.rect = pygame.Rect(100, 396, 50, 50)
        self.angle = 0

    def update(self, angle):
        if 70 >= self.angle + angle >= 0:
            self.angle += angle
            self.image = pygame.transform.rotate(Pushka.image, self.angle)
            self.rect.x = 100 + (54 * math.sin(math.radians(self.angle))) - self.angle
            self.rect.y = 450 - (54 * math.cos(math.radians(self.angle))) - self.angle


class Mishen(pygame.sprite.Sprite):
    image = load_image('mishen.png')

    def __init__(self):
        super().__init__(mishen_sprite, second_all_sprites)
        self.image = Mishen.image
        self.rect = self.image.get_rect()
        self.rect.x = 450
        self.rect.y = 350
        self.mask = pygame.mask.from_surface(self.image)


player_image = load_image('pushka.png')
running = True
flying = False
push = Pushka()
clock = pygame.time.Clock()
fon = pygame.transform.scale(load_image('fon_zap.jpg'), (600, 500))
v = 50  # пикселей в секунду
fps = 60
mishen = Mishen()
lifes = 3
while running:
    screen.blit(fon, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or lifes == 0:
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
        if ball.rect[0] >= 1000 or ball.rect[1] > (push.rect[1] + 75):
            second_all_sprites.remove(ball)
            flying = False
            lifes -= 1
        elif ball.vresalsy:
            print(100)
            clock.tick(2)
            flying = False
            second_all_sprites.remove(ball)
    second_all_sprites.draw(screen)
    pygame.display.flip()
    d = v / fps
    clock.tick(fps)
