import pygame 
from settings import *
from support import import_folder
from debug import debug
from entity import Entity

class Player(Entity):

	def __init__(self, pos,groups,obstacle_sprites, create_attack, destroy_attack, create_magic, sound_player):

		super().__init__(groups, sound_player)

		self.image = pygame.image.load('../gfx/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])

		# graphics setup
		self.obstacle_sprites = obstacle_sprites
		self.import_player_assets()
		self.status = 'down'

		# attack
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.weapon_switch_cooldown = 200

		# magic
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		# stats
		self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'magic': 4, 'speed': 6}
		self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'magic': 10, 'speed': 10}
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
		self.health = self.stats['health'] * 0.5
		self.energy = self.stats['energy'] * 0.8
		self.exp = 5000
		self.speed = self.stats['speed']

        # invincibiilty timer
		self.vulnerable = True
		self.hurt_time = None
		self.invincibility_duration = 300

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
				self.create_attack()
				self.sound.play('player_attack')

			# check for magic
			if keys[pygame.K_LALT] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_magic(self.magic,
					magic_data[self.magic]['strength'] + self.stats['magic'],
					magic_data[self.magic]['cost']
				)

			# switch weapon
			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0
				self.weapon = list(weapon_data.keys())[self.weapon_index]

			# switch magic
			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0
				self.magic = list(magic_data.keys())[self.magic_index]

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

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
				self.can_switch_weapon = True

		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.weapon_switch_cooldown:
				self.can_switch_magic = True

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# flicker
		if not self.vulnerable:
			self.image.set_alpha(self.wave_value())
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage
	
	def get_full_magic_damage(self):
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']
		return base_damage + spell_damage
	
	def get_value_by_index(self, index):
		return list(self.stats.values())[index]

	def get_cost_by_index(self, index):
		return list(self.upgrade_cost.values())[index]

	def energy_recovery(self):
		if self.energy < self.stats['energy']:
			self.energy += 0.01 * self.stats['magic']
		else:
			self.energy = self.stats['energy']

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
		self.energy_recovery()
		# debug(self.status)