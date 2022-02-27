import pygame
import sys
import os
import time


size = width, height = 1152, 648
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
i = 0
MOVE_SPEED = 4
JUMP_POWER = 10
GRAVITY_FORCE = 0.55
PLAYER_WIDTH = 48
PLAYER_HEIGHT = 72
FOR_I = 10
ATTACK_SPEED = 10
FIREBALL_MOVE_SPEED = 2
ENEMY_SPEED = 2
PROBEG = 0.55
DAMAGE = 10
DEAD = False


all_sprites = pygame.sprite.Group()
boxes = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullets = pygame.sprite.Group()
attack = False
player_group = pygame.sprite.Group()


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


class FonBoxes(pygame.sprite.Sprite):
    image = [load_image('IndustrialTile_03.png')]

    def __init__(self, x, y, type):
        super().__init__(all_sprites)
        self.image = FonBoxes.image[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box(pygame.sprite.Sprite):
    image = [load_image('IndustrialTile_57.png'), load_image('chest.png')]

    def __init__(self, x, y, type):
        super().__init__(all_sprites)
        self.add(boxes)
        self.image = Box.image[type]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y


class FireBall(pygame.sprite.Sprite):
    image = load_image('fireball.png')

    def __init__(self, x, y, type):
        # type - 1, если вправо; 2, если влевоd
        super().__init__(all_sprites)
        self.rect = self.image.get_rect()
        self.add(bullets)
        self.rect.x = x + PLAYER_WIDTH
        self.rect.y = y + PLAYER_HEIGHT / 2
        self.type = type

    def update(self):
        self.rect.x += self.type * FIREBALL_MOVE_SPEED
        if self.rect.x > 1200 or self.rect.x < -30:
                self.kill()
        print(self.rect.x)

# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, player):
#         super().__init__(all_sprites)
#         self.add(bullets)
#         self.image = load_image('bullet.png')
#         self.rect = self.image.get_rect()
#         self.xvel = 0
#         if player.xvel > 0:
#             self.rect.x = player.rect.x + 10
#             self.xvel = 3
#         if player.xvel < 0:
#             self.rect.x = player.rect.x - 10
#             self.xvel = -3
#             self.image = pygame.transform.flip(self.image, True, False)
#         self.rect.y = player.rect.y + 40
#         self.player = player
#
#     def update(self, enemies):
#         # print(self.rect.x, self.player.xvel)
#         self.rect.x += self.xvel
#         if self.rect.x > 1200 or self.rect.x < -30:
#             self.kill()
#
#         if pygame.sprite.spritecollideany(self, enemy_group):
#             # print(self.rect.x)
#             self.kill()
#             # for enemy in enemies:
#             #     print(enemy.rect.x)
#             #     if pygame.sprite.spritecollideany(enemy, bullets):
#             #         print(enemy.rect.x)
#             #         enemy.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(enemy_group)
        self.rect = pygame.Rect(x, y, 0, 0)
        self.frames = []
        self.cut_sheet(load_image('enemy_run.png'), 6, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 0
        self.right = True
        self.left = False
        self.isGround = False
        self.xvel = 0
        self.yvel = 0
        self.hp = 20

    def cut_sheet(self, sheet, columns, rows):
        self.cur_frame = 0
        self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.rect.w = 50
        # if self.rect.y > 700:
        #     self.die()
        #

        if self.right:
            self.xvel = ENEMY_SPEED
        if self.left:
            self.xvel = -ENEMY_SPEED

        if not self.isGround:
            self.yvel += GRAVITY_FORCE

        self.rect.x += self.xvel

        self.collide(self.xvel, 0, boxes)

        self.isGround = False
        self.rect.y += self.yvel

        self.collide(0, self.yvel, boxes)

        if self.hp <= 0:
            self.kill()

        if self.i == 10:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.i = 0
        else:
            self.i += 1

    def collide(self, xvel, yvel, boxes):
        for box in boxes:
            if pygame.sprite.collide_rect(self, box):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = box.rect.left  # то не движется вправо
                    self.frames = []
                    self.cut_sheet(load_image('enemy_run1.png'), 6, 1)
                    self.right = False
                    self.left = True

                if xvel < 0:  # если движется влево
                    self.rect.left = box.rect.right  # то не движется влево
                    self.frames = []
                    self.cut_sheet(load_image('enemy_run.png'), 6, 1)
                    self.rect.x -= 1
                    self.right = True
                    self.left = False

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = box.rect.top  # то не падает вниз
                    self.isGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = box.rect.bottom  # то не движется вверх
                    self.yvel = 0
        for bullet in bullets:
            if pygame.sprite.collide_rect(self, bullet):
                bullet.kill()
                self.hit()

    def hit(self):
        if self.xvel > 0:
            self.image = pygame.image.load('data/enemy_hit.png')
        else:
            self.image = pygame.image.load('data/enemy_hit1.png')
        self.hp -= DAMAGE


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        self.xvel = 0
        self.yvel = 0
        self.isGround = False
        self.isAttack = False
        super().__init__(player_group)
        self.rect = pygame.Rect(x, y, 0, 0)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.start_x = x
        self.start_y = y
        self.poryadok = 1
        self.xvel_for_hit = 0
        self.hp = 20

    def cut_sheet(self, sheet, columns, rows):
        self.isAttack = False
        self.cur_frame = 0
        self.poryadok = 1
        self.rect = pygame.Rect(self.rect.x, self.rect.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, left, right, up):
        global attack, i
        self.rect.w = PLAYER_WIDTH
        if self.rect.y > 700:
            self.die()

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

        if self.xvel_for_hit > 0:
            self.rect.x -= self.xvel_for_hit
            self.xvel_for_hit -= PROBEG

        self.rect.x += self.xvel
        # self.x += self.xvel
        self.collide(self.xvel, 0, boxes)

        self.isGround = False
        self.rect.y += self.yvel
        # self.y += self.yvel
        self.collide(0, self.yvel, boxes)

        if self.hp <= 0:
            self.die()

        if self.isAttack:
            if self.cur_frame == 6 and i == 0:
                bul = FireBall(self.rect.x, self.rect.y, 1)

        if self.rect.x > width:
            from MainMenu import main as main_menu
                main_menu()

        if i == FOR_I:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            i = 0
        else:
            i += 1

        print(self.cur_frame)
    def attack(self):
        self.isAttack = True

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def die(self):
        global GRAVITY_FORCE, FOR_I, i, DEAD
        # time.sleep(2)
        # self.teleport(self.start_x, self.start_y)
        for something in all_sprites:
            something.kill()
        GRAVITY_FORCE = 0
        self.yvel = 0
        self.xvel = 0
        self.frames = []
        i = 0
        self.hp = 10
        FOR_I = 60
        self.cut_sheet(load_image('death.png'), 6, 1)
        self.cur_frame = 0
        self.image = self.frames[0]
        DEAD = True


    def hit(self):
        self.yvel = -13
        self.image = pygame.image.load('data/Punk_hurt.png')
        self.hp -= 10

    def teleport(self, x, y):
        self.rect.x = x
        self.rect.y = y

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

        if pygame.sprite.spritecollideany(self, enemy_group):
            if not (self.yvel < -10):
                self.hit()
            print(self.rect.x, self.xvel)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
        max_width = max(map(len, level_map))
        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                Box(48 * x, 24 + 48 * y, 0)
            elif level[y][x] == 'f':
                FonBoxes(48 * x, 24 + 48 * y, 0)
            elif level[y][x] == 'c':
                Box(48 * x, 24 + 48 * y, 1)
            elif level[y][x] == 'e':
                Enemy(48 * x, 24 + 48 * y)


def main():
    pygame.init()
    global i
    global FOR_I
    global attack
    bg = pygame.image.load("data/Background.jpg")
    player = Player(load_image('stay.png'), 4, 1, 200, 400)
    generate_level(load_level('lvl1.txt'))
    running = True
    OPACITY = 255
    left = right = up = attack = False
    # fon = Fon()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not DEAD:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        player.throw()
                    if event.key == pygame.K_d:
                        if not left and not attack:
                            right = True
                            player.frames = []
                            i = 10
                            player.cut_sheet(load_image("run.png"), 6, 1)
                    elif event.key == pygame.K_a:
                        if not right and not attack:
                            left = True
                            player.frames = []
                            i = 10
                            player.cut_sheet(load_image("run1.png"), 6, 1)
                    elif event.key == pygame.K_w:
                        up = True
                    elif event.key == pygame.K_RIGHT:
                        if not (left or right):
                            player.frames = []
                            i = 0
                            player.cut_sheet(load_image("attack.png"), 8, 1)
                            FOR_I = ATTACK_SPEED
                            player.attack()
                            attack = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        right = False
                        if not left and not attack:
                            player.frames = []
                            i = 10
                            player.cut_sheet(load_image("stay.png"), 4, 1)
                    elif event.key == pygame.K_a:
                        left = False
                        if not right and not attack:
                            player.frames = []
                            i = 10
                            player.cut_sheet(load_image("stay1.png"), 4, 1)
                    elif event.key == pygame.K_w:
                        up = False
                    elif event.key == pygame.K_RIGHT:
                        if not (left or right):
                            player.frames = []
                            i = 10
                            player.cut_sheet(load_image("stay.png"), 4, 1)
                            FOR_I = 10
                            attack = False
            else:
                left = False
                right = False
        screen.blit(bg, (0, 0))
        # screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        player_group.update(left, right, up)
        player_group.draw(screen)
        clock.tick(60)
        pygame.display.flip()
        if DEAD:
            pygame.draw.rect(bg, (OPACITY, OPACITY, OPACITY, OPACITY), (0, 0, *size))
            if i >= 7:
                OPACITY -= 1
            if OPACITY < 0:
                pygame.quit()
                from MainMenu import main as main_menu
                main_menu()
    pygame.quit()


if __name__ == "__main__":
    main()
