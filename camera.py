import pygame
import sys

from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

pygame.display.set_caption("My pygame Window")

WINDOW_SIZE = (800, 600)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((800, 600))

player_image = pygame.image.load('./image/chicken.png')
player_image.set_colorkey((255, 255, 255))
grass_image = pygame.image.load('./image/grass.png')
terra_image = pygame.image.load('./image/terra.png')
terra2_image = pygame.image.load('./image/terra2.png')
terra3_image = pygame.image.load('./image/terra3.png')
terra4_image = pygame.image.load('./image/terra4.png')
terra5_image = pygame.image.load('./image/terra5.png')
terra6_image = pygame.image.load('./image/terra6.png')

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
while True:
    display.fill((146, 244, 255))
    
    true_scroll[0] += ((player_rect.x - true_scroll[0]) - (WINDOW_SIZE[0]/3 + 10))/20
    true_scroll[1] += ((player_rect.y - true_scroll[1]) - (WINDOW_SIZE[1]/3 + 10))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    y = 0
    tile_rects = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(terra_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(terra2_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '3':
                display.blit(terra3_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '4':
                display.blit(terra4_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '5':
                display.blit(terra5_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '6':
                display.blit(terra6_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
            if tile == '7':
                display.blit(grass_image, (x*TILE_SIZE-scroll[0], y*TILE_SIZE-scroll[1]))
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
    player_y_momentum += 0.5
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    
    if collisions["bottom"]:
        stamina += 2
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1
        
    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    # player_rect.y = player_location[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum -= 6
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
