class Settings():
    '''Класс для хранения всех настроек Alien_invasion'''

    def __init__(self):
        '''Инициализирует настройки игры'''
        # Параетры экрана
        self.screen_width = 1550
        self.screen_height = 800
        self.bg_color = (153, 217, 234)
        self.bullet_allowed = 100

        # Настройки корабля
        self.ship_limit = 2

        # Настройки пришельцев
        self.fleet_drop_speed = 9
        self.fleet_direction = 1 # 1 - движение вправо, -1 - влево

        # Темп ускорения игры
        self.speed_scale = 1.2
        self.initialize_dynamic_settings()

        # Темп роста скорости пришельца
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        ''' Инициализирует настройки, изменяющиеся в ходе игры '''
        self.ship_speed = 2.5
        self.bullet_speed = 3.0
        self.alien_speed = 2.0
        self.alien_points = 10

        # left -1, right 1
        self.fleet_direction = 1

    def increase_speed(self):
        ''' Увеичивает настройки скорости и стоимость пришельцев'''
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
