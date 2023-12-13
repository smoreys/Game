import pygame
import sys
import os
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
        self.hero = [[self.left, self.top + 120], [60, 120]]
        self.animation = {'up': ['up-walk-2.png', 'up-stand.png', 'up-walk-1.png', 'up-stand.png'],
                          'down': ['down-walk-2.png', 'down-stand.png', 'down-walk-1.png', 'down-stand.png'],
                          'left': ['left-walk-2.png', 'left-stand.png', 'left-walk-1.png', 'left-stand.png'],
                          'right': ['right-walk-2.png', 'right-stand.png', 'right-walk-1.png', 'right-stand.png']}
        self.direction = 'down'
        self.up = 1
        self.down = 1
        self.toleft = 1
        self.right = 1
        self.IMPORT_COORDS = [self.left, self.top, self.left + self.cell_size, self.top + 2 * self.cell_size] #коробка, кровать, стол

    def get_rect(self, x, y):
        one = (x - self.top) // self.cell_size
        sec = (y - self.left) // self.cell_size
        return one, sec

    def drawing(self):
        sprite.image = load_image(self.animation[self.direction][1])
        all_sprites.draw(screen)

    def moving_up(self, x, y):
        self.direction = 'up'
        sprite.image = load_image(self.animation['up'][self.up])
        if self.up == 3:
            self.up = 0
        else:
            self.up += 1
        if y - 5 > self.top - 110:
            return [x, y - 5]
        return [x, y]

    def moving_down(self, x, y):
        self.direction = 'down'
        sprite.image = load_image(self.animation['down'][self.down])
        if self.down == 3:
            self.down = 0
        else:
            self.down += 1
        if y <= self.left + self.cell_size * 8 - 10:
            return [x, y + 5]
        return [x, y]

    def moving_left(self, x, y):
        self.direction = 'left'
        sprite.image = load_image(self.animation['left'][self.toleft])
        if self.toleft == 3:
            self.toleft = 0
        else:
            self.toleft += 1
        if x - 5 > self.left:
            return [x - 5, y]
        return [x, y]

    def moving_right(self, x, y):
        self.direction = 'right'
        sprite.image = load_image(self.animation['right'][self.right])
        if self.right == 3:
            self.right = 0
        else:
            self.right += 1
        if x + 10 < self.left + self.cell_size * 6.5:
            return [x + 5, y]
        return [x, y]

def load_image(name, colorkey=None):
    fullname = os.path.join('animation', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


size = width, height = 800, 800
screen = pygame.display.set_mode(size)
board = Board(8, 6)
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("down-stand.png")
sprite.rect = sprite.image.get_rect()
all_sprites.add(sprite)
sprite.rect = [200, 200]
screen.fill((255, 255, 255))
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1. Спальня')
    running = True
    screen.fill((0, 0, 0))
    board.render(screen)
    hero = Hero()
    hero.drawing()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                sprite.rect = hero.moving_up(sprite.rect[0], sprite.rect[1])
            elif keys[pygame.K_a]:
                sprite.rect = hero.moving_left(sprite.rect[0], sprite.rect[1])
            elif keys[pygame.K_d]:
                sprite.rect = hero.moving_right(sprite.rect[0], sprite.rect[1])
            elif keys[pygame.K_s]:
                sprite.rect = hero.moving_down(sprite.rect[0], sprite.rect[1])
            else:
                hero.drawing()
            screen.fill((0, 0, 0))
            board.render(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
