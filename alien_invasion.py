import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры'''

    def __init__(self):
        '''Инициализирует игру и создает игровые ресурсы'''
        # pygame.init() - эта строчка есть в книге, но не влияет на запуск кода
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion. Meow')
        
        self.ship = Ship(self)

    def run_game(self):
        '''Запуск основного цикла игры'''
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()

    def _check_events(self):
        # Отслеживает события клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.type == pygame.KEYUP:
                    self.ship.moving_right = False

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается цвет экрана
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()     

        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    # Создание эксемпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
