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
        self.box_close = True

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        # x - код цвета в зависимости от того, открыта дверь или нет
        if self.room_locked:
            x = pygame.Color(100, 255, 100)
            # рисуем дверь закрытую
            pygame.draw.rect(screen, x, (self.left + 200, self.top - 120, 80, 120), 5)
        else:
            x = pygame.Color(0, 170, 255)
            # рисуем дверь открытую
            pygame.draw.rect(screen, x, (self.left + 200, self.top - 120, 80, 120), 5)
            pygame.draw.line(screen, x, (self.left + 200, self.top - 120), (self.left + 220, self.top - 80), 5)
            pygame.draw.line(screen, x, (self.left + 200, self.top), (self.left + 220, self.top - 20), 5)
            pygame.draw.line(screen, x, (self.left + 220, self.top - 20), (self.left + 220, self.top - 80), 5)
        for i in range(self.height):  #рисуем поле
            for j in range(self.width):
                pygame.draw.rect(screen, x, (self.cell_size * j + self.left,
                                                                      self.cell_size * i + self.top, self.cell_size,
                                                                      self.cell_size), 2)

        pygame.draw.rect(screen, x, (self.left, self.top - 170, 480, 170), 4) #стена с дверью
        # рисуем кровать
        pygame.draw.rect(screen, pygame.Color(255, 0, 255), (6 * self.cell_size + self.left, self.top, 2 * self.cell_size, 3 * self.cell_size))
        pygame.draw.rect(screen, pygame.Color(200, 0, 200), (6 * self.cell_size + self.left, self.top + 150, 2 * self.cell_size, 0.5 * self.cell_size))
        pygame.draw.rect(screen, pygame.Color(255, 150, 255), (6 * self.cell_size + self.left + 20, self.top + 20, 2 * self.cell_size - 40, 0.5 * self.cell_size))
        #рисуем стол с компом и стулом
        pygame.draw.rect(screen, pygame.Color(200, 200, 255), (self.cell_size + self.left, self.top + self.cell_size * 5 - 2, 120, 60))
        pygame.draw.rect(screen, pygame.Color(200, 0, 200), (1.5 * self.cell_size + self.left + 2, self.top + self.cell_size * 5.25 - 2, 50, 30))
        pygame.draw.circle(screen, pygame.Color(0, 200, 150), (2 * self.cell_size + self.left - 10, self.top + self.cell_size * 5 - 30), 25)
        # ща буит магия и появится коробка с секретиками:)
        pygame.draw.rect(screen, pygame.Color(255, 222, 173), (self.left + 2.5, self.top + 1, 120, 60))
        pygame.draw.rect(screen, pygame.Color(222, 184, 135), (self.left + 2.5, self.top + 1 + 40, 120, 20))
        if self.box_close: #чекаем открыта коробка или закрыта
            pygame.draw.line(screen, pygame.Color(222, 184, 135), (self.left + 2.5, self.top + 1 + 20), (self.left + 2.5 + 119, self.top + 1 + 20), 2)
        else:
            pygame.draw.rect(screen, pygame.Color(222, 184, 135), (self.left + 2.5, self.top + 1, 120, 60))
            pygame.draw.rect(screen, pygame.Color(159, 130, 90), (self.left + 2.5 + 10, self.top + 1 + 20, 100, 20))


class Hero:
    def __init__(self):
        self.left = 150
        self.top = 250
        self.cell_size = 60
        # героя на норм картинку поменяем позже
        self.hero = [[self.left + 120, self.top + 120], [60, 120]]

    def get_rect(self, x, y):
        one = (x - self.top) // self.cell_size
        sec = (y - self.left) // self.cell_size
        return one, sec

    def drawing(self):
        pygame.draw.rect(screen, pygame.Color(0, 255, 255), (self.hero[0][0], self.hero[0][1],
                            self.hero[1][0], self.hero[1][1]))

    def moving(self, click):
        if click == 'w' and self.hero[0][1] >= self.top - 60:
            self.hero[0][1] -= 10
        elif click == 'a' and self.hero[0][0] >= self.left + 10:
            self.hero[0][0] -= 10
        elif click == 's' and self.hero[0][1] <= self.top + self.cell_size * 4 - 10:
            self.hero[0][1] += 10
        elif click == 'd' and self.hero[0][0] <= self.left + self.cell_size * 7 - 10:
            self.hero[0][0] += 10


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1. Спальня')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    board = Board(8, 6)
    running = True
    screen.fill((0, 0, 0))
    board.render(screen)
    hero = Hero()
    hero.drawing()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == 119:
                    hero.moving('w')
                elif event.key == 97:
                    hero.moving('a')
                elif event.key == 115:
                    hero.moving('s')
                elif event.key == 100:
                    hero.moving('d')
                screen.fill((0, 0, 0))
                board.render(screen)
                hero.drawing()
        pygame.display.flip()
