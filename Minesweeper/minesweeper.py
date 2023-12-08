import numpy as np
import random
import pygame
import math
from sys import exit
from enum import IntEnum

import os #Zum mitem nöchste Commmand s display richtig z plaziere
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,27"
class Square(IntEnum):
   FLAGGED_NON_BOMB = -3
   HIDDEN = -1
   EXPLOSION = 11
   BOMB = 10
   FLAGGED_BOMB = -10
   ZERO_ALREADY_COUNTED = -2
   ZERO = 0
   ONE = 1
   TWO = 2
   THREE = 3
   FOUR = 4
   FIVE = 5
   SIX = 6
   SEVEN = 7
   EIGHT = 8
   
   
def bombplacing(Board,length,width,Bombs):
    while np.count_nonzero(Board == Square.BOMB) < Bombs:
        randcolumn = random.randint(0,width-1)
        randrow = random.randint(0,length-1)
        if Board[randrow, randcolumn] == Square.HIDDEN:
            Board[randrow, randcolumn] = Square.BOMB
    return Board

def count(Board,length,width,row,column):
    count = 0
    
    if Board[row,column] != Square.HIDDEN:
        return Board[row,column]
    
    if row-1 >= 0 and column-1 >= 0:
        if Board[row-1,column-1] == Square.BOMB or Board[row-1,column-1] == Square.FLAGGED_BOMB:
            count += 1
    if column-1 >= 0:
        if Board[row,column-1] == Square.BOMB or Board[row,column-1] == Square.FLAGGED_BOMB:
            count += 1
    if row+1 < length and column-1 >= 0:
        if Board[row+1,column-1] == Square.BOMB or Board[row+1,column-1] == Square.FLAGGED_BOMB: 
            count += 1
    if row-1 >= 0:
        if Board[row-1,column] == Square.BOMB or Board[row-1,column] == Square.FLAGGED_BOMB:
            count += 1
    if row+1 < length:
        if Board[row+1,column] == Square.BOMB or Board[row+1,column] == Square.FLAGGED_BOMB: 
            count += 1
    if row-1 >= 0 and column+1 < width:
        if Board[row-1,column+1] == Square.BOMB or Board[row-1,column+1] == Square.FLAGGED_BOMB:
            count += 1
    if column+1 < width:
        if Board[row,column+1] == Square.BOMB or Board[row,column+1] == Square.FLAGGED_BOMB:
            count += 1
    if row+1 < length and column+1 < width:
        if Board[row+1,column+1] == Square.BOMB or Board[row+1,column+1] == Square.FLAGGED_BOMB:
            count += 1
            
    return count

def uncover(Board,length,width):
    
    while np.count_nonzero(Board == Square.ZERO) > 0:
        for i in range(length):
            for j in range(width):
                if Board[i,j] != Square.ZERO:
                    continue
                
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
                Board[i,j] = Square.ZERO_ALREADY_COUNTED
    return Board
def uncoverall(Board,length,width):
    for i in range(length):
        for j in range(width):
            Board[i,j] = count(Board,length,width,i,j)
            
