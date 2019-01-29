from board import Board
from walls import Walls, load_image
import pygame
import random
screen = pygame.display.set_mode((1400,770))
board = Board(50, 28)
running = True
all_sprites = pygame.sprite.Group()
for i in range(100):
    w = Walls(all_sprites, (random.randint(0, 50) * board.cell_size + board.left, random.randint(0,28) * board.cell_size+board.top))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass
    screen.fill((0, 0, 0))
    board.render()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
