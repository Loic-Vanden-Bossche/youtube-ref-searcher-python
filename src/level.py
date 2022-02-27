import pygame
from pygame_gui.core import ObjectID

from player import Player
from enemy import Enemy
from bullet import Bullet
from settings import *
import pygame_gui
from random import *

import utils


class Names:

    def get_cursor(self):
        if self._cursor >= len(self._names):
            self._cursor = -1

        self._cursor += 1
        return self._cursor

    @property
    def current(self):
        return self._names[self.get_cursor()]

    def __init__(self, names):
        self._cursor = -1

        shuffle(names)
        self._names = names

class StatusBar(pygame_gui.elements.UIPanel):

    @property
    def wave(self):
        return self.status_text.text

    @wave.setter
    def wave(self, wave):
        self.status_text.set_text(f'Wave {wave}')

    def __init__(self, width, manager):
        super().__init__(pygame.Rect(pygame.display.get_surface().get_width() - width, 0, width, 75), 1, manager)

        self.status_text = pygame_gui.elements.UILabel(
            pygame.Rect(0, 0, self.relative_rect.w, self.relative_rect.h),
            'wave 1', self.ui_manager, container=self, object_id=ObjectID('#wave_text'))



def sprite_alive(sprite):
    return sprite.alive()


class Level:
    def __init__(self, channel_id,  difficulty, names):
        self._manager = pygame_gui.UIManager((WIDTH, HEIGHT), '../themes/game.json')
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.player = Player(channel_id, GOAL, (self.visible_sprites,), difficulty)
        self.enemies = []
        self.bullets = []
        self.wave = 1
        self.enemiesFactor = 10
        self.enemiesSpawnOffset = 3000
        self.timeToEnemySpawn = None
        self.inFight = True
        self.enemiesSpawned = 0
        self.enemiesNames = Names(names)
        self.channel_thumbs = [f'../cache/{channel_id}/video_thumbs/{video_file}' for video_file in utils.getFiles(f'../cache/{channel_id}/video_thumbs', '')]
        self.status_bar = StatusBar(200, self._manager)

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.player.is_alive():
                self.bullets.append(Bullet(self.channel_thumbs, (self.visible_sprites,)))

    def get_level_scores(self):
        return self.wave

    def spawn_enemy(self):
        if choice([False, True]):
            x_position = randint(-30, WIDTH + 30)
            y_position = choice([randint(-30, 0), randint(HEIGHT, HEIGHT + 30)])

        else:
            x_position = choice([randint(-30, 0), randint(WIDTH, WIDTH + 30)])
            y_position = randint(-30, HEIGHT + 30)

        self.enemies.append(Enemy(
            (x_position, y_position),
            (self.visible_sprites,),
            self.player,
            self._manager,
            self.enemiesNames.current))
        self.enemiesSpawned += 1

    def update(self, time_delta):
        self.bullets = list(filter(sprite_alive, self.bullets))
        self.enemies = list(filter(sprite_alive, self.enemies))

        if len(self.visible_sprites):
            if not self.player.is_alive():
                self.inFight = False

            if self.inFight and (self.enemiesSpawned < self.wave * self.enemiesFactor):
                if self.timeToEnemySpawn:
                    if pygame.time.get_ticks() >= self.timeToEnemySpawn + self.enemiesSpawnOffset:
                        self.timeToEnemySpawn = pygame.time.get_ticks()
                        self.spawn_enemy()
                else:
                    self.timeToEnemySpawn = pygame.time.get_ticks()
                    self.spawn_enemy()

            elif self.inFight and not len(self.enemies):
                self.enemiesSpawnOffset = self.enemiesSpawnOffset * 0.85
                self.wave += 1
                self.status_bar.wave = self.wave
                self.enemiesFactor += ENEMIES_FACTOR_AUGMENTATION

            for bullet in self.bullets:
                bullet.check_collision(self.enemies)

            self.visible_sprites.draw(self.display_surface)
            self._manager.draw_ui(self.display_surface)
            self.visible_sprites.update()
            self._manager.update(time_delta)
