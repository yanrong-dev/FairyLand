import random

import pygame

import assets
import configs
from objects.layer import Layer


class Star(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.REWARD
        self.images = [
            assets.get_sprite("star_" + str(i)) for i in range(1, 9)
        ]
        self.frame_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH + 150, random.uniform(100, 300)))

        self.mask = pygame.mask.from_surface(self.image)
        #print(self.mask)

        super().__init__(*groups)

    def collect(self):
        self.kill()

    def update(self):
        self.rect.x -= 2
        self.frame_index += 1
        self.image_index = (int(self.frame_index / (configs.FPS / configs.ANIMATION_FPS)) + 1) % len(self.images)
        self.image = self.images[self.image_index]