import pygame


class Ship:
	"""A class to manage the ship."""

	def __init__(self, ai_game):
		"""Initialize the ship and set its starting position."""
		self.screen=ai_game.screen
		self.screen_rect=ai_game.screen.get_rect()
		self.settings = ai_game.settings

		# Load the ship image and gets its rect.
		self.image=pygame.image.load('images/DurrrSpaceShip.png')
		self.rect=self.image.get_rect()

		# Start the ship at the bottom center of the screen.
		self.rect.midbottom=self.screen_rect.midbottom

		# Store a float for the ship's exact horizontal position.
		self.x=float(self.rect.x)

		#Movement flag: start with a ship that's not moving.
		self.moving_right=False
		self.moving_left=False
		self.boost=False

	def update(self):
		# Local variable for self.settings.ship_speed
		speed = self.settings.ship_speed

		if self.boost:
			speed*=2

		"""Update the ship's position based on the movement flag."""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x+=speed
		if self.moving_left and self.rect.left > 0:
			self.x-=speed

		# Update rect object from self.x.
		self.rect.x=self.x

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)