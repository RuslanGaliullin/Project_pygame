class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target, flag_x, flag_y):
        if flag_x:
            self.dx = -(target.rect.x + target.rect.w - 500 // 2)
        else:
            self.dx = 0
        if flag_y:
            self.dy = -(target.rect.y + target.rect.h - 500 // 2)
        else:
            self.dy = 0

