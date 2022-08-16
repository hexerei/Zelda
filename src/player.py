import pygame 
from settings import *
from support import import_folder
from debug import debug

class Player(pygame.sprite.Sprite):

	def __init__(self,pos,groups,obstacle_sprites):

		super().__init__(groups)

		self.image = pygame.image.load('../gfx/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15


		# movement
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		charcter_path = '../gfx/player/'
		self.animations = {
			'up': [],
			'down': [],
			'left': [],
			'right': [],
			'up_idle': [],
			'down_idle': [],
			'left_idle': [],
			'right_idle': [],
			'up_attack': [],
			'down_attack': [],
			'left_attack': [],
			'right_attack': []
		}

		for animation in self.animations.keys():
			full_path = charcter_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):

		if not self.attacking:

			# get pressed keys
			keys = pygame.key.get_pressed()

			# check for vertical movement
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			# check for horizontal movement
			if keys[pygame.K_LEFT]:
				self.status = 'left'
				self.direction.x = -1
			elif keys[pygame.K_RIGHT]:
				self.status = 'right'
				self.direction.x = 1
			else:
				self.direction.x = 0

			# check for attack
			if keys[pygame.K_SPACE] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()

			# check for magic
			if keys[pygame.K_LCTRL] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()

	def get_status(self):
		# attack status
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				else:
					self.status = self.status + '_attack'
		else:
			# idle status
			if self.direction.x == 0 and self.direction.y == 0:
				if not 'idle' in self.status:
					if 'attack' in self.status:
						self.status = self.status.replace('_attack', '_idle')
					else:
						self.status = self.status + '_idle'

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

	def cooldowns(self):
		if self.attacking:
			current_time = pygame.time.get_ticks()
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# se the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		debug(self.status)