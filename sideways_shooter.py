import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

from random import randint

class SidewaysShooter:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
        self.settings.screen_width = self.screen_rect.width
        self.settings.screen_height = self.screen_rect.height
        pygame.display.set_caption("Sideways Shooter")

        # Create a scoreboard and an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Sideways Shooter in an inactive state
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.game_active:
                    self._check_play_button(mouse_pos)


    def _quit_game(self):
        """Exit the game."""
        self.stats.write_high_score()
        sys.exit()


    def _check_play_button(self, mouse_pos):
        """Check whether the player clicks on the Play button."""
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_button_clicked:
            self._start_game()


    def _start_game(self):
        """Start a new game if the game is currently inactive."""
        if not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_images()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    
    def _fire_bullet(self):
        """Create a new bullet and add it the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self._new_level()


    def _new_level(self):
        """Start a new level."""
        self.stats.level += 1
        self.sb.prep_level()


    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the left of the screen.
        self._check_aliens_left()
        

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x = self.settings.screen_width - 2 * alien_width
        current_y = self.settings.top_margin
        while current_x > (2 * alien_width):
            while current_y < (self.settings.screen_height - 2 * alien_height):
                self._create_alien(current_x, current_y,
                                   [0, 100], [50, 50])
                current_y += 2 * alien_height
            
            # Finished a column; subtract x value, and reset y value.
            current_x -= 2 * alien_width
            current_y = self.settings.top_margin
    

    def _create_alien(self, x_position, y_position,
                      x_range=[0,0], y_range=[0,0]):
        """
        Create an alien and place it in the column.
        Adjust the alien's position by a random amount
         within x_range and y_range.
        """
        if len(x_range) == 2:
            random_x = randint(x_range[0], x_range[1])
        
        if len(y_range) == 2:
            random_y = randint(y_range[0], y_range[1])

        new_alien = Alien(self)
        new_alien.y = y_position
        new_alien.rect.x = x_position + random_x

        if self._check_spawn_point(y_position, random_y, new_alien.rect.height):
            new_alien.rect.y = y_position + random_y
        else:
            return
        
        self.aliens.add(new_alien)

    
    def _check_spawn_point(self, y_position, random_y, alien_height, 
                           safety_margin_top=50,
                           safety_margin_bottom=50):
        """Check if the spawn point is too close to the top or bottom."""
        if ((y_position + random_y <= 
             self.settings.top_margin + safety_margin_top) 
            or
            (y_position + random_y + alien_height >= 
             self.settings.screen_height - safety_margin_bottom)):
            return False
        else:
            return True


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):
        """Move the entire fleet forward and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_lurch_speed
        self.settings.fleet_direction *= -1

    
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(1)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_left(self):
        """Check if any aliens have reached the left of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.left <= 0:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


    def _update_screen(self):
        """Update images on the screen, and flip to t he new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the Play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ss = SidewaysShooter()
    ss.run_game()