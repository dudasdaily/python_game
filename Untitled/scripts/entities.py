class Entity:
    def __init__(self, game):
        self.game = game

        self.movement = [0, 0]
        self.velocity = [0, 0]
    
    def update(self):
        pass

    def render(self):
        pass

class Player:
    def __init__(self, game):
        super().__init__(game)
        self.state = {
            "left" : False,
            "right" : False,
            "space" : False,
        }
    
    def update(self):
        pass

    def render(self):
        pass