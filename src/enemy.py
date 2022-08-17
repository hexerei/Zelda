import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):

    def __init__(self, monster_name, pos, groups, obstacle_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        self.can_attack = True

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../gfx/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        dist_vec = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        distance = dist_vec.magnitude()
        if distance > 0:
            direction = dist_vec.normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'
        return self.status

    def actions(self, player):
        if self.status == 'attack':
            print('attack')
        elif self.status == 'move':
            print('move')
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.move(self.speed)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)