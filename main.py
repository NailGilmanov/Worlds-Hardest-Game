import os
import sys

import pygame

import time

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
    'green': load_image('green_cell.png'),
    'green_f': load_image('green_cell.png')
}

player_image = load_image('main_hero.png')
enemy_image = load_image('enemy.png')

tile_width = tile_height = 67
hero_width = hero_height = 67

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
final_zone_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'green_f':
            print('added')
            self.add(final_zone_group)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, right=None):
        self.right = right
        self.x = pos_x
        self.y = pos_y
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            hero_width * pos_x + 19.5, hero_height * pos_y + 19.5)

    def move(self):
        if self.right:
            self.rect.x += 10
            if pygame.sprite.spritecollideany(self, border_group):
                self.rect.x += self.rect.x - pygame.sprite.spritecollideany(self, border_group).rect.x
                self.right = not self.right
        else:
            self.rect.x -= 10
            if pygame.sprite.spritecollideany(self, border_group):
                self.rect.x += pygame.sprite.spritecollideany(self, border_group).rect.x + tile_width - self.rect.x
                self.right = not self.right


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            hero_width * pos_x + 15, hero_height * pos_y + 5)
        self.level = 1

    def update(self):
        if pygame.sprite.spritecollideany(self, enemy_group):
            self.__init__(self.x, self.y)

        if pygame.sprite.spritecollideany(self, border_group):
            player_can_move = False
        else:
            player_can_move = True
        if pygame.sprite.spritecollideany(self, final_zone_group):
            return 'new_level'
        return player_can_move


class Border(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(border_group, all_sprites)
        self.image = tile_images['fon']
        self.rect = self.image.get_rect().move(
            hero_width * pos_x, hero_height * pos_y)


def generate_level(level):
    new_player, x, y, new_enemy, border = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('fon', x, y)
            elif level[y][x] == '#':
                Tile('white', x, y)
            elif level[y][x] == ',':
                Tile('green', x, y)
            elif level[y][x] == '!':
                Tile('purple', x, y)
            elif level[y][x] == '@':
                Tile('green', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'L':
                Tile('purple', x, y)
                new_enemy = Enemy(x, y, right=False)
            elif level[y][x] == 'R':
                Tile('purple', x, y)
                new_enemy = Enemy(x, y, right=True)
            elif level[y][x] == 'W':
                Tile('fon', x, y)
                border = Border(x, y)
            elif level[y][x] == 'F':
                Tile('green_f', x, y)
                border = Border(x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, new_enemy, border


level = 1

player, level_x, level_y, enemy, border = generate_level(load_level('level2.txt'))

clock = pygame.time.Clock()

start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Список нажатых клавиш
    keys = pygame.key.get_pressed()

    if player.update() == 'new_level':
        level += 1
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        enemy_group.empty()
        border_group.empty()
        final_zone_group.empty()
        player, level_x, level_y, enemy, border = generate_level(load_level(f'level{level}.txt'))

    if keys[pygame.K_RIGHT]:
        player.rect.x += 5
        if not player.update():
            player.rect.x -= 5
    if keys[pygame.K_LEFT]:
        player.rect.x -= 5
        if not player.update():
            player.rect.x += 5
    if keys[pygame.K_UP]:
        player.rect.y -= 5
        if not player.update():
            player.rect.y += 5
    if keys[pygame.K_DOWN]:
        player.rect.y += 5
        if not player.update():
            player.rect.y -= 5

    # Рендер
    tiles_group.draw(screen)
    player_group.draw(screen)
    for enemy in enemy_group:
        enemy.move()
    player.update()
    enemy_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
