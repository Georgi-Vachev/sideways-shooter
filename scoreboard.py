import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:

    def __init__(self, ss_game):

        self.ss_game = ss_game
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        self.stats = ss_game.stats

        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_high_score()
        self.prep_score()
        self.prep_ships()
        self.prep_level()
        
    def prep_score(self):

        rounded_score = round(self.stats.score, -1)
        score_str = "Score: " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                        self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = self.high_score_rect.bottom + 5
        self.score_rect.left = self.high_score_rect.left
        

    def show_score(self):

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):

        high_score = round(self.stats.high_score, -1)
        high_score_str = "Record: " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 5
        self.high_score_rect.top = self.screen_rect.top + 5

    def prep_level(self):

        level_str = str(f"Level: {self.stats.level}")
        self.level_image = self.font.render(level_str, True,
                        self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.y =( self.settings.screen_height -
                self.level_rect.height - 70)
        self.level_rect.x = 15
        
    def prep_ships(self):

        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ss_game)
            ship.image = pygame.transform.scale(ship.image, (50, 50))
            ship.rect.x = 5 + ship_number * (ship.rect.width - 25)
            ship.rect.y = self.settings.screen_height - ship.rect.height + 15
            self.ships.add(ship)

    def check_high_score(self):

        if self.stats.score > self.stats.high_score:
            with open('highest_score.txt', 'w') as f:
                f.write(str(self.stats.score))
            self.stats.high_score = self.stats.score
        self.prep_high_score()