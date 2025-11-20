from json import load
import pygame
import sys

from scenes.scenemanager import SceneManager
from scripts.utils import load_image, load_images, Animation

FRAME = 30
pygame.init()

class Game:
    def __init__(self):
        # pygame 설정들
        self.screen = pygame.display.set_mode((640, 480))
        self.display =pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()
        
        self.assets = {
            'background' : load_image('background.png'),
            'player/idle' : Animation(load_images('player/idle'), img_dur=30, loop=True),
            'player/run' : Animation(load_images('player/run'), img_dur=15, loop=True),
            # 'arrow/left' : Animation(load_images('ui/arrow/left'), loop=True),
            # 'arrow/left_select' : Animation(load_images('ui/arrow/left_select'), loop=True),
            # 'arrow/right' : Animation(load_images('ui/arrow/right'), loop=True),
            # 'arrow/right_select' : Animation(load_images('ui/arrow/right_select'), loop=True),    
            'arrow/left' :load_image('ui/arrow/left/00.png'),
            'arrow/left_select' :load_image('ui/arrow/left_select/00.png'),
            'arrow/right' :load_image('ui/arrow/right/00.png'),
            'arrow/right_select' :load_image('ui/arrow/right_select/00.png'),
            # Hp/Ap
            'hp' : Animation(load_images('ui/hp'), img_dur=10, loop=True),
            'ap' : Animation(load_images('ui/ap'), img_dur=10, loop=True),
            'hp_base' : load_image('ui/hp_base.png'),
            'ap_base' : load_image('ui/ap_base.png'),
        }
 
        # Scene 관련 설정
        self.sm = SceneManager(self, "title")  
        # self.sm.current_scene.manager = self.sm

    def run(self):
        play = True 
        while play:
            dt = self.clock.tick(FRAME) / 1000 # dt = 직전 업데이트로부터 흐른 시간 (sec)

            # 유저 입력
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            scene = self.sm.current_scene
            scene.handle_events(events)
            scene.update(dt)
            scene.render(self.display)

            # print(self.sm.current_scene)

            # 화면 렌더링
            pygame.transform.scale(self.display, self.screen.get_size(), self.screen)
            pygame.display.update()

Game().run()