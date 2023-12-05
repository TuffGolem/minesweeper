import numpy as np
import random
import pygame
from sys import exit

import os #Zum mitem nöchste Commmand s display richtig z plaziere
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,27"

def bombplacing(Board,length,width,Bombs):
    while np.count_nonzero(Board == 10) < Bombs:
        randcolumn = random.randint(0,width-1)
        randrow = random.randint(0,length-1)
        if Board[randrow, randcolumn] == -1:
            Board[randrow, randcolumn] = 10
    return Board

def count(Board,length,width,row,column):
    count = 0
    
    if Board[row,column] != -1 and Board[row,column] != -3:
        return Board[row,column]
    
    if row-1 >= 0 and column-1 >= 0:
        if Board[row-1,column-1] == 10 or Board[row-1,column-1] == -10:
            count += 1
    if column-1 >= 0:
        if Board[row,column-1] == 10 or Board[row,column-1] == -10:
            count += 1
    if row+1 < length and column-1 >= 0:
        if Board[row+1,column-1] == 10 or Board[row+1,column-1] == -10: 
            count += 1
    if row-1 >= 0:
        if Board[row-1,column] == 10 or Board[row-1,column] == -10:
            count += 1
    if row+1 < length:
        if Board[row+1,column] == 10 or Board[row+1,column] == -10: 
            count += 1
    if row-1 >= 0 and column+1 < width:
        if Board[row-1,column+1] == 10 or Board[row-1,column+1] == -10:
            count += 1
    if column+1 < width:
        if Board[row,column+1] == 10 or Board[row,column+1] == -10:
            count += 1
    if row+1 < length and column+1 < width:
        if Board[row+1,column+1] == 10 or Board[row+1,column+1] == -10:
            count += 1
            
    return count

def uncover(Board,length,width):
    while np.count_nonzero(Board == 0) > 0:
        for i in range(length):
            for j in range(width):
                if Board[i,j] == 0:
                    if i-1 >= 0 and j-1 >= 0:
                        Board[i-1,j-1] = count(Board,length,width,i-1,j-1)
                    if j-1 >= 0:
                        Board[i,j-1] = count(Board,length,width,i,j-1)
                    if j-1 >= 0 and i+1 < length:
                        Board[i+1,j-1] = count(Board,length,width,i+1,j-1)
                    if i-1 >= 0:
                        Board[i-1,j] = count(Board,length,width,i-1,j)
                    if i+1 < length:
                        Board[i+1,j] = count(Board,length,width,i+1,j)
                    if i-1 >= 0 and j+1 < width:
                        Board[i-1,j+1] = count(Board,length,width,i-1,j+1)
                    if j+1 < width:
                        Board[i,j+1] = count(Board,length,width,i,j+1)
                    if i+1 < length and j+1 < width:
                        Board[i+1,j+1] = count(Board,length,width,i+1,j+1)
                    Board[i,j] = -2
    return Board
    
    
print("\nHello Player! Welcome to my Minesweeper!\n")
while True:
    try:
        length = int(input("How long should the board be(3-100)?\n"))
        width = int(input("How wide should the board be(3-100)?\n"))
        Bombs = int(input(f"how many Bombs do you want to be placed(max {length*width-9})?\n"))
    except:
        print("Try again!")
        continue
    if 3 > length or 3 > width or length > 100 or width > 100 or Bombs >= length*width-8 or Bombs < 0: 
        print("Try again!")
        continue
    break
if width > length:
    changer = length
    length = width
    width = changer

#Breite und Höhe des Screens festlegen sowie Brett(für Programm) definieren
if length/width > 1280/690: #Längi/breiti isch grösser als die vom Laptop > Längi isch maximalfaktor
    k = 1280//length
else: #Breiti macht us wie gross mers chönd mache
    k = 690//width
x = length*k
y = width*k
Board = np.zeros((length,width))
Board[Board == 0] = -1
    
pygame.init()
Screen = pygame.display.set_mode((1280,690))
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("graphics/flag.png")
pygame.display.set_icon(icon)

