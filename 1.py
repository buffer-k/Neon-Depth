import pygame
import sys
import os


pygame.init()
size = width, height = 1152, 648
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
i = 0
MOVE_SPEED = 4
JUMP_POWER = 10
GRAVITY_FORCE = 0.55
PLAYER_WIDTH = 18
PLAYER_HEIGHT = 35


all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()


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


class Fon(pygame.sprite.Sprite):
    image = load_image('Background.png')

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Fon.image
        self.rect = self.image.get_rect()


class Box(pygame.sprite.Sprite):
    image = load_image('IndustrialTile_57.png')

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = Box.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        self.jumped = False
        self.xvel = 0
        self.yvel = 0
        self.isGround = False
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x, y, 0, 0)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, left, right, up):

        if right:
            self.xvel = MOVE_SPEED
        if left:
            self.xvel = -MOVE_SPEED
        if not (left or right):
            self.xvel = 0
        if up:
            if self.isGround:
                self.yvel = -JUMP_POWER
        if not self.isGround:
            self.yvel += GRAVITY_FORCE

        self.rect.x += self.xvel
        # self.x += self.xvel
        self.collide(self.xvel, 0, boxes)

        self.isGround = False
        self.rect.y += self.yvel
        # self.y += self.yvel
        self.collide(0, self.yvel, boxes)
        global i
        if i == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            i = 0
        else:
            i += 1

    def jump(self):
        if self.is_ground and moving:
            self.coef = 18
            self.jumped = True
            self.is_ground = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def collide(self, xvel, yvel, boxes):
        for box in boxes:
            if pygame.sprite.collide_rect(self, box):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = box.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = box.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = box.rect.top  # то не падает вниз
                    self.isGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = box.rect.bottom  # то не движется вверх
                    self.yvel = 0


moving = False


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Box(48 * x, 24 + 48 * y)


def main():
    global i
    global moving
    bg = pygame.image.load("data/Background.png")
    player = Player(load_image('stay.png'), 4, 1, 200, 200)
    generate_level(load_level('lvl1.txt'))
    running = True
    left = right = up = False
    # fon = Fon()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                    player.frames = []
                    i = 10
                    player.cut_sheet(load_image("run.png"), 6, 1)
                elif event.key == pygame.K_LEFT:
                    left = True
                    player.frames = []
                    i = 10
                    player.cut_sheet(load_image("run1.png"), 6, 1)
                elif event.key == pygame.K_UP:
                    up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                    moving = False
                    player.frames = []
                    player.cut_sheet(load_image("stay.png"), 4, 1)
                elif event.key == pygame.K_LEFT:
                    left = False
                    moving = False
                    player.frames = []
                    player.cut_sheet(load_image("stay1.png"), 4, 1)
                elif event.key == pygame.K_UP:
                    up = False
            # elif event.type == pygame.MOUSEBUTTONDOWN:

        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update(left, right, up)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()