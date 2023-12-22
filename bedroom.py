import pygame
import sys
import os
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 150
        self.top = 300
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
            x = pygame.Color(220, 20, 60)
            # рисуем дверь закрытую
            door_closed.draw(screen)
        else:
            x = pygame.Color(250, 128, 114)
            # рисуем дверь открытую
            door_open.draw(screen)
        pygame.draw.rect(screen, pygame.Color(230, 100, 92), (self.left, self.top, 8 * self.cell_size, 6 * self.cell_size))
        for i in range(self.height):  #рисуем поле
            for j in range(self.width):
                pygame.draw.rect(screen, x, (self.cell_size * j + self.left,
                                                                      self.cell_size * i + self.top, self.cell_size,
                                                                      self.cell_size), 2)
        #текст на картине + сама картинаs
        pygame.draw.rect(screen, x, (self.left, self.top - 170, 480, 170), 4) #стена с дверью
        pygame.draw.rect(screen, pygame.Color(255, 182, 193), (self.left + 5.5 * self.cell_size, 150, 130, 72))
        pygame.draw.rect(screen, pygame.Color(219, 112, 147), (self.left + 5.5 * self.cell_size, 150, 130, 72), 5)
        font = pygame.font.Font(None, 35)
        line1 = font.render("10010010", True, (200, 255, 100))
        lx1 = self.left + 5.5 * self.cell_size + 10
        ly1 = 155
        screen.blit(line1, (lx1, ly1))
        line2 = font.render("00101001", True, (200, 255, 250))
        screen.blit(line2, (lx1, ly1 + 20))
        line3 = font.render("10100101", True, (250, 255, 100))
        screen.blit(line3, (lx1, ly1 + 40))
        #магия отменяется, дев нашел спрайты


class Hero:
    def __init__(self):
        self.left = 150
        self.top = 250
        self.cell_size = 60
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
        self.health_per = 100
        self.happy_per = 100
        self.move = {'up': [(0, -7), self.up], 'down': [(0, 7), self.down],
                     'left': [(-7, 0), self.toleft], 'right': [(7, 0), self.right]}

    def get_rect(self, x, y):
        one = (x - self.top) // self.cell_size
        sec = (y - self.left) // self.cell_size
        return one, sec

    def drawing(self):
        sprite.image = load_image(self.animation[self.direction][1])
        all_sprites.draw(screen)

    def life(self):
        font = pygame.font.Font(None, 35)
        health_line = font.render(f"{self.health_per}%", True, (0, 0, 0))
        screen.blit(health_line, (80, 20))
        self.health_per = round((self.health_per * 100 - 2) / 100, 2)
        happy_line = font.render(f"{self.happy_per}%", True, (0, 0, 0))
        screen.blit(happy_line, (80, 80))
        self.happy_per = round((self.health_per * 100 - 2) / 100, 2)
        return (self.happy_per, self.health_per)

    def moving(self, x, y, direction):
        self.life()
        self.direction = direction
        sprite.image = load_image(self.animation[direction][self.move[direction][1]])
        if self.move[direction][1] == 3:
            self.move[direction][1] = 0
        else:
            self.move[direction][1] += 1
        if self.left + self.cell_size * 6.4 - 2 > x + self.move[direction][0][0] > self.left and self.top - 50 < y + self.move[direction][0][1] < self.top + self.cell_size * 5 - 30:
            return [x + self.move[direction][0][0], y + self.move[direction][0][1]]
        else:
            return [x, y]


def load_image(name, colorkey=None):
    fullname = os.path.join('animation', name)
    if not os.path.isfile(fullname):
        fullname = os.path.join(name)
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
door_open = pygame.sprite.Group()
d_open = pygame.sprite.Sprite()
d_open.image = load_image("open-door.png", (166, 172, 186))
d_open.image = pygame.transform.scale(d_open.image, (120, 170))
d_open.rect = d_open.image.get_rect()
d_open.rect = [350, 135]
door_open.add(d_open)
door_closed = pygame.sprite.Group()
d_closed = pygame.sprite.Sprite()
d_closed.image = load_image('closed-door.png', (76, 80, 86))
d_closed.image = pygame.transform.scale(d_closed.image, (90, 150))
d_closed.rect = d_closed.image.get_rect()
d_closed.rect = [350, 150]
door_closed.add(d_closed)


time = 0
clock = pygame.time.Clock()

bed = pygame.sprite.Sprite()
box_c, sprite, plant, trash, chair, table = pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()
health, happiness = pygame.sprite.Sprite(), pygame.sprite.Sprite()
sprites = {'bed': ((32, 30, 41), bed, (300, 300), [380, 200]), 'box-c': (None, box_c, (150, 120), [130, 250]),
           'down-stand': (None, sprite, None, [300, 300]), 'plant': ((0, 0, 0), plant, (80, 120), [553, 539]),
           'trash': ((0, 0, 0), trash, (50, 60), [150, 590]), 'chair': ((0, 0, 0), chair, (70, 120), [250, 500]),
           'table': ((0, 0, 0), table, (180, 130), [200, 527]), 'health': ((255, 255, 255), health, (100, 90), [-10,-15]),
           'happiness': ((255, 255, 255), happiness, (55, 50), [10, 60])}
for i in sprites:
    sprites[i][1].image = load_image(i + '.png', sprites[i][0])
    if sprites[i][2]:
        sprites[i][1].image = pygame.transform.scale(sprites[i][1].image, sprites[i][2])
    sprites[i][1].rect = sprites[i][1].image.get_rect()
    sprites[i][1].rect = sprites[i][3]
    all_sprites.add(sprites[i][1])
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Уровень 1. Спальня')
    running = True
    screen.fill((0, 0, 0))
    board.render(screen)
    hero = Hero()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'up')
            elif keys[pygame.K_a]:
                sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'left')
            elif keys[pygame.K_d]:
                sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'right')
            elif keys[pygame.K_s]:
                sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'down')
            else:
                hero.drawing()
            screen.fill((255, 160, 122))
            time += clock.tick() / 1000
            board.render(screen)
            hero.life()
            all_sprites.draw(screen)
            pygame.display.flip()
