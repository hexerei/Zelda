import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemy(Entity):

    def __init__(self, monster_name, pos, group, obstacle_sprites):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['health']
        self.speed = monster_info['health']
        self.attack_damage = monster_info['health']
        self.resistance = monster_info['health']
        self.attack_radius = monster_info['health']
        self.notice_radius = monster_info['health']
        self.attack_type = monster_info['attack_type']

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        main_path = f'../gfx/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def update(self):
        self.move(self.speed)