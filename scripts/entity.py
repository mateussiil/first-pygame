class Entity:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
    
    def move(self, rect, movement, tiles):
        collision_types = {"top": False, "bottom": False,
                        "right": False, "left": False}

        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types["right"] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types["left"] = True

        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types["bottom"] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types["top"] = True

        return rect, collision_types


    def collision_test(self,rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list