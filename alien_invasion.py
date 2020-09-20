import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры'''

    def __init__(self):
        '''Инициализирует игру и создает игровые ресурсы'''
        # pygame.init() - эта строчка есть в книге, но не влияет на запуск кода
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion. Meow')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Запуск основного цикла игры'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _check_events(self):
        # Отслеживает события клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        ''' Запускает новую игру по нажатию кнопки Play '''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровой статистики и настроек
            self.stats.reset_stats()
            self.stats.game_active = True
            self.settings.initialize_dynamic_settings()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списка пришельцев и снарядов
            self.aliens.empty()
            self.bullet.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)
   
    def _check_keydown_events(self, event):
        '''Реагирует на нажатие клавиш '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # elif event.key == pygame.K_Q:
        #     sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''Реагирует на отпускание клавиш '''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''Создание нового снаряда и вкл. его в группу bullets'''
        if len(self.bullet) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)

    def _update_bullets(self):
        '''Обновляет позиции снарядов и уничтожает старые снаряды'''
        # Обновляет позиции снарядов
        self.bullet.update()

        # Удаление снарядов, вышедших за экран
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        ''' Обработка коллизий снарядов с пришельцами '''    
        if not self.aliens:
            # Уничтожение текужих сарядов и создание нового флота
            self.bullet.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            
        # проверка попадания в пришельцев
        # При обнаружени попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullet, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points * len(alien)
            self.sb.prep_score()
            #self.sb.check_high_score()

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        

    def _create_fleet(self):
        ''' Создать флот'''
        # Создание пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        avalibale_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avalibale_space_x // (2 * alien_width)
        self.aliens.add(alien)

        # определяет количество рядов, помещ. на экране
        ship_height = self.ship.rect.height
        available_spase_y = (self.settings.screen_height - (2 * alien_height) - ship_height)
        number_rows = available_spase_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _update_aliens(self):
        ''' обнвляет позицию всех пришельцев во флоте '''
        self.aliens.update()
        self._check_fleet_edges()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        '''Реагирует на достижение пришельцем края экрана '''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        ''' Опускает весь флот и меняет направление флота'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        ''' Обрабатывает столкновение корабля с пришельцом '''
        # Уменьшает ship_left
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # Очистка пришельцев и снарядов
            self.aliens.empty()
            self.bullet.empty()

            # Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(1.1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        ''' Проверяет, добрались ли пришельцы до края экрана '''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        # При каждом проходе цикла перерисовывается цвет экрана
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen) 

        # Выводит информацию о счёте
        self.sb.show_score()

        #Кнопка Play отображается только если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_buton()
            
        # Отображение последнего прорисованного экрана
        pygame.display.flip()

if __name__ == '__main__':
    # Создание эксемпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()