import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, ss_game):

        # Screen, settings, color
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect and position it
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midright = ss_game.ship.rect.midright

        # Decimal s value
        self.x = float(self.rect.x)

    def update(self):

        self.x += self.settings.bullet_speed

        self.rect.x = self.x

    def draw_bullet(self):

        pygame.draw.rect(self.screen, self.color, self.rect)

