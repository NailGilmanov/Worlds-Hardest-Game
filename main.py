import os
import sys

import pygame

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Worlds hardest game!!!!!!!')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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

    return image


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color("orange"))
    pygame.display.flip()

pygame.quit()
