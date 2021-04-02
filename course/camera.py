import pygame
import sys
import random

from pygame.locals import *

sys.path.append(".")
from scripts.camera  import *
from scripts.entity import *
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(64)

pygame.display.set_caption("My pygame Window")

WINDOW_SIZE = (800, 600)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((800, 600))

player = Entity(50,50, pygame.image.load('./image/idle/idle_1.png').convert())

player_image = pygame.image.load('./image/idle/idle_1.png').convert()
# player_image.set_colorkey((255, 255, 255))

player_rect = pygame.Rect(100, 100, 5, 13)
background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [
    0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

grass_image = pygame.image.load('./image/grass.png')
terra_image = pygame.image.load('./image/terra.png')
terra2_image = pygame.image.load('./image/terra2.png')
terra3_image = pygame.image.load('./image/terra3.png')
terra4_image = pygame.image.load('./image/terra4.png')
terra5_image = pygame.image.load('./image/terra5.png')
terra6_image = pygame.image.load('./image/terra6.png')

jump_sound = pygame.mixer.Sound('./sounds/jump.wav')
grass_sounds = [pygame.mixer.Sound(
    './sounds/grass_0.wav'), pygame.mixer.Sound('./sounds/grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

pygame.mixer.music.load('./sounds/music.wav')
pygame.mixer.music.play(-1)

TILE_SIZE = grass_image.get_width()


def load_map(path):
    f = open(path+'.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('./map/map')

global animation_frames
animation_frames = {}


def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 1
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc)
        # animation_image.set_colorkey((255, 255, 255)) fundo da imagem
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


animation_database = {}
animation_database["run"] = load_animation('image/run', [10, 10, 10, 10])
animation_database["idle"] = load_animation('image/idle', [10])

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {"top": False, "bottom": False,
                       "right": False, "left": False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True

    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True

    return rect, collision_types


moving_right = False
moving_left = False
moving_up = False
moving_down = False

player_location = [50, 50]
player_y_momentum = 0
air_timer = 0

true_scroll = [0, 0]

player_rect = pygame.Rect(
    50, 50, player_image.get_width(), player_image.get_height())
test_rect = pygame.Rect(100, 100, 100, 50)
Camera = Camera('ok') 

while True:
    display.fill((146, 244, 255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1
        
    Camera.set_target([player_rect.x, player_rect.y])
    Camera.update()
    
    scroll = Camera.true_pos
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # paralalex
    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 100, 1500, 700))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0]*background_object[0], background_object[1]
                               [1] - scroll[1]*background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)
    y = 0
    tile_rects = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(terra_image, (x*TILE_SIZE -
                                           scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(terra2_image, (x*TILE_SIZE -
                                            scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '3':
                display.blit(terra3_image, (x*TILE_SIZE -
                                            scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '4':
                display.blit(terra4_image, (x*TILE_SIZE -
                                            scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '5':
                display.blit(terra5_image, (x*TILE_SIZE -
                                            scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '6':
                display.blit(terra6_image, (x*TILE_SIZE -
                                            scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '7':
                display.blit(grass_image, (x*TILE_SIZE -
                                           scroll[0], y*TILE_SIZE-scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(
                    x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]

    if moving_right == True:
        player_movement[0] += 5
    if moving_left == True:
        player_movement[0] -= 5

    player_movement[1] += player_y_momentum
    player_y_momentum += 0.9
    if player_y_momentum > 3:
        player_y_momentum = 3

    if player_movement[0] > 0:
        player_action, player_frame = change_action(
            player_action, player_frame, 'run')
        player_flip = True
    if player_movement[0] == 0:
        player_action, player_frame = change_action(
            player_action, player_frame, 'idle')
    if player_movement[0] < 0:
        player_action, player_frame = change_action(
            player_action, player_frame, 'run')
        player_flip = False
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions["bottom"]:
        player_y_momentum = 0
        air_timer = 0
        if player_movement[0] != 0:
             if grass_sound_timer == 0:
                 grass_sound_timer =30
                 random.choice(grass_sounds).play()
    else:
        air_timer += 1

    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0

    player_img_id = animation_database[player_action][player_frame]
    player_image = animation_frames[player_img_id]

    display.blit(pygame.transform.flip(player_image, player_flip, False), (player_rect.x -
                                                                           scroll[0], player_rect.y - scroll[1]))

    # player_rect.y = player_location[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                pygame.mixer.music.fadeout(1000)
            if event.key == K_e:
                pygame.mixer.music.play(-1)
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 10:
                    jump_sound.play()
                    player_y_momentum -= 10
            if event.key == K_DOWN:
                moving_down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(60)