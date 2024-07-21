import random

import pygame

import assets
import configs
from objects.layer import Layer


class Finish(pygame.sprite.Sprite):
    def __init__(self, floor_y, *groups):
        self._layer = Layer.FINISH
        self.image = assets.get_sprite("finish")
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH * 2.5, floor_y - self.image.get_size()[1]))

        self.passed = False
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

    def is_passed(self):
        if self.rect.x <= 100 and not self.passed:
            self.passed = True
            return True
        return False