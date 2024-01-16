import pygame
import sys
import os

def runbedroom(flag=False):
    class Board:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.board = [[0] * width for _ in range(height)]
            self.left = 150
            self.top = 300
            self.cell_size = 60
            self.room_locked = True #дверь открыта - False, дверь закрыта - True, если открыта, то уровень пройден

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
            #текст на картине + сама картина
            pygame.draw.rect(screen, x, (self.left, self.top - 170, 480, 170), 4) #стена с дверью
            pygame.draw.rect(screen, pygame.Color(255, 182, 193), (self.left + 5.5 * self.cell_size, 150, 130, 72))
            pygame.draw.rect(screen, pygame.Color(219, 112, 147), (self.left + 5.5 * self.cell_size, 150, 130, 72), 5)
            font = pygame.font.Font(None, 33)
            lx1 = self.left + 5.5 * self.cell_size + 10
            ly1 = 155
            line2 = font.render("110010100", True, (200, 255, 250))
            screen.blit(line2, (lx1, ly1 + 20))
            coords = (400, 10, 70, 70) #рисуем инвентарные коробки
            for i in range(5):
                pygame.draw.rect(screen, pygame.Color(255, 0, 122), (coords[0] + i * 65, coords[1], coords[2], coords[3]), 5)
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
            self.kn, self.lomm, self.k_t, self.k_d, self.pol = False, False, False, False, False

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
            if self.left + self.cell_size * 6.4 - 2 > new_x > self.left and self.top - 50 < new_y < self.top + self.cell_size * 5 - 30:
                if (rect_x < 0 and rect_y <= 1 or (rect_x == -1 or rect_x == -2 or rect_x == 0) and (rect_y == 6 or rect_y == 5)
                        or rect_x == 2 and (rect_y == 0 or rect_y == 1 or rect_y == 2)) or rect_y == 2 and (rect_x == 4 or rect_x == 3):
                    return [x, y]
                else:
                    return [new_x, new_y]
            else:
                return [x, y]


        def interaction(self, x, y, cuboc_counter):
            sx, sy = hero.get_rect(x, y)
            if sx == -2 and sy == 4:
                self.kn = True
                all_sprites.add(knife)
            elif (sx == 0 and sy in (0, 1, 2) or sx == -1 and sy == 2 or sx == -2 and sy in (2, 3, 4)) and self.kn:
                knife.image = load_image('space.png', (255, 255, 255))
                box_c.image = load_image('box-o.png', (0, 0, 0))
                box_c.image = pygame.transform.scale(box_c.image, (150, 120))
                all_sprites.add(lom)
                self.lomm = True
                with open('lomishere.txt', 'w') as file:
                    file.write('True')
                self.kn = False
                return cuboc_counter + 1, False
            elif sx == 1 and sy in (0, 1, 2) and not self.k_d:
                all_sprites.add(key_table)
                self.k_t = True
            elif self.k_t and (sy == 4 and sx in (0, -1)):
                all_sprites.add(pol)
                self.pol = True
                key_table.image = load_image('space.png', (255, 255, 255))
            elif self.pol and sx == 4 and sy == 6:
                all_sprites.add(key_door)
                self.k_d = True
                pol.image = load_image('space.png', (255, 255, 255))
            elif self.k_d and sx in (0, 1) and sy in (0, 1):
                if not board.room_locked:
                    if self.lomm:
                        return cuboc_counter, True
                    else:
                        return cuboc_counter, False
                board.room_locked = False
                return cuboc_counter + 1, False
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


    bed, box_c, sprite, plant, trash, chair, table, cuboc = pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()
    knife = pygame.sprite.Sprite()
    lom = pygame.sprite.Sprite()
    key_table = pygame.sprite.Sprite()
    key_door = pygame.sprite.Sprite()
    pol = pygame.sprite.Sprite()
    spr = {'knife': [knife, (255, 255, 255), [100, 100], (385, -5)], 'lom': [lom, (255, 255, 255), [55, 55], (670, 15)], 'key_table': [key_table, (255, 255, 255), [60, 60], (475, 13)],
           'pol': [pol, (250, 251, 253), [60, 60], (533, 15)], 'key_door': [key_door, (255, 255, 255), [60, 70], (600, 7)]}
    for i in spr:
        spr[i][0].image = load_image(i + '.png', spr[i][1])
        spr[i][0].image = pygame.transform.scale(spr[i][0].image, spr[i][2])
        spr[i][0].rect = spr[i][0].image.get_rect()
        spr[i][0].rect = spr[i][3]

    sprites = {'bed': ((32, 30, 41), bed, (300, 300), [380, 200]), 'box-c': (None, box_c, (150, 120), [130, 250]),
               'down-stand': (None, sprite, None, [300, 300]), 'plant': ((0, 0, 0), plant, (80, 120), [553, 539]),
               'trash': ((0, 0, 0), trash, (50, 60), [150, 590]), 'chair': ((0, 0, 0), chair, (70, 120), [250, 500]),
               'table': ((0, 0, 0), table, (180, 130), [200, 527]), 'cuboc': ((252, 252, 252), cuboc, (100, 100), [700, 700])}
    for i in sprites:
        sprites[i][1].image = load_image(i + '.png', sprites[i][0])
        if sprites[i][2]:
            sprites[i][1].image = pygame.transform.scale(sprites[i][1].image, sprites[i][2])
        sprites[i][1].rect = sprites[i][1].image.get_rect()
        sprites[i][1].rect = sprites[i][3]
        all_sprites.add(sprites[i][1])
    tf = False
    if flag:
        pygame.init()
        pygame.display.set_caption('Уровень 1. Спальня')
        running = True
        screen.fill((0, 0, 0))
        board.render(screen)
        font = pygame.font.Font(None, 70)
        x = 670
        y = 730
        cuboc_counter = 0
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
                screen.fill((255, 160, 122))
                board.render(screen)
                all_sprites.draw(screen)
                with open('points.txt', 'w') as text:
                    text.write(str(cuboc_counter))
                line2 = font.render(str(cuboc_counter), True, (255, 255, 255))
                screen.blit(line2, (x, y))
                pygame.display.flip()
                if tf:
                    return True
    return False
