import pygame
import os

BASE_PATH = 'data/images/'

def load_image(path, colorkey=(0, 0, 0)):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey(colorkey)

    return img

def load_images(path, colorkey=(0, 0, 0)):
    images = []

    for img_name in sorted(os.listdir(BASE_PATH + path)):
        image = load_image(f'{path}/{img_name}', colorkey=colorkey)
        images.append(image)

    return images

class Animation:
    def __init__(self, images, img_dur=5, loop=False):
        self.images = images
        self.img_dur = img_dur
        self.loop = loop

        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_dur)]