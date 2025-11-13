import pygame
import sys

from scenes.scenemanager import SceneManager

FRAME = 60
pygame.init()

class Game:
    def __init__(self):
        # pygame 설정들
        self.screen = pygame.display.set_mode((640, 480))
        self.display =pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

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

            # 화면 렌더링
            pygame.transform.scale(self.display, self.screen.get_size(), self.screen)
            pygame.display.update()

Game().run()