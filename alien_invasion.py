import sys
from time import sleep
from random import randint

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from blue_star import Blue_Star
from asteroids import Asteroid


class AlienInvasion:
    """Class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        pygame.display.set_icon(pygame.image.load('images/icon.png'))
        pygame.display.set_caption("Alien Invasion")

        self.screen = pygame.display.set_mode((self.settings.screen_width,
           self.settings.screen_height))        

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.blue_star = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._populate_starfield()
        self._create_fleet()

        self.game_active = True


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self._create_asteroids()
                self._update_asteroids()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(self.settings.clock_tick)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True 
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=True
        elif event.key == pygame.K_LSHIFT:
            self.ship.boost=True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=False
        elif event.key == pygame.K_LSHIFT:
            self.ship.boost=False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        # Check for any bullets that have hit aliens.
        #   If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        if self.stats.ships_left > 0:

            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
        else:
            self.game_active = False

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _update_asteroids(self):
        self.asteroids.update()
        for asteroid in self.asteroids.copy():
            if asteroid.rect.top >= self.settings.screen_height:
                self.asteroids.remove(asteroid)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 10 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value and increment y value.
            current_x = alien_width
            current_y += 1.5 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _populate_starfield(self):
        star = Blue_Star(self)
        star_width, star_height = star.rect.size

        current_x, current_y = star_width, star_height
        while current_y < (self.settings.screen_height - star_height):
            while current_x < (self.settings.screen_width - star_width):
                random_numbers = []
                for i in range(0, 2):
                    random_numbers.append(randint(-100, 100))
                self._create_star(current_x + random_numbers[0], current_y + random_numbers[1])
                current_x += 2 * star_width
            current_x = star_width
            current_y += 2 * star_height

    def _create_star(self, x_position, y_position):
        new_star = Blue_Star(self)
        new_star.x = x_position
        new_star.rect.x = x_position
        new_star.rect.y = y_position
        self.blue_star.add(new_star)

    def _create_asteroids(self):
        asteroid = Asteroid(self)
        asteroid_width, asteroid_height = asteroid.rect.size

        current_x, current_y = asteroid_width, asteroid_height
        if randint(0, 400) < 10:
            self._create_asteroid(randint(0, self.settings.screen_width), 
                0)

    def _create_asteroid(self, x_position, y_position):
        new_asteroid = Asteroid(self)
        new_asteroid.x = x_position
        new_asteroid.rect.x = x_position
        new_asteroid.rect.y = y_position
        self.asteroids.add(new_asteroid)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.blue_star.draw(self.screen)
        self.asteroids.draw(self.screen)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    #ai = AlienInvasion()
    #ai.run_game()
    AlienInvasion().run_game()