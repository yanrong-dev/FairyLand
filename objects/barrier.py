import random

import pygame

import assets
import configs
from objects.layer import Layer

class Barrier(pygame.sprite.Sprite):
    def __init__(self, floor_y, current_level, index, *groups):
        # floor_y is the y position of the floor
        # we should go beyond this value

        ground_barriers = assets.search_sprite("barrier")
        sky_barriers = assets.search_sprite("vine_")

        self._layer = Layer.OBSTACLE
        # when levels up, narrow the vertical gap
        self.gap = configs.LEVEL_ONE_GAP * (configs.GAP_NARROWING_FACTOR ** (current_level - 1))
        self.sky_barrier = sky_barriers[random.randint(0, len(sky_barriers) - 1)]
        self.ground_barrier = ground_barriers[random.randint(0, len(ground_barriers) - 1)]

        self.barrier_top = self.sky_barrier
        gap_y_offset = random.uniform(-250, -130)
        top_x_offset = random.uniform(0, 80)
        bottom_x_offset = random.uniform(0, 40)
        self.barrier_top_rect = self.barrier_top.get_rect(topleft=(top_x_offset, gap_y_offset))

        #print("floor_y", floor_y)
        remaining_height = floor_y - (self.barrier_top_rect.y + self.barrier_top_rect.height) - self.gap
        #print("remaining_height=", remaining_height)

        self.barrier_bottom_sprite = self.ground_barrier
        #scale_ratio = remaining_height / self.barrier_bottom_sprite.get_rect().height
        #self.barrier_bottom = pygame.transform.scale(self.barrier_bottom_sprite, (self.barrier_bottom_sprite.get_rect().width * scale_ratio, remaining_height))
        self.barrier_bottom = self.barrier_bottom_sprite
        #self.barrier_bottom_rect = self.barrier_bottom.get_rect(topleft=(bottom_x_offset, self.barrier_top_rect.y + self.barrier_top_rect.height + self.gap))
        self.barrier_bottom_rect = self.barrier_bottom.get_rect(topleft=(bottom_x_offset,  self.barrier_top_rect.y + self.barrier_top_rect.height + self.gap))
        #print("barrier_bottom_rect=", self.barrier_bottom_rect)

        self.image = pygame.surface.Surface((max(self.barrier_top_rect.width + top_x_offset, self.barrier_bottom_rect.width + bottom_x_offset), floor_y), pygame.SRCALPHA)
        self.image.blit(self.barrier_top, self.barrier_top_rect)
        self.image.blit(self.barrier_bottom, self.barrier_bottom_rect)
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH, 0))

        self.passed = False
        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2
        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False