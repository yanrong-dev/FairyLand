import pygame

import assets
import configs
from objects import layer
from objects.collision import Collision
from objects.layer import Layer


class Fairy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.PLAYER
        self.images = assets.search_sprite("fairysprite")
        self.frame_index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(-50, 50))

        self.mask = pygame.mask.from_surface(self.image)
        #print(self.mask)

        self.drop_speed = 0
        super().__init__(*groups)

    def update(self):
        self.frame_index += 1
        self.image_index = (int(self.frame_index / (configs.FPS / configs.ANIMATION_FPS)) + 1) % len(self.images)
        self.image = self.images[self.image_index]
        self.drop_speed += configs.GRAVITY
        self.rect.y += self.drop_speed
        if self.rect.x < 50:
            self.rect.x += 2

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_speed = -4
            assets.play_audio("flap")

    def check_overlap(self, sprite):
        if not hasattr(sprite, 'mask'):
            sprite.mask = pygame.mask.from_surface(sprite.image)
        if sprite.mask.overlap(self.mask,
                               (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)):
            return True
        return False

    def check_collision(self, sprites):
        if self.rect.bottom < 0:
            return True
        for sprite in sprites:
            if sprite._layer in [Layer.FLOOR, Layer.OBSTACLE]:
                if self.check_overlap(sprite):
                    return Collision.DIE
        for sprite in sprites:
            if sprite._layer in [Layer.REWARD]:
                if self.check_overlap(sprite):
                    sprite.collect()
                    return Collision.REWARD
        return Collision.NONE
