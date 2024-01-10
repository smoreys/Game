import pygame
import random
import sys
import os
from bedroom import runbedroom
from kitchen import runkitchen
from final import final

a = 0
b = 0
clock = pygame.time.Clock()

def start():
    def draw(screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)
        text = font.render("hikipsycho", True, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
        for i in range(10000):
            screen.fill(pygame.Color('white'),
                        (random.random() * width,
                         random.random() * height, 1, 1))


    if True:
        pygame.init()
        size = width, height = 800, 800
        screen = pygame.display.set_mode(size)
        draw(screen)
        pygame.display.flip()
        running = True
        f = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return False
                if event.type == pygame.KEYDOWN:
                    return True
                else:
                    draw(screen)
        pygame.quit()
