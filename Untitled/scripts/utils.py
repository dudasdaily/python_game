import pygame
import os

BASE_PATH = '/data/images'

def load_image(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey(colorkey)

    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []

    for img_name in sorted(os.listdir(BASE_PATH + path)):
        image = load_image(f'{path}/{img_name}', colorkey=colorkey)

    return images