Tile_Size = (k,k)
firstmove = True
lost = False
showbombs = False
won = False
ymove = 0
xmove = 0
zoom = 1
while True:
    #Screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and lost == False and won == False: #Damit mer nüt me chan mache usser umeluege am schluss
            
            tile = (int(event.pos[0]*zoom-xmove))//k,int((event.pos[1]*zoom-ymove)//k)
            print(tile)
            
            if pygame.mouse.get_pressed() == (True,False,False):
                if firstmove:
                    firstmove = False
                    for i in range(-1,2):
                        for j in range(-1,2):
                            try:
                                Board[tile[0]+i,tile[1]+j] = 0
                            except:
                                continue
                            
                    Board = bombplacing(Board,length,width,Bombs)
                    
                    for i in range(-1,2):
                        for j in range(-1,2):
                            try:
                                Board[tile[0]+i,tile[1]+j] = -1
                            except:
                                continue

                    Board[tile[0],tile[1]] = 0    
                    Board = uncover(Board,length,width)
    
                elif Board[tile[0],tile[1]] == 10 or Board[tile[0],tile[1]] == -10:
                    Board[tile[0],tile[1]] = 11
                    lost = True
                    showbombs = True
                    print("you have lost the Game! Get good")
            
                else:
                    Board[tile[0],tile[1]] = count(Board,length,width,tile[0],tile[1])
                    Board = uncover(Board,length,width)
    
            if pygame.mouse.get_pressed() == (False,False,True) and firstmove == False:
                if Board[tile[0],tile[1]] == 10: Board[tile[0],tile[1]] = -10
                elif Board[tile[0],tile[1]] == -10: Board[tile[0],tile[1]] = 10
                elif Board[tile[0],tile[1]] == -1: Board[tile[0],tile[1]] = -3
                elif Board[tile[0],tile[1]] == -3: Board[tile[0],tile[1]] = -1
    
    
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_s]:# and ymove > -width*k*(1-zoom) and y/zoom-ymove > 690:
       ymove -= 4
    if pressed[pygame.K_w]:# and ymove < 0:
       ymove += 4
    if pressed[pygame.K_d]:# and xmove > -length*k*(1-zoom) and x/zoom-xmove > 1280:
       xmove -= 4
    if pressed[pygame.K_a]:# and xmove < 0:
       xmove += 4
    if pressed[pygame.K_q]:
        zoom *= 0.99
        Tile_Size = (Tile_Size[0]/0.99,Tile_Size[1]/0.99)
    if pressed[pygame.K_e]:# and zoom < -xmove/1280-1 and zoom > -ymove/690-1:
        zoom /= 0.99
        Tile_Size = (Tile_Size[0]*0.99,Tile_Size[1]*0.99)
    
    background_surf = pygame.transform.scale(pygame.image.load("graphics/background.png").convert(), (1280,690))
    
    hidden_surf = pygame.transform.scale(pygame.image.load("graphics/hidden.png").convert(), Tile_Size) #Erstellt es surface für es image und scaleds grad, damits ufd grössi vom Display apasst wird
    flag_surf = pygame.transform.scale(pygame.image.load("graphics/flag.png").convert(), Tile_Size)
    bomb_surf = pygame.transform.scale(pygame.image.load("graphics/bomb.png").convert(), Tile_Size)
    explosion_surf = pygame.transform.scale(pygame.image.load("graphics/explosion.png").convert(), Tile_Size)
    zero_surf = pygame.transform.scale(pygame.image.load("graphics/zero.png").convert(), Tile_Size)
    one_surf = pygame.transform.scale(pygame.image.load("graphics/one.png").convert(), Tile_Size)
    two_surf = pygame.transform.scale(pygame.image.load("graphics/two.png").convert(), Tile_Size)
    three_surf = pygame.transform.scale(pygame.image.load("graphics/three.png").convert(), Tile_Size)
    four_surf = pygame.transform.scale(pygame.image.load("graphics/four.png").convert(), Tile_Size)
    five_surf = pygame.transform.scale(pygame.image.load("graphics/five.png").convert(), Tile_Size)
    six_surf = pygame.transform.scale(pygame.image.load("graphics/six.png").convert(), Tile_Size)
    seven_surf = pygame.transform.scale(pygame.image.load("graphics/seven.png").convert(), Tile_Size)
    eight_surf = pygame.transform.scale(pygame.image.load("graphics/eight.png").convert(), Tile_Size)
    
    if np.count_nonzero(Board == -1) + np.count_nonzero(Board == -3) == 0 and won == False:
        print("You Have won the Game, Congratulations!")
        won = True
        showbombs = True
    
    Screen.blit(background_surf,(0,0))
    for i in range(length):
        for j in range(width):
            if Board[i,j] == -1 or Board[i,j] == 10 and showbombs == False: Screen.blit(hidden_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 10 and showbombs == True or Board[i,j] == -10 and showbombs == True: Screen.blit(bomb_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == -3 or Board[i,j] == -10 and showbombs == False: Screen.blit(flag_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 11: Screen.blit(explosion_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == -2 or Board[i,j] == 0: Screen.blit(zero_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 1: Screen.blit(one_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 2: Screen.blit(two_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 3: Screen.blit(three_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 4: Screen.blit(four_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 5: Screen.blit(five_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 6: Screen.blit(six_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 7: Screen.blit(seven_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
            if Board[i,j] == 8: Screen.blit(eight_surf,((i*k+xmove)//zoom,(j*k+ymove)//zoom))
    pygame.display.update()