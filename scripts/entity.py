class Entity:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        
    