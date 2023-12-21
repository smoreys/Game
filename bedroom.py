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
        lh = 15
        lw = 15
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
        if y - 5 > self.top - 50:
            return [x, y - 5]
        return [x, y]
#переписать движение в одну функцию
    def moving_down(self, x, y):
        self.direction = 'down'
        sprite.image = load_image(self.animation['down'][self.down])
        if self.down == 3:
            self.down = 0
        else:
            self.down += 1
        if y <= self.top + self.cell_size * 5 - 30:
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
bed = pygame.sprite.Sprite()
bed.image = load_image('bed.png', (32, 30, 41))
bed.image = pygame.transform.scale(bed.image, (300, 300))
bed.rect = bed.image.get_rect()
all_sprites.add(bed)
bed.rect = [380, 200]
box_sp = pygame.sprite.Sprite()
box_sp.image = load_image("box-c.png")
box_sp.image = pygame.transform.scale(box_sp.image, (150, 120))
box_sp.rect = box_sp.image.get_rect()
all_sprites.add(box_sp)
box_sp.rect = [130, 250]
sprite = pygame.sprite.Sprite()
sprite.image = load_image("down-stand.png")
sprite.rect = sprite.image.get_rect()
sprite.rect = [300, 300]
all_sprites.add(sprite)
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
plant = pygame.sprite.Sprite()
plant.image = load_image('plant.png', (0, 0, 0))
plant.image = pygame.transform.scale(plant.image, (80, 120))
plant.rect = plant.image.get_rect()
plant.rect = [553, 539]
all_sprites.add(plant)
table = pygame.sprite.Sprite()
table.image = load_image('table.png', (0, 0, 0))
table.image = pygame.transform.scale(table.image, (180, 130))
table.rect = table.image.get_rect()
table.rect = [200, 527]
all_sprites.add(table)
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
            screen.fill((255, 160, 122))
            board.render(screen)
            all_sprites.draw(screen)
            pygame.display.flip()
