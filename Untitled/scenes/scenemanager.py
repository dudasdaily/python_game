from scenes.battle import Battle
from scenes.maingame import Maingame
from scenes.title import Title
from scenes.interact import Interact

class SceneManager:
    def __init__(self, game, start_scene: str):
        self.scenes = {
            "title" : Title(game, self),
            "battle" : Battle(game, self),
            "maingame" : Maingame(game, self),
            "interact" : Interact(game, self),
        }

        self.current_scene = self.scenes[start_scene]
        self.current_scene.collided_obj = None

    def go_to(self, scene, obj):
        self.current_scene = self.scenes[scene]
        self.current_scene.collided_obj = obj