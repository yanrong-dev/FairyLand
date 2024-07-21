import os
import sys

import pygame
sprites = {}
audios = {}

def get_current_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    # If it's not use the path we're on now
    else:
        return os.path.dirname(__file__)
def load_sprites():
    path = os.path.join(get_current_path(), "assets", "sprites")
    print(path)
    for file in os.listdir(path):
        sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))



def get_sprite(name):
    return sprites[name]

def search_sprite(name):
    found = []
    for key in sprites:
        if key.startswith(name):
            found.append(sprites[key])
    return found

def load_audio():
    path = os.path.join(get_current_path(), "assets", "audios")
    print(path)
    for file in os.listdir(path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))

def play_audio(name):
    audios[name].play()