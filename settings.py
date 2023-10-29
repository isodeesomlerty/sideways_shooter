class Settings:
    """A class to store all settings for Sideways Shooter."""

    def __init__(self):
        """Initilize the game's settings."""
        # Screen settings
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5
        self.ship_limit = 2

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_lurch_speed = 10
        # fleet_direction of 1 represents down; -1 represents up.
        self.fleet_direction = 1