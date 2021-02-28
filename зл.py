import pygame, sys, os


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if WIDTH <= obj.rect.x:
            obj.rect.x = 50
        if obj.rect.x <= 0:
            obj.rect.x = WIDTH - 50
        if HEIGHT <= obj.rect.y:
            obj.rect.y = 50
        if obj.rect.y <= 0:
            obj.rect.y = HEIGHT - 50

    # позиционировать камеру на объекте target
    def update(self, target):
        width = WIDTH
        height = HEIGHT
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, wall_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, *args, **kwargs):
        global flag1, flag2, flag3, flag4, flag_over_game
        if flag1:
            self.rect = self.rect.move(0, 50)
        elif flag2:
            self.rect = self.rect.move(0, -50)
        elif flag3:
            self.rect = self.rect.move(50, 0)
        elif flag4:
            self.rect = self.rect.move(-50, 0)
        if pygame.sprite.spritecollideany(self, wall_group):
            if flag1:
                self.rect = self.rect.move(0, -50)
            elif flag2:
                self.rect = self.rect.move(0, 50)
            elif flag3:
                self.rect = self.rect.move(-50, 0)
            elif flag4:
                self.rect = self.rect.move(50, 0)
        flag1, flag2, flag3, flag4 = False, False, False, False


FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
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
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    # читаем уров4нь, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_skreen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_render = font.render(line, 1, pygame.Color(0, 0, 0))
        intro_rect = string_render.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_render, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)


def over_game():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


if __name__ == '__main__':
    player = None
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()

    pygame.init()
    pygame.display.set_caption('Игра')
    size = WIDTH, HEIGHT = 550, 550
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mar.png')

    tile_width = tile_height = 50

    print('введите имя файла с картой или 0 если по уполчанию')
    a = input()
    if a == '0':
        a = 'map.txt'
    filename = 'data/' + a
    if not os.path.isfile(filename):
        print(f"Файл с изображением '{filename}' не найден")
        sys.exit()
    else:
        start_skreen()
        player, level_x, level_y = generate_level(load_level(a))
        flag1, flag2, flag3, flag4 = False, False, False, False
        flag_over_game = False
        camera = Camera()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        flag2 = True
                    if event.key == pygame.K_DOWN:
                        flag1 = True
                    if event.key == pygame.K_RIGHT:
                        flag3 = True
                    if event.key == pygame.K_LEFT:
                        flag4 = True
                    player_group.update()
            screen.fill((0, 0, 0))
            camera.update(player);
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
            all_sprites.draw(screen)
            player_group.draw(screen)
            pygame.display.flip()
            if flag_over_game:
                over_game()
        pygame.quit()