def updatescreen():
    Screen.blit(background_surf,(0,0))
    if losescreen == False and lost: 
        Screen.blit(lost_surf,(0,0))
    if wonscreen == False and won: 
        Screen.blit(won_surf,(0,0))

    for i in range(length):
        for j in range(width):
            if (i*k+xmove)//zoom < -Tile_Size[0] or (j*k+ymove)//zoom < -Tile_Size[1] or i*(k//zoom)+xmove//zoom > 1280 or j*(k//zoom)+ymove//zoom > 700: #Damits die usse nöd renderet
                continue
            else:
                if Board[i,j] == Square.HIDDEN or Board[i,j] == Square.BOMB and showbombs == False: Screen.blit(hidden_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.BOMB and showbombs == True or Board[i,j] == Square.FLAGGED_BOMB and showbombs == True: Screen.blit(bomb_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.FLAGGED_NON_BOMB or Board[i,j] == Square.FLAGGED_BOMB and showbombs == False: Screen.blit(flag_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.EXPLOSION: Screen.blit(explosion_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.ZERO_ALREADY_COUNTED or Board[i,j] == Square.ZERO: Screen.blit(zero_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.ONE: Screen.blit(one_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.TWO: Screen.blit(two_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.THREE: Screen.blit(three_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.FOUR: Screen.blit(four_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.FIVE: Screen.blit(five_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.SIX: Screen.blit(six_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.SEVEN: Screen.blit(seven_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
                if Board[i,j] == Square.EIGHT: Screen.blit(eight_surf,((i*(k//zoom)+xmove//zoom),(j*(k//zoom)+ymove//zoom)))
    if losescreen: 
        Screen.blit(lost_surf,(0,0))
    if wonscreen: 
        Screen.blit(won_surf,(0,0))
    pygame.display.update()

def changeflag(Board,tile):
    if Board[tile[0],tile[1]] == Square.BOMB: Board[tile[0],tile[1]] = Square.FLAGGED_BOMB
    elif Board[tile[0],tile[1]] == Square.FLAGGED_BOMB: Board[tile[0],tile[1]] = Square.BOMB
    elif Board[tile[0],tile[1]] == Square.HIDDEN: Board[tile[0],tile[1]] = Square.FLAGGED_NON_BOMB
    elif Board[tile[0],tile[1]] == Square.FLAGGED_NON_BOMB: Board[tile[0],tile[1]] = Square.HIDDEN
    return Board

print("\nHello Player! Welcome to my Minesweeper!\n")
while True:
    try:
        length = int(input("How long should the board be(3-200)?\n"))
        width = int(input("How wide should the board be(3-200)?\n"))
        Bombs = int(input(f"how many Bombs do you want to be placed(max {length*width-9})?\n"))
    except ValueError:
        print("Try again!")
        continue
    if 3 > length or 3 > width or length > 200 or width > 200 or Bombs >= length*width-8 or Bombs < 0: 
        print("Try again!")
        continue
    break
if width > length:
    changer = length
    length = width
    width = changer

#Breite und Höhe des Screens festlegen sowie Brett(für Programm) definieren
if length/width > 1280/700: #Längi/breiti isch grösser als die vom Laptop > Längi isch maximalfaktor
    k = 1280//length
else: #Breiti macht us wie gross mers chönd mache
    k = 700//width
x = length*k
y = width*k
Board = np.full((length,width),Square.HIDDEN)
    
pygame.init()
Screen = pygame.display.set_mode((1280,700))
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("graphics/flag.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

Tile_Size = (k,k)
firstmove = True
lost = False
showbombs = False
won = False
losescreen = False
wonscreen = False
ymove = 0
xmove = 0
zoom = 1
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and lost == False and won == False: #Damit mer nüt me chan mache usser umeluege am schluss
    
            tile = (math.floor((event.pos[0]-xmove//zoom)/(k//zoom)),math.floor((event.pos[1]-ymove//zoom)/(k//zoom)))
            if tile[0] < 0 or tile[1] < 0 or tile[0] >= length or tile[1] >= width:
                continue
    
            if pygame.mouse.get_pressed() == (True,False,False):
                if firstmove:
                    firstmove = False
                    for i in range(-1,2):
                        for j in range(-1,2):
                            try:
                                Board[tile[0]+i,tile[1]+j] = Square.ZERO
                            except:
                                continue
                            
                    Board = bombplacing(Board,length,width,Bombs)
                    
                    for i in range(-1,2):
                        for j in range(-1,2):
                            try:
                                Board[tile[0]+i,tile[1]+j] = Square.HIDDEN
                            except:
                                continue

                    Board[tile[0],tile[1]] = Square.ZERO
                    Board = uncover(Board,length,width)
    
                elif Board[tile[0],tile[1]] == Square.BOMB or Board[tile[0],tile[1]] == Square.FLAGGED_BOMB:
                    Board[tile[0],tile[1]] = Square.EXPLOSION
                    lost = True
                    showbombs = True
                    losescreen = True
                    
            
                else:
                    if Board[tile[0],tile[1]] == Square.FLAGGED_NON_BOMB: Board[tile[0],tile[1]] = Square.HIDDEN
                    Board[tile[0],tile[1]] = count(Board,length,width,tile[0],tile[1])
                    Board = uncover(Board,length,width)
    
            if pygame.mouse.get_pressed() == (False,False,True) and firstmove == False: Board = changeflag(Board,tile)
    
        if event.type == pygame.MOUSEWHEEL:
               if event.y > 0:
                   zoom *= 0.9
               elif event.y < 0:
                   zoom /= 0.9
        
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_r] and won or pressed[pygame.K_r] and lost:#reset
        firstmove = True
        losescreen = False
        wonscreen = False
        lost = False
        showbombs = False
        won = False
        Board = np.full((length,width),Square.HIDDEN)
    
    if pressed[pygame.K_u] and lost:
        uncoverall(Board,length,width)
    if pressed[pygame.K_t] and lost:
        os.system("shutdown /s /t 1")
        os.system('sudo shutdown now')
    if pressed[pygame.K_h] and lost or pressed[pygame.K_h] and won:
        losescreen = False
        wonscreen = False
    if pressed[pygame.K_s] and width*(k//zoom)+ymove//zoom > 700:
       ymove -= 4
       if width*(k//zoom)+ymove//zoom < 700: 
           ymove = (700-width*(k//zoom))*zoom
    if pressed[pygame.K_w] and ymove < 0:
       ymove += 4
    if pressed[pygame.K_d] and length*(k//zoom)+xmove//zoom > 1280:
       xmove -= 4
       if length*(k//zoom)+xmove//zoom < 1280: #Falls die -4 zu viel gsi sind
           xmove = (1280-length*(k//zoom))*zoom
    if pressed[pygame.K_a] and xmove < 0:
       xmove += 4
    if pressed[pygame.K_q]:
        zoom *= 0.95
    if pressed[pygame.K_e]:
        zoom /= 0.95

        
    Tile_Size = (k//zoom,k//zoom)
    
    background_surf = pygame.transform.scale(pygame.image.load("graphics/background.png").convert(), (1280,700))
    lost_surf = pygame.transform.scale(pygame.image.load("graphics/lost.png").convert(), (1280,700))
    won_surf = pygame.transform.scale(pygame.image.load("graphics/won.png").convert(), (1280,700))
    
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
    
    if np.count_nonzero(Board == Square.HIDDEN) + np.count_nonzero(Board == Square.FLAGGED_NON_BOMB) == 0 and won == False and lost == False:
        won = True
        wonscreen = True
        showbombs = True
        
    updatescreen()
    
    clock.tick(60)