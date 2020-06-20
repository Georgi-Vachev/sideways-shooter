import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class that manages individual aliens."""

    def __init__(self, ss_game):
        """Initializes screen,image, rect for the alien class."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (75,60))
        self.rect = self.image.get_rect()

        self.rect.x = ss_game.settings.screen_width - self.rect.width
        

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.col_number = 0
        self.fleet_direction = -1

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True

    def update(self):
        self.y += self.settings.alien_speed * self.fleet_direction
        self.rect.y = self.y
