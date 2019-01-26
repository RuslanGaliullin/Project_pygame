from board import Board
import pygame
# поле 5 на 7
screen = pygame.display.set_mode((1400,770))
board = Board(50, 28)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
