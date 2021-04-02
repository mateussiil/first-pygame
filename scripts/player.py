from scripts.entity import *

class Player(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.movement = [0,0]