
class Game:
    def __init__(self):
        self.window = Window(self)
    
    def update(self):
        self.input.update()
        
    def run(self):
        while True:
            self.update()
            
Game().run()
