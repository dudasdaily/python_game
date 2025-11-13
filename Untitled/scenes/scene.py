# Scene 인터페이스 => 다양한 scene들이 얘를 상속받아서 씀
class Scene:
    def __init__(self, game, manager):
        self.game = game # 의존성 주입으로 Scene에서 game자원에 접근 가능하게 함
        self.manager = manager

    def handle_events(self, events): pass
    def update(self, dt): pass
    def render(self, surf, offset=(0, 0)): pass