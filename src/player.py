import pygame 
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.image.load('../gfx/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		# get pressed keys
		keys = pygame.key.get_pressed()

		# check for vertical movement
		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		# check for horizontal movement
		if keys[pygame.K_LEFT]:
			self.direction.x = -1
		elif keys[pygame.K_RIGHT]:
			self.direction.x = 1
		else:
			self.direction.x = 0

	def move(self,speed):
		# normalize vector to 1 to fix speed
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		# apply delta to current position
		self.rect.center += self.direction * speed

	def update(self):
		self.input()
		self.move(self.speed)