import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ss_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('chapter_12/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien near the top right of the screen.
        self.rect.x = self.settings.screen_width - self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact vertical position.
        self.y = float(self.rect.y)

    
    def check_edges(self):
        """Return True if alien is at edge of screen."""
        return ((self.rect.top <= 0) or 
                (self.rect.bottom >= self.settings.screen_height))
    

    def update(self):
        """Move the alien up or down."""
        self.y += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.y = self.y
    


