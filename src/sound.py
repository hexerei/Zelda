import pygame
from settings import *

class SoundPlayer:

    def __init__(self):
        self.sounds = {
            'main': {'sound': None, 'source': '../sfx/main.ogg', 'volume': 0.5},
            'player_attack': {'sound': None, 'source': '../sfx/sword.wav', 'volume': 0.4},
            'enemy_death': {'sound': None, 'source': '../sfx/death.wav', 'volume': 0.6},
            'enemy_hit': {'sound': None, 'source': '../sfx/hit.wav', 'volume': 0.6},
            'magic_heal': {'sound': None, 'source': '../sfx/heal.wav', 'volume': 0.6},
            'magic_flame': {'sound': None, 'source': '../sfx/Fire.wav', 'volume': 0.6},
        }
        #for name in monster_data.keys():
        #    self.sounds['enemy_' + name] =  {'sound': None, 'source': monster_data[name]['attack_sound'], 'volume': 0.6}
        self.main_volume = 1.0
        pygame.mixer.init()

    def volume(self, level = None):
        if level:
            self.main_volume = level
            # update volume of loaded sounds
            for sound in self.sounds.values():
                if isinstance(sound['sound'], pygame.mixer.Sound):
                    sound['sound'].set_volume(sound['volume'] * self.main_volume)
        return self.main_volume

    def load(self, sound_name, source = None, volume = 1.0):
        if not sound_name in self.sounds.keys():
            if source:
                self.sounds[sound_name] = {
                    'sound': None,
                    'source': source,
                    'volume': volume
                }
            else:
                print(f'Could not find sound: {sound_name}')
                return None
        sound = self.sounds[sound_name]
        if not isinstance(sound['sound'], pygame.mixer.Sound):
            print(f"Loading sound source: {sound['source']}")
            sound['sound'] = pygame.mixer.Sound(sound['source'])
            sound['sound'].set_volume(sound['volume'] * self.main_volume)
        return sound['sound']

    def preload(self):
        for name in self.sounds.keys():
            self.load(name)

    def play(self, sound_name, loops = 0):
        sound = self.load(sound_name)
        if sound:
            sound.play(loops=loops)

if __name__ == '__main__':
    sound = SoundPlayer()
    sound.preload()