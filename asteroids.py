import pygame
from pygame.sprite import Sprite
from random import randint

asteroid_list = []
for i in range(1, 10):
	asteroid_list.append('images/asteroid_' + str(i) + '_30x30.png')


class Asteroid(Sprite):

	def __init__(self, ai_game):
		super().__init__()
		self.screen = ai_game.screen


		self.image = pygame.image.load(asteroid_list[randint(0, 8)])
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		self.y = float(self.rect.y)

	def update(self):
		self.y += 5
		self.rect.y = self.y