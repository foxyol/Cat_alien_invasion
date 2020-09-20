import pygame
pygame.init()

class Button:
    def __init__(self, ai_game, msg):
        ''' Инициализирует атрибуты кнопки ''' 
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Назначение размеров и свойств кнопки
        self.width, self.height = 300, 150
        self.button_color = (182, 170, 159)
        self.text_color = (77, 53, 29)
        self.font = pygame.font.SysFont(None, 72)

        # Построение объекта rect кнопки и выравние по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Сообщение кнопки создается только 1 раз
        self._prer_msg(msg)

    def _prer_msg(self, msg):
        ''' Преобразует msg в прямоугольник и выравнивает текст по центру '''
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_buton(self):
        # Отображение пустой кнопки и вывод сообщения
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)