import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock=pygame.time.Clock()
        self.settings=Settings()

        self.screen=pygame.display.set_mode((self.settings.screen_width,
            self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship=Ship(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(self.settings.clock_tick)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.KEYDOWN:
                    # Move the ship +/- on x axis
                    if event.key==pygame.K_RIGHT:
                        self.ship.moving_right = True 
                    elif event.key==pygame.K_LEFT:
                        self.ship.moving_left=True
                    elif event.key==pygame.K_LSHIFT:
                        self.ship.boost=True
                elif event.type==pygame.KEYUP:
                    if event.key==pygame.K_RIGHT:
                        self.ship.moving_right=False
                    elif event.key==pygame.K_LEFT:
                        self.ship.moving_left=False
                    elif event.key==pygame.K_LSHIFT:
                        self.ship.boost=False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        pygame.display.flip()


if __name__=='__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()