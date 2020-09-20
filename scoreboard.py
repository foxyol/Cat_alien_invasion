import pygame
from pygame.sprite import Group
from ship import Ship
pygame.init()


class Scoreboard():
    ''' Класс для вывода игровой информации '''

    def __init__(self, ai_game):
        ''' Инициализирует атрибуты подсчета очков '''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счёта
        self.text_color = (77, 53, 29)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения
        self.prep_score()
        # self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        ''' Перобразует текущий счёт в графическое изображение '''
        rounded_score = round(self.stats.score, -1)
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True, 
                self.text_color, self.settings.bg_color)

        # Вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = 30

    # def prep_high_score(self):
    #     ''' Перобразует рекордный счёт в графическое изображение '''
    #     high_score = round(self.stats.high_score, -1)
    #     high_score_str = '{:,}'.format(high_score)
    #     self.high_score_image = self.font.render(high_score_str, True, 
    #             self.text_color, self.settings.bg_color)

    #     # Вывод счета по центру
    #     self.high_score_rect = self.high_score_image.get_rect()
    #     self.high_score_rect.centerx = self.screen_rect.centerx
    #     self.score_rect.top = 30

    def show_score(self):
        ''' Выводит счёт и уровень на экран '''
        self.screen.blit(self.score_image, self.score_rect)
        # self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.ships.draw(self.ships, self.screen)

    # def check_high_score(self):
    #     ''' Проверяет, появился ли новый рекорд '''
    #     if self.stats.score > self.stats.high_score:
    #         self.stats.high_score = self.stats.score
    #         self.prep_high_score()

    def prep_level(self):
        ''' Преобразует новый уровеь в графическое изображение '''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, 
                self.text_color, self.settings.bg_color)

        # Уровень выводится под текущим счётом
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 15

    def prep_ships(self):
        ''' Сообщает о кол-ве оставшихся кораблей '''
        self.ships = Group
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 15
            self.ships.add(ship)