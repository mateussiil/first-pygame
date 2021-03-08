import pygame
import sys

from pygame.locals import *

mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('Physics Explanation')
screen = pygame.display.set_mode((500, 500), 0, 32)

player = pygame.Rect(150, 100, 40, 80)



tiles = [pygame.Rect(150, 450, 50, 50), 
         pygame.Rect(200, 450, 50, 50),
         pygame.Rect(250, 200, 50, 50),
         pygame.Rect(250, 250, 50, 50),
         pygame.Rect(250, 300, 50, 50),
         pygame.Rect(250, 350, 50, 50),
         pygame.Rect(250, 400, 50, 50),
         pygame.Rect(250, 450, 50, 50),
         ]

def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


def move(rect, movement, tiles):  # movement = [5,2]
    rect.x += movement[0]
    collisions = collision_test(rect, tiles)
    collision_types = {"top": False, "bottom": False,
                       "right": False, "left": False}
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types["right"] = True
        if movement[0] < 0:
            rect.left = tile.right
            collision_types["left"] = True
    rect.y += movement[1]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types["bottom"] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types["top"] = True
            
    return rect, collision_types

right = False
left = False
up = False
down = False

player_y_momentum = 0
air_timer = 0

stamina = 100
stamina_max = True
stamina_min = False

while True:
    # clear display
    screen.fill((0, 0, 0))

    movement = [0, 0]
    if right == True:
        movement[0] += 5
    if left == True:
        movement[0] -= 5
    if up == True and stamina_min!=True:
        movement[1] -= 5
    if down == True:
        movement[1] += 5
        
    movement[1] += player_y_momentum
    player_y_momentum += 0.2
    if player_y_momentum > 3:
        player_y_momentum = 3
        
    player_y_momentum += 0.2
    
    if stamina == 100:
        stamina_max=True
    else: 
        stamina_max=False
    if stamina == 0:
        stamina_min=True
    else: 
        stamina_min=False
        
    player, collisions = move(player, movement, tiles)
    
    pygame.draw.rect(screen, (255, 255, 255), player)
    
    stamina_tile = [ pygame.Rect(350,10,x,10) for x in range(stamina+1)]
    
    if(stamina_max!=True):
        stamina_bar = pygame.Rect(350,10,100,10)
        pygame.draw.rect(screen, (255, 255, 255), stamina_bar)
        for tile in stamina_tile:
            pygame.draw.rect(screen, (0, 255, 0), tile)
        
    if collisions["bottom"]:
        if(stamina_max == False):
            stamina += 2
            
        player_y_momentum = 0
    if collisions["right"] or collisions["left"]:
        if(stamina_min == False):
            stamina -= 2
            player_y_momentum = 1
        else:
            player_y_momentum+=0.2
            
        
    for tile in tiles:
        pygame.draw.rect(screen, (255, 0, 0), tile)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                right = True
            if event.key == K_LEFT:
                left = True
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                right = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False

    pygame.display.update()
    mainClock.tick(60)
