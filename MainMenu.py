import pygame
import Main
from Main import main as main_func
import pygame_gui

def main():

    pygame.init()


    screen = pygame.display.set_mode(Main.size)
    manager = pygame_gui.UIManager(Main.size)
    play = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 200), (250, 50)),
        text='Играть',
        manager=manager
    )

    settings = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((440, 500), (250, 50)),
        text='Управление',
        manager=manager
    )

    clock = pygame.time.Clock()
    running = True
    bg = pygame.image.load('data/title.png')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play:
                        main_func()
                    elif event.ui_element == settings:
                        pass
                        #TODO: okno nastroek
            manager.process_events(event)
            screen.fill(pygame.Color(31, 31, 31))
            screen.blit(bg, (250, -100))
            manager.update(clock.tick(60))
            manager.draw_ui(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
