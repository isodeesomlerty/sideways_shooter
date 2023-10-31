class Settings:
    """A class to store all settings for Sideways Shooter."""

    def __init__(self):
        """Initilize the game's settings."""
        # Screen settings
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 2

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_lurch_speed = 10

        # Top margin setting reserved for the scoreboard
        self.top_margin = 75

        # How quickly the game speeds up
        self.speedup_scale = 1.5
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Initialize dynamic settings upon the game starting.
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 10.0

        # fleet_direction of 1 represents down; -1 represents up.
        self.fleet_direction = 1

        # Scoring settings.
        self.alien_points = 50


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)