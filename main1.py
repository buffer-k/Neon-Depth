# Переписанный код из уроков про лабиринт


import sys
import pygame
import pytmx

SIZE = WIDTH, HEIGHT = 672, 608
FPS = 15
LEVELS_DIR = 'levels'
TILE_SIZE = 32


class NeonDepth:

    def __init__(self, filename, free_tiles, finish_tile):
        self.map = pytmx.load_pygame(f'{LEVELS_DIR}/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tile_size = self.map.tilewidth
        self.free_tiles = free_tiles
        self.finish_tile = finish_tile

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                image = self.map.get_tile_image(x, y, 0)
                screen.blit(image, (x * self.tile_size, y * self.tile_size))

    def get_tile_id(self, position):
        return self.map.tiledgidmap[self.map.get_tile_gid(*position, 0)]

    def is_free(self, position):
        return self.get_tile_id(position) in self.free_tiles


class Hero:

    def __init__(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 255), center, TILE_SIZE // 2)


class Game:

    def __init__(self, game, hero):
        self.game = game
        self.hero = hero

    def render(self, screen):
        self.game.render(screen)
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        if self.game.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)

    game = NeonDepth('map.tmx', [3, 13, 15], 15)
    hero = Hero((10, 10))
    mover = Game(game, hero)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                terminate()
        mover.update_hero()
        screen.fill((0, 0, 0))
        mover.render(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


if __name__ == '__main__':
    main()
