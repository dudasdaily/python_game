import os
import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    
    return img

def load_images(path):
    images = []
    # 리눅스와 윈도우에서 os.listdir이 작동하는 방식이 다르기 때문에 sorted
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))

    return images