import pygame
import sys

from scripts.hud import TextBox, InteractBox
from scenes.scene import Scene

class Interact(Scene):
    TEXT_BOX_COLOR = (255, 255, 255, 200)
    SELECTED_COLOR = (0, 0, 0)
    UNSELECTED_COLOR = (169, 169, 169)

    def __init__(self, game, manager):
        super().__init__(game, manager)
        self.collided_obj = None # maingame에서 sm.go_to(obj)로 초기화
        
        self.texts = [] # 텍스트 박스(TextBox)의 내용
        self.interect_texts = [] # 상호작용 박스(InteractBox)의 내용

        self.init_cnt = 0

        self.box_queue = [] # Box들을 담은 순서

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pass
                if event.key == pygame.K_RIGHT:
                    pass
                if event.key == pygame.K_SPACE and self.box_queue:
                    if isinstance(self.box_queue[0], TextBox):
                        self.box_queue.pop(0)

                    if isinstance(self.box_queue[0], InteractBox):
                        self.game.sm.scenes['maingame'].map.obj_list.remove(self.collided_obj)
                        self.game.sm.scenes['maingame'].map.update()
                        self.box_queue.pop(0)

                    
            if event.type == pygame.KEYUP:
                pass

    def update(self, dt):
        self.game.sm.scenes['maingame'].update(dt)

        # 플레이어가 객체와 충돌 했을 때!
        if self.collided_obj and not self.init_cnt:
            self.init_cnt += 1

            for texts in self.collided_obj.texts:
                self.texts.append(texts.split('\n'))

            self.interect_texts = self.collided_obj.interact_text.split('\n')

            for text in self.texts:
                self.box_queue.append(TextBox(self.game, text))

            self.box_queue.append(InteractBox(self.game, self.interect_texts))
        
        if not self.box_queue:
            self.__init__(self.game, self.manager)
            self.manager.go_to("maingame", None)

        print(f'len: {len(self.box_queue)}, texts: {self.texts}, interect_texts: {self.interect_texts}')

        for box in self.box_queue:
            box.update()

    def render(self, surf):
        # 베이스 씬 렌더링
        self.game.sm.scenes["maingame"].render(surf)

        if self.box_queue:
            self.box_queue[0].render(surf)