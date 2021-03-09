import pygame
import sys

stamina = 100
stamina_max = True
stamina_min = False

stamina_tile = [ pygame.Rect(350,10,x,10) for x in range(stamina+1)]

def verificar_stamina():
    if stamina == 100:
        print(stamina)
        stamina_max=True
    else: 
        stamina_max=False
    if stamina == 0:
        stamina_min=True
    else: 
        stamina_min=False
    