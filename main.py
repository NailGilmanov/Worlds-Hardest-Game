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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, start_screen=True):
        super().__init__(all_sprites)
        if start_screen:
            animated_group_start_screen.add(self)
        else:
            animated_group_finish_screen.add(self)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.count = 0
        self.start_screen = start_screen

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        k = 0
        for j in range(rows):
            for i in range(columns):
                k += 1
                if k == 10:
                    break
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.start_screen:
            self.count += 1
            if self.count == 5:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.count = 0
        else:
            self.count += 1
            if self.count == 5:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]
                self.count = 0


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
        string_rendered = font.render(line, 1, pygame.Color(120, 120, 240))
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
        animated_group_start_screen.update()
        fon = pygame.transform.scale(load_image('background.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(120, 120, 240))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        animated_group_start_screen.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def finish_screen():
    intro_text = ["Вы прошли Самую Сложную Игру в Мире!", "",
                  f"Итоговое количество смертей: {death_count}"]
    animated_group_start_screen.update()
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(120, 120, 240))
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
        animated_group_finish_screen.update()
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 50)
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(120, 120, 240))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 20
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        animated_group_finish_screen.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def render_display(death_count, lvl):
    font = pygame.font.SysFont('didot.ttc', 40)
    death_img = font.render(f'DEATHS: {death_count}', True, (0, 0, 120))
    level_img = font.render(f'LEVEL: {lvl}/5', True, (0, 0, 120))
    screen.blit(death_img, (1400, 20))
    screen.blit(level_img, (720, 20))


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
    filename = "levels/" + filename
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
key_image1 = load_image('key2.jpg')  # ключ с белым фоном
key_image2 = load_image('key1.jpg')  # ключ с фиолетовым фоном

tile_width = tile_height = 67
hero_width = hero_height = 67
enemy_padding = 19.5

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
border_group = pygame.sprite.Group()
final_zone_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
animated_group_start_screen = pygame.sprite.Group()
animated_group_finish_screen = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        if tile_type == 'green_f':
            self.add(final_zone_group)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(enemy_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            hero_width * pos_x + enemy_padding, hero_height * pos_y + enemy_padding)


class VerticalEnemy(Enemy):
    def __init__(self, pos_x, pos_y, top=None):
        super().__init__(pos_x, pos_y)
        self.top = top

    def move(self):
        if self.top:
            self.rect.y += 10
            if pygame.sprite.spritecollideany(self, border_group):
                self.rect.y += self.rect.y - pygame.sprite.spritecollideany(self, border_group).rect.y
                self.top = not self.top
        else:
            self.rect.y -= 10
            if pygame.sprite.spritecollideany(self, border_group):
                self.rect.y += pygame.sprite.spritecollideany(self, border_group).rect.y + tile_width - self.rect.y
                self.top = not self.top


class HorizontalEnemy(Enemy):
    def __init__(self, pos_x, pos_y, right=None):
        super().__init__(pos_x, pos_y)
        self.right = right

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

    def update(self):
        global all_keys

        # смерть главного героя
        if pygame.sprite.spritecollideany(self, enemy_group):
            return 'death'

        if pygame.sprite.spritecollideany(self, border_group):
            player_can_move = False
        else:
            player_can_move = True

        # пересечение с зоной оканчания уровня
        if pygame.sprite.spritecollideany(self, final_zone_group):
            if not all_keys:
                player_can_move = False
                return player_can_move
            return 'new_level'

        # подбор ключа
        if pygame.sprite.spritecollide(self, key_group, dokill=True):
            if len(key_group) == 0:
                all_keys = True
            return 'key_was_taken'

        return player_can_move


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, white=True):
        self.x = pos_x
        self.y = pos_y
        super().__init__(key_group, all_sprites)
        if white:
            self.image = key_image1
        else:
            self.image = key_image2
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 10)


class Border(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        super().__init__(border_group, all_sprites)
        self.image = tile_images['fon']
        self.rect = self.image.get_rect().move(
            hero_width * pos_x, hero_height * pos_y)


key_x = None
key_y = None
key_list = []


def generate_level(level):
    global key_x, key_y
    new_player, x, y, new_enemy, border_block = None, None, None, None, None
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
                new_enemy = HorizontalEnemy(x, y, right=False)
            elif level[y][x] == 'R':
                Tile('purple', x, y)
                new_enemy = HorizontalEnemy(x, y, right=True)
            elif level[y][x] == 'T':
                Tile('purple', x, y)
                new_enemy = VerticalEnemy(x, y, top=True)
            elif level[y][x] == 'X':
                Tile('white', x, y)
                new_enemy = VerticalEnemy(x, y, top=True)
            elif level[y][x] == 'B':
                Tile('purple', x, y)
                new_enemy = VerticalEnemy(x, y, top=False)
            elif level[y][x] == 'Z':
                Tile('white', x, y)
                new_enemy = VerticalEnemy(x, y, top=False)
            elif level[y][x] == 'W':
                Tile('fon', x, y)
                border_block = Border(x, y)
            elif level[y][x] == 'F':
                Tile('green_f', x, y)
                border_block = Border(x, y)
            elif level[y][x] == 'K':
                Tile('purple', x, y)
                Key(x, y, white=False)
                key_x = x
                key_y = y
                key_list.append((key_x, key_y, False))
            elif level[y][x] == 'k':
                Tile('white', x, y)
                Key(x, y, white=True)
                key_x = x
                key_y = y
                key_list.append((key_x, key_y, True))

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, new_enemy, border_block


class NewLevel:
    def __init__(self, lvl):
        self.level = lvl

    def change_level(self):
        self.level += 1
        all_sprites.empty()
        tiles_group.empty()
        player_group.empty()
        enemy_group.empty()
        border_group.empty()
        final_zone_group.empty()
        key_group.empty()
        global player, level_x, level_y, enemy, border
        player, level_x, level_y, enemy, border = generate_level(load_level(f'level{self.level}.txt'))


new_level = NewLevel(1)

level = 1

player, level_x, level_y, enemy, border = generate_level(load_level('level1.txt'))

# анимированный спрайт на начальном экране
animated_hero = AnimatedSprite(load_image("animated_hero.png"), 5, 2, 541, 350, start_screen=True)

# анимированный спрайт на конечном экране
animated_boy = AnimatedSprite(load_image("animated_boy.png"), 4, 3, 900, 561, start_screen=False)


death_count = 0

all_keys = False

clock = pygame.time.Clock()

start_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Список нажатых клавиш
    keys = pygame.key.get_pressed()

    # подбор ключа
    if player.update() == 'key_was_taken':
        if len(key_group) == 0:
            all_keys = True

    # проверка перехода на новый уровень, если взяты все ключи
    if player.update() == 'new_level' and all_keys:
        level += 1
        if level == 6:
            finish_screen()
            running = False
        else:
            key_list = []
            new_level.change_level()

    # смерть главного героя
    if player.update() == 'death':
        all_keys = False
        hero_x = player.x
        hero_y = player.y
        player.kill()
        death_count += 1
        player = Player(hero_x, hero_y)
        # проверяем есть на уровне ключи
        if new_level.level == 1 or new_level.level == 4 or new_level.level == 5:
            if key_list:
                key_group.empty()
                for x, y, white in key_list:
                    if white:
                        Key(x, y)
                    else:
                        Key(x, y, white=False)
        else:
            all_keys = True

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
    key_group.draw(screen)
    for enemy in enemy_group:
        enemy.move()
    player.update()
    enemy_group.draw(screen)
    render_display(death_count, level)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
