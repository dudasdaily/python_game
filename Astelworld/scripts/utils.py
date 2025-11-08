from ast import List
import os
import pygame

BASE_IMG_PATH = 'data/jump/images/'

def load_image(path, colorkey = (0,0,0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(colorkey)
    
    return img

def load_images(path, colorkey = (0,0,0)):
    images = []
    # 리눅스와 윈도우에서 os.listdir이 작동하는 방식이 다르기 때문에 sorted
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, colorkey=colorkey))

    return images

class Animation:
    def __init__(self, images, img_dur = 5, loop = True):
        """
            img_duration * len(images) => 총 프레임 수
            예를 들어서 이미지가 [0.png, 1.png, 2.png] 이렇게 3개 있고 img_duration = 5 이면,
            0.png를 5프레임, 1.png를 5프레임, 2.png를 5프레임 이렇게 총 15프레임으로 애니메이션을 재생함
        """
        self.images = images
        self.loop = loop
        self.img_duration = img_dur # [0.png, 1.png, 2.png, ...] 이 이미지 하나하나가 유지될 프레임 수
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)] # 보여줄 이미지 프레임 반환!


    
        