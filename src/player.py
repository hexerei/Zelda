import pygame 
from settings import *

class Player(pygame.sprite.Sprite):

	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('../gfx/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		self.direction = pygame.math.Vector2()
		self.speed = 5

		self.obstacle_sprites = obstacle_sprites

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
		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					elif self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					elif self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def update(self):
		self.input()
		self.move(self.speed)