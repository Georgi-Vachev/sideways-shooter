class Settings:

    def __init__(self):
        
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = ((52, 94, 235))

        self.ship_limit = 3

        self.bullet_width = 15
        self.bullet_height = 300

        self.bullet_color = (235, 223, 52)
        self.bullets_allowed = 10

        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        
        self.ship_speed = 1.5
        self.alien_speed = 1.0
        self.bullet_speed = 3.0
        self.alien_points = 50

    def speed_increase(self):

        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.speedup_scale)

