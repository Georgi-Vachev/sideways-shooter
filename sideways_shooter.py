import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard 


class SidewaysShooter:

    def __init__(self):
        
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Sideways Shooter")
        self.screen_rect = self.screen.get_rect()

        # Instances
        self.settings = Settings()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.play_button = Button(self, 'Play')

    def run_game(self):

        while True:
            self._check_events()
            self._update_screen()
            

            if self.stats.game_active:
                self._update_bullets()
                self._update_aliens()
                self.ship.update()

    def _check_events(self):
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

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):

        self.stats.reset_stats()
        self.settings.initialize_dynamic_settings()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_s:
            self.ship.moving_down = False
        elif event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False

    def _create_fleet(self):
        alien = Alien(self)
        alien.width, alien.height = alien.rect.size
        available_space_y = self.settings.screen_height - 2 * alien.height
        number_aliens_y = available_space_y // (2 * alien.height)
        number_columns = 8
        for column in range(number_columns):
            for alien_num in range(number_aliens_y):
                self._create_alien(alien_num, column)

    def _create_alien(self, alien_num, column):
        alien = Alien(self)
        if column % 2 == 0:
            alien.fleet_direction *= -1
        alien.col_number = column
        alien.width, alien.height = alien.rect.size
        alien.y = 30 + alien.height + 2 * alien.height * alien_num
        alien.rect.y = alien.y
        alien.rect.x -= 20 + alien.height + 2 * alien.width * column
        self.aliens.add(alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                column = alien.col_number
                self._change_fleet_direction(column)
                

    def _change_fleet_direction(self, column):
        for alien in self.aliens.sprites():
            if alien.col_number == column:
                alien.fleet_direction *= -1

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.ship.center_ship()
            self.sb.prep_ships()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            
    def _update_bullets(self):

        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen_rect.right:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)      
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:

            self.bullets.empty()
            self._create_fleet()
            self.settings.speed_increase()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):

        if self.stats.game_active:
            self.screen.fill(self.settings.bg_color)
            self.sb.show_score()
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            
        else:
            self.play_button.draw_button()
        
        pygame.display.flip()
    
if __name__ == "__main__":

    new_game = SidewaysShooter()
    new_game.run_game()