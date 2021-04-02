import random

map_x = 10
map_y = 10

mapa = []

for x in range(map_x):
    mapa.append([])
    n_possibles = []
    for y in range(map_y):
        if(x==0):
            mapa[x].append(0)
        else:
            n_possibles = [0,5,7,6]
            if(y==0):
                n_possibles = [0,5,7,6]
                if(mapa[x-1][y]== 5):
                    n_possibles = [3]
                if(mapa[x-1][y]==7):
                    n_possibles = [1]
                if(mapa[x-1][y]==6):
                    n_possibles = [2]
            else:
                if(mapa[x-1][y]==1):
                    n_possibles = [1]
                if(mapa[x-1][y]==5):
                    n_possibles = [3]
                if(mapa[x-1][y]==7 and mapa[x][y-1]!=0):
                    n_possibles = [1]
                if(mapa[x-1][y]==7 and mapa[x][y-1]==0):
                    n_possibles = [1]
                if(mapa[x-1][y]==6 or mapa[x-1][y]==2):
                    n_possibles = [2]
                if(mapa[x-1][y]==3):
                    n_possibles = [0]
                if(mapa[x][y-1]==7):
                    n_possibles = [6,7]
                if(mapa[x][y-1]==6 or mapa[x][y-1]==2):
                    n_possibles = [0]
                if(mapa[x][y-1]==5):
                    n_possibles = [7,6]


            mapa[x].append(n_possibles[random.randint(0,len(n_possibles)-1)])

        
[print(x) for x in mapa]