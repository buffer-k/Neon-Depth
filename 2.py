import pygame
import sys
import os


pygame.init()
size = width, height = 1152, 648
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
i = 0
can_run_left = True
can_run_right = True
MOVE_SPEED = 7


all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()
all_dots = pygame.sprite.Group()
for_pl = pygame.sprite.Group()


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


class Check_side_collision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_dots)
        self.rect = pygame.Rect(0, 0, 38, 50)

    def update(self):
        global moving, can_run_left, can_run_right
        self.rect.x = player.x + 11
        self.rect.y = player.y + 1
        if pygame.sprite.spritecollideany(self, boxes):
            if moving == -5:
                can_run_left = False
            if moving == 5:
                can_run_right = False
        else:
            can_run_right = True
            can_run_left = True


class Check_bottom_collision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_dots)
        self.rect = pygame.Rect(0, 0, 35, 1)

    def update(self):
        global moving, can_run_left, can_run_right
        self.rect.x = player.x + 20
        self.rect.y = player.y + 67
        if player.jumped:
            player.rect.y -= player.coef
            player.y -= player.coef
            player.coef -= 1
            if player.coef == -1:
                player.coef = 0
            self.rect.x = player.x + 2
            self.rect.y = player.y + 67
        if not pygame.sprite.spritecollideany(self, boxes):
            player.y += 8
            player.rect.y += 8
        elif can_run_left and can_run_right:
            player.is_ground = True
            player.jumped = False


class Check_top_collision(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_dots)
        self.rect = pygame.Rect(0, 0, 35, 2)

    def update(self):
        global moving, can_run_left, can_run_right
        self.rect.x = player.x + 12
        self.rect.y = player.y
        if pygame.sprite.spritecollideany(self, boxes):
            player.jumped = False
            print(16)




class Fon(pygame.sprite.Sprite):
    image = [load_image('fon.jpg')]

    def __init__(self, x, y, type):
        super().__init__(all_sprites)
        self.image = Fon.image[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box(pygame.sprite.Sprite):
    image = [load_image('IndustrialTile_57.png'), load_image('Locker4.jpg')]

    def __init__(self, x, y, type):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = Box.image[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        self.is_ground = False
        self.jumped = False
        self.x = 0
        self.xvel = 0
        self.yvel = 0
        self.y = 0
        super().__init__(all_sprites)
        self.frames = []
        self.add(for_pl)
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.x, self.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, left, right):
        self.rect.w = 38
        if pygame.sprite.spritecollideany(self, boxes):
            pass
        global i
        if i == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            i = 0
        else:
            i += 1
        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.x += self.xvel  # переносим свои положение на xvel

    def jump(self):
        if self.is_ground and moving:
            self.coef = 19
            self.jumped = True
            self.is_ground = False


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
                Box(48 * x, 24 + 48 * y, 0)
            if level[y][x] == '#':
                Fon(48 * x, 24 + 48 * y, 0)
            if level[y][x] == 'L':
                Box(48 * x,  48 * y, 1)


def main():
    global i
    global moving
    bg = pygame.image.load("data/Background.png")
    global player
    player = Player(load_image('stay.png'), 4, 1, 200, 200)
    generate_level(load_level('lvl1.txt'))
    running = True
    # fon = Fon()
    left = right = False
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
                    player.jump()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving = False
                    player.frames = []
                    player.cut_sheet(load_image("stay.png"), 4, 1)
                elif event.key == pygame.K_LEFT:
                    moving = False
                    player.frames = []
                    player.cut_sheet(load_image("stay1.png"), 4, 1)
            # elif event.type == pygame.MOUSEBUTTONDOWN:

        if moving:
            if moving == -5 and can_run_left:
                player.x += moving
                player.rect.x += moving
            if moving == 5 and can_run_right:
                player.x += moving
                player.rect.x += moving
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update(left, right)
        all_dots.update()
        for_pl.draw(screen)
        boxes.draw(screen)
        player.update(left, right)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()