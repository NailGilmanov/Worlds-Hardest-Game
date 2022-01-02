import os
import sys

import pygame

pygame.init()
size = width, height = 1608, 938
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Worlds hardest game!!!!!!!')

FPS = 50
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("data/soundtrack.mp3")
pygame.mixer.music.play(-1)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["САМАЯ СЛОЖНАЯ ИГРА В МИРЕ", "",
                  "Правила игры:",
                  "Собрать все монеты",
                  "и прийти к финишу"]

    fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('azure'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'purple': load_image('purple_cell.png'),
    'white': load_image('white_cell.png'),
    'fon': load_image('fon.png'),
    'green': load_image('green_cell.png')
}

player_image = load_image('main_hero.png')

tile_width = tile_height = 67
hero_width = hero_height = 48

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            hero_width * pos_x + 15, hero_height * pos_y + 5)


horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        all_sprites.add(self)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


Border(3 * tile_width, 4 * tile_height, 6 * tile_width, 4 * tile_height)
Border(16 * tile_width, 4 * tile_height, 21 * tile_width, 4 * tile_height)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('fon', x, y)
            elif level[y][x] == '#':
                Tile('white', x, y)
            elif level[y][x] == ',':
                Tile('green', x, y)
            elif level[y][x] == '!':
                pass
                Tile('purple', x, y)
            elif level[y][x] == '@':
                Tile('green', x, y)
                new_player = Player(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


player, level_x, level_y = generate_level(load_level('level1.txt'))

clock = pygame.time.Clock()

start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Список нажатых клавиш
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
    if keys[pygame.K_UP]:
        player.rect.y -= 5
    if keys[pygame.K_DOWN]:
        player.rect.y += 5

    # Рендер
    tiles_group.draw(screen)
    player_group.draw(screen)
    horizontal_borders.draw(screen)
    vertical_borders.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
