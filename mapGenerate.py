import random

map_x = 10
map_y = 10

mapa = []

for x in range(map_x):
    mapa.append([])
    for y in range(map_y):
        print(x,y)
        if(y!=0):
            if(mapa[x][y-1] == 0):
                nsramdon = [5,3]
                if(x!=0):
                    if(mapa[x-1][y] == 5):
                        nsramdon = [3]
                        nramdon = random.randint(0,1)
                        mapa[x].append(3)
                        break
                    else:
                        mapa[x].append(5)
                else:
                    
                    nramdon = nsramdon[random.randint(0,2)]
                    mapa[x].append(nramdon)

            if(mapa[x][y-1] == 5):
                nsramdon = [7,6]
                nramdon = nsramdon[random.randint(0,2)]
                mapa[x].append(nramdon)
            if(mapa[x][y-1] == 7):
                nsramdon = [7,6]
                nramdon = nsramdon[random.randint(0,2)]
                mapa[x].append(nramdon)
        else:
            nramdon = random.randint(0,8)
            mapa[x].append(nramdon)

        
print(mapa)