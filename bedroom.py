import pygame
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 150
        self.top = 250
        self.cell_size = 60
        self.room_locked = True #дверь открыта - False, дверь закрыта - True, если открыта, то уровень пройден

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        # x - код цвета в зависимости от того, открыта дверь или нет
        if self.room_locked:
            x = pygame.Color(100, 255, 100)
            # рисуем дверь закрытую
            pygame.draw.rect(screen, x, (self.left + 220, self.top - 70, 50, 70), 5)
        else:
            x = pygame.Color(0, 170, 255)
            # рисуем дверь открытую
            pygame.draw.rect(screen, x, (self.left + 220, self.top - 70, 50, 70), 5)
            pygame.draw.line(screen, x, (self.left + 220, self.top - 70), (self.left + 240, self.top - 50), 5)
            pygame.draw.line(screen, x, (self.left + 220, self.top), (self.left + 240, self.top - 20), 5)
            pygame.draw.line(screen, x, (self.left + 240, self.top - 50), (self.left + 240, self.top - 20), 5)
        for i in range(self.height):  #рисуем поле
            for j in range(self.width):
                pygame.draw.rect(screen, x, (self.cell_size * j + self.left,
                                                                      self.cell_size * i + self.top, self.cell_size,
                                                                      self.cell_size), 2)
                # рисуем кровать
        pygame.draw.rect(screen, x, (self.left, self.top - 100, 480, 100), 4)
        pygame.draw.rect(screen, pygame.Color(255, 0, 255), (6 * self.cell_size + self.left, self.top, 2 * self.cell_size, 3 * self.cell_size))
        pygame.draw.rect(screen, pygame.Color(200, 0, 200), (6 * self.cell_size + self.left, self.top + 150, 2 * self.cell_size, 0.5 * self.cell_size))
        pygame.draw.rect(screen, pygame.Color(255, 150, 255), (6 * self.cell_size + self.left + 20, self.top + 20, 2 * self.cell_size - 40, 0.5 * self.cell_size))

    def get_rect(self, x, y):
        one = (x - self.top) // self.cell_size
        sec = (y - self.left) // self.cell_size


class Hero:
    def __init__(self):
        self.left = 150
        self.top = 250
        self.cell_size = 60
        # героя на норм картинку поменяем позже
        self.hero = (screen, pygame.Color(0, 255, 255), (self.left + 120, self.top + 120, 60, 120))
        pygame.draw.rect(*self.hero)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1. Спальня')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    board = Board(8, 6)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render(screen)
        hero = Hero()
        pygame.display.flip()
