import sys
import pygame

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры'''

    def __init__(self):
        '''Инициализирует игру и создает игровые ресурсы'''
        # pygame.init() - эта строчка есть в книге, но не влияет на запуск кода
                
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption('Alien Invasion')

        # назначение цвета фона
        self.bg_color = (230, 20, 230)

    def run_game(self):
        '''Запуск основного цикла игры'''
        while True:
            # Отслеживает события клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # При каждом проходе цикла перерисовывается цвет экрана
            self.screen.fill(self.bg_color)        
                
            # Отображение последнего прорисованного экрана
            pygame.display.flip()

if __name__ == '__main__':
    # Создание эксемпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()