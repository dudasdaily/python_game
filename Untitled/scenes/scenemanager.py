from scenes.battle import Battle
from scenes.maingame import Maingame
from scenes.title import Title

class SceneManager:
    def __init__(self, game, start_scene: str):
        self.scenes = {
            "title" : Title(game, self),
            "battle" : Battle(game, self),
            "maingame" : Maingame(game, self),
            }
        
        self.current_scene = self.scenes[start_scene]

    def go_to(self, scene):
        self.current_scene = self.scenes[scene]