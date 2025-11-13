# Scene 인터페이스 => 다양한 scene들이 얘를 상속받아서 씀
class Scene:
    def __init__(self, manager):
        self.manager = manager

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self, screen):
        pass

class SceneManager:
    def __init__(self, start_scene):
        self.current_scene = start_scene

    def go_to(self, scene):
        self.current_scene = scene