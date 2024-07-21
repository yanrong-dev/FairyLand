import random

import pygame

import assets
import configs

from objects.background import Background
from objects.collision import Collision
from objects.barrier import Barrier
from objects.fairy import Fairy
from objects.finish import Finish
from objects.floor import Floor
from objects.game_over_message import GameOverMessage
from objects.game_phase import GamePhase
from objects.game_start_message import GameStartMessage
from objects.layer import Layer
from objects.level_complete_message import LevelCompleteMessage
from objects.score import Score
from objects.star import Star
from objects.welcome import Welcome

pygame.init()

screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
clock = pygame.time.Clock()
hide_welcome_event = pygame.USEREVENT
column_create_event = pygame.USEREVENT
next_level_event = pygame.USEREVENT
floor_y = 0
running = True
score = 0

assets.load_sprites()
assets.load_audio()

sprites = pygame.sprite.LayeredUpdates()

def setup_game(with_start = True):
    global floor_y
    global bird, game_start_message, score
    for i in range(2):
        Background(i, sprites)
        floor = Floor(i, sprites)
        if floor_y == 0:
            floor_y = floor.get_floor_y()
            #print("floor_y = ", floor_y)
    pygame.time.set_timer(column_create_event, 1500)
    bird = Fairy(sprites)
    if with_start:
        game_start_message = GameStartMessage(sprites)
    score = Score(sprites)
    score.set_level(current_level)

game_over_message = None
bird = None
game_start_message = None
score = None

game_phase = GamePhase.WELCOME
columns_in_phase = 0
current_level = 1
welcome = Welcome(sprites)
pygame.time.set_timer(hide_welcome_event, 3000)
pygame.display.set_caption('FairyLand')
pygame_icon = assets.get_sprite("fairysprite1")
pygame.display.set_icon(pygame_icon)

while running:
    if game_phase == GamePhase.WELCOME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == hide_welcome_event:
                welcome.kill()
                game_phase = GamePhase.WAIT_TO_START
                setup_game()
    elif game_phase == GamePhase.WAIT_TO_START:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_start_message.kill()
                    if game_over_message is not None:
                        game_over_message.kill()
                    game_phase = GamePhase.PLAYING
                    columns_in_phase = 0
    elif game_phase == GamePhase.GAMEOVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Restart game")
                    game_over_message.kill()
                    sprites.empty()
                    setup_game()
                    game_phase = GamePhase.WAIT_TO_START
    elif game_phase == GamePhase.LEVEL_COMPLETE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == next_level_event:
                level_complete_message.kill()
                game_phase = GamePhase.PLAYING
                current_level += 1
                print("Playing level ", current_level)
                columns_in_phase = 0
                sprites.empty()
                setup_game(with_start = False)

    elif game_phase == GamePhase.PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == column_create_event:
                columns_in_phase += 1
                Barrier(floor_y, current_level, columns_in_phase, sprites)
                if random.uniform(0, 1) <= configs.SPAWN_STAR_PROB:
                    Star(sprites)
                if columns_in_phase >= configs.COLUMNS_PER_ROUND:
                    pygame.time.set_timer(column_create_event, 0)
                    Finish(floor_y, sprites)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Restarted")
                    game_phase = GamePhase.WAIT_TO_START
                    sprites.empty()
                    setup_game()
                else:
                    bird.handle_event(event)

    #screen.fill("pink")
    sprites.draw(screen)

    if game_phase == GamePhase.PLAYING:
        collision_check = bird.check_collision(sprites)
        if collision_check == Collision.REWARD:
            score.value += 1
            assets.play_audio("pop")

        if collision_check == Collision.DIE:
            game_phase = GamePhase.GAMEOVER
            current_level = 1
            game_over_message = GameOverMessage(sprites)
            pygame.time.set_timer(column_create_event, 0)
            assets.play_audio("hit")

        for sprite in sprites:
            if sprite._layer == Layer.OBSTACLE and sprite.is_passed():
                score.value += 1
                assets.play_audio("collect")
            if sprite._layer == Layer.FINISH and sprite.is_passed():
                game_phase = GamePhase.LEVEL_COMPLETE
                level_complete_message = LevelCompleteMessage(sprites)
                assets.play_audio("hooray")
                pygame.time.set_timer(next_level_event, 2500)

        sprites.update()

    pygame.display.flip()
    clock.tick(configs.FPS)
pygame.quit()