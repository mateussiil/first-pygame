class Camera:
    def __init__(self, game):
        self.game = game
        self.true_pos = [0, 0]
        self.target_pos = [0,0]
        
    def set_target(self, pos):
        self.target_pos = pos

    def update(self):
        self.true_pos[0] += (( self.target_pos[0] - self.true_pos[0]) - (800/3 + 10))/20
        self.true_pos[1] += (( self.target_pos[1] - self.true_pos[1]) - (600/3 + 10))/20