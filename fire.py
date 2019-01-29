import pygame
import os

pygame.init()
second_all_sprites = pygame.sprite.Group()
pushka_sprite = pygame.sprite.Group()
ground_sprite = pygame.sprite.Group()
mishen_sprite = pygame.sprite.Group()

screen = pygame.display.set_mode((500, 500))
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
        self.rect = (0, 0)
        self.angle = 0

    def update(self, angle):
        self.angle += angle
        self.image = pygame.transform.rotate(screen, self.angle)


player_image = load_image('pushka.png')

running = True
push = Pushka()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            push.update(5)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            push.update(-5)
    second_all_sprites.draw(screen)
    pygame.display.flip()
