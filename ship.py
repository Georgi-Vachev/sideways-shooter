import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ss_game):
        
        super().__init__()
        # Screen
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()

        # Settings
        self.settings = ss_game.settings
        
        # Image
        self.image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.scale(self.image,(75,75))
        self.rect = self.image.get_rect()

        # Spawn Position
        self.rect.midleft = self.screen_rect.midleft

        # Decimal value of rect.x
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)