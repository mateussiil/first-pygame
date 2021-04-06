import pygame

class Entity:
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.movement = [0,0]
        self.action = None
        self.animation_database = {}
        self.animation_frames = {}
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    
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
    
    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list
    
    def updateRect(self):
        print(self.pos)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def load_animation(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 1
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc)
            # animation_image.set_colorkey((255, 255, 255)) fundo da imagem
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data


    def change_action(self, action_var, frame, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame
