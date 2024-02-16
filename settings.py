class Settings:
	"""A class to store all settings for Alien Invasion."""

	def __init__(self):
		"""Initialize the game's settings."""
		# Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (17, 70, 193)
		self.clock_tick = 60

		# Ship settings
		self.ship_speed = 2.0
		self.ship_limit = 3

		# Bullet settings
		self.bullet_speed = 5.0
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		# Alien settings
		self.alien_speed = 2.0
		self.fleet_drop_speed = 25
		# fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1