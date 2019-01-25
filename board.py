import pygame

running = True
screen = pygame.display.set_mode((501, 501))


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for g in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + (i * self.cell_size), self.top + (self.cell_size * g), self.cell_size,
                                  self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell != None:
            self.on_click(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] < self.left or mouse_pos[1] < self.top or mouse_pos[0] > (
                self.left + self.cell_size * self.width) \
                or mouse_pos[1] > (self.top + self.cell_size * self.height):
            return None
        else:
            pos_squar = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
            return pos_squar

    def on_click(self, cell_coords):
        pass
