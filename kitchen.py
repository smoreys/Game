import pygame
import sys
import os
from final import final


def runkitchen(tf=False):
    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.left = 150
            self.top = 300
            self.cell_size = 60
            self.room_locked = True

        def set_view(self, left, top, cell_size):
            self.left = left
            self.top = top
            self.cell_size = cell_size

        def render(self, screen):
            if self.room_locked:
                x = pygame.Color(32, 178, 170)
                door_closed.draw(screen)
            else:
                x = pygame.Color(127, 255, 212)
                door_open.draw(screen)
            pygame.draw.rect(screen, pygame.Color(0, 255, 255), (self.left, self.top, 8 * self.cell_size, 5 * self.cell_size))
            for i in range(self.height):  #рисуем поле
                for j in range(self.width):
                    pygame.draw.rect(screen, x, (self.cell_size * j + self.left,
                                                                          self.cell_size * i + self.top, self.cell_size,
                                                                          self.cell_size), 2)
            coords = (400, 10, 70, 70) #рисуем инвентарные коробки
            pygame.draw.rect(screen, x, (self.left, self.top - 170, 480, 170), 4)  # стена с дверью
            for i in range(5):
                pygame.draw.rect(screen, pygame.Color(0, 139, 139), (coords[0] + i * 65, coords[1], coords[2], coords[3]), 5)
            pygame.draw.rect(screen, pygame.Color(0, 139, 139), (1 * self.cell_size + self.left, self.top + self.cell_size * 3, self.cell_size, self.cell_size))
            #магия отменяется, дев нашел спрайты


    class Hero:
        def __init__(self):
            self.stuff = []
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
            self.move = {'up': [(0, -7), self.up], 'down': [(0, 7), self.down],
                         'left': [(-7, 0), self.toleft], 'right': [(7, 0), self.right]}
            self.t, self.t1, self.ff, self.gw, self.fk = False, False, False, False, False
            with open('lomishere.txt', 'r') as file:
                self.lomm = file.read()

        def get_rect(self, x, y):
            one = (x - self.top) // self.cell_size
            sec = (y - self.left) // self.cell_size
            return one, sec

        def drawing(self):
            sprite.image = load_image(self.animation[self.direction][1])
            all_sprites.draw(screen)

        def moving(self, x, y, direction):
            self.direction = direction
            sprite.image = load_image(self.animation[direction][self.move[direction][1]])
            new_x = x + self.move[direction][0][0]
            new_y = y + self.move[direction][0][1]
            rect_x, rect_y = self.get_rect(new_x, new_y)
            if self.move[direction][1] == 3:
                self.move[direction][1] = 0
            else:
                self.move[direction][1] += 1
            if self.left + self.cell_size * 6.4 - 5> new_x > self.left and self.top - 50 < new_y < self.top + self.cell_size * 4 - 35:
                if new_y < 280 and rect_x in (-2, -1, 1, 0, 4, 5, 3):
                    return [x, y]
                return [new_x, new_y]
            else:
                return [x, y]

        def interaction(self, x, y, cuboc_counter):
            sx, sy = hero.get_rect(x, y)
            if sx == -1 and sy == 4 and self.lomm:
                all_sprites.add(tool1)
                self.t1 = True
                lom.image = load_image('space.png', (255, 255, 255))
            elif self.t1 and sx in (0, -1, 1) and sy == 2:
                all_sprites.add(tool)
                self.t = True
                tool1.image = load_image('space.png', (255, 255, 255))
            elif self.t and sx in (-1, -2) and sy == 2:
                self.ff = True
                tool.image = load_image('space.png', (255, 255, 255))
                all_sprites.add(frozen_fish)
            elif self.ff and sx in (4, 3) and sy == 2:
                self.gw = True
                frozen_fish.image = load_image('space.png', (255, 255, 255))
                all_sprites.add(water_glass)
            elif sx == 4 and sy in (4, 5) and self.gw:
                self.fk = True
                water_glass.image = load_image('space.png', (255, 255, 255))
                all_sprites.add(final_key)
            elif sx == 2 and sy in (2, 3, 4, 1, 0) and self.fk:
                if not board.room_locked:
                    return cuboc_counter, True
                board.room_locked = False
                return int(cuboc_counter) + 1, False
            return cuboc_counter, False


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
    board = Board(8, 5)
    all_sprites = pygame.sprite.Group()
    door_open = pygame.sprite.Group()
    d_open = pygame.sprite.Sprite()
    d_open.image = load_image("open-door.png", (166, 172, 186))
    d_open.image = pygame.transform.scale(d_open.image, (120, 170))
    d_open.rect = d_open.image.get_rect()
    d_open.rect = [400, 135]
    door_open.add(d_open)
    door_closed = pygame.sprite.Group()
    d_closed = pygame.sprite.Sprite()
    d_closed.image = load_image('closed-door.png', (76, 80, 86))
    d_closed.image = pygame.transform.scale(d_closed.image, (90, 150))
    d_closed.rect = d_closed.image.get_rect()
    d_closed.rect = [400, 150]
    door_closed.add(d_closed)

    sprite, fridge, shave1, shave2, shave3, sink, table, chair1, chair2, plant, cuboc = pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()
    tool1, tool, frozen_fish, water_glass, final_key, lom = pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()
    spr = {'tool1': [tool1, (255, 246, 247), [55, 55], (409, 17)], 'tool': [tool, (255, 247, 248), [60, 60], (475, 13)],
           'frozenfish': [frozen_fish, (255, 255, 255), [65, 70], (533, 10)], 'water': [water_glass, (255, 255, 255), [50, 65], (603, 10)],
           'finalkey': [final_key, (255, 255, 255), [55, 55], (670, 15)]}
    for i in spr:
        spr[i][0].image = load_image(i + '.png', spr[i][1])
        spr[i][0].image = pygame.transform.scale(spr[i][0].image, spr[i][2])
        spr[i][0].rect = spr[i][0].image.get_rect()
        spr[i][0].rect = spr[i][3]
    sprites = {'cuboc': ((252, 252, 252), cuboc, (100, 100), [700, 700]), 'fridge': ((255, 246, 247), fridge, (130, 220), [150, 130]),
               'shave1': ((255, 246, 247), shave1, (120, 200), [273, 150]), 'sink': ((255, 246, 247), sink, (110, 200), [518, 150]),
               'up-stand': (None, sprite, None, [330, 450]), 'plant': ((0, 0, 0), plant, (80, 120), [553, 479]), 'lom': [(255, 255, 255), lom, [55, 55], (670, 15)]}
    for i in sprites:
        sprites[i][1].image = load_image(i + '.png', sprites[i][0])
        if sprites[i][2]:
            sprites[i][1].image = pygame.transform.scale(sprites[i][1].image, sprites[i][2])
        sprites[i][1].rect = sprites[i][1].image.get_rect()
        sprites[i][1].rect = sprites[i][3]
        all_sprites.add(sprites[i][1])
    if tf:
        pygame.init()
        pygame.display.set_caption('Уровень 2. Кухня')
        running = True
        screen.fill((0, 0, 0))
        board.render(screen)
        font = pygame.font.Font(None, 70)
        x = 670
        y = 730
        tf = False
        with open('points.txt', 'r') as point:
            cuboc_counter = point.read()
        hero = Hero()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'up')
                elif keys[pygame.K_a]:
                    sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'left')
                elif keys[pygame.K_d]:
                    sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'right')
                elif keys[pygame.K_s]:
                    sprite.rect = hero.moving(sprite.rect[0], sprite.rect[1], 'down')
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        cuboc_counter, tf = hero.interaction(sprite.rect[0], sprite.rect[1], cuboc_counter)
                else:
                    hero.drawing()
                screen.fill((152, 251, 152))
                board.render(screen)
                all_sprites.draw(screen)
                with open('points.txt', 'w') as text:
                    text.write(str(cuboc_counter))
                line2 = font.render(str(cuboc_counter), True, (255, 255, 255))
                screen.blit(line2, (x, y))
                pygame.display.flip()
                if tf:
                    return True
    return True
