import numpy as np
import random
import pygame
import math
from sys import exit
from enum import IntEnum

import os #Zum mitem nöchste Commmand s display richtig z plaziere
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,27"
ADJACENT_SHIFTS = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
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
    if Board[row,column] != Square.HIDDEN:
        return Board[row,column]
    count = 0
    for shift in ADJACENT_SHIFTS:
        if isvalid(length,width,row+shift[0],column+shift[1]): 
            if Board[row+shift[0],column+shift[1]] == Square.BOMB or Board[row+shift[0],column+shift[1]] == Square.FLAGGED_BOMB: count += 1
    return count

def uncover(Board,length,width):
    while np.count_nonzero(Board == Square.ZERO) > 0:
        for row in range(length):
            for column in range(width):
                if Board[row,column] != Square.ZERO:
                    continue
                for shift in ADJACENT_SHIFTS:
                    if isvalid(length,width,row+shift[0],column+shift[1]): 
                        Board[row+shift[0],column+shift[1]] = count(Board,length,width,row+shift[0],column+shift[1])
                Board[row,column] = Square.ZERO_ALREADY_COUNTED
    return Board
def uncoverall(Board,length,width):
    for i in range(length):
        for j in range(width):
            Board[i,j] = count(Board,length,width,i,j)

def select_surface(Board,tile_x,tile_y,showbombs):
    if Board[tile_x,tile_y] == Square.HIDDEN or Board[tile_x,tile_y] == Square.BOMB and showbombs == False: return hidden_surf
    elif Board[tile_x,tile_y] == Square.BOMB and showbombs == True or Board[tile_x,tile_y] == Square.FLAGGED_BOMB and showbombs == True: return bomb_surf
    elif Board[tile_x,tile_y] == Square.FLAGGED_NON_BOMB or Board[tile_x,tile_y] == Square.FLAGGED_BOMB and showbombs == False: return flag_surf
    elif Board[tile_x,tile_y] == Square.EXPLOSION: return explosion_surf
    elif Board[tile_x,tile_y] == Square.ZERO_ALREADY_COUNTED or Board[tile_x,tile_y] == Square.ZERO: return zero_surf
    elif Board[tile_x,tile_y] == Square.ONE: return one_surf
    elif Board[tile_x,tile_y] == Square.TWO: return two_surf
    elif Board[tile_x,tile_y] == Square.THREE: return three_surf
    elif Board[tile_x,tile_y] == Square.FOUR: return four_surf
    elif Board[tile_x,tile_y] == Square.FIVE: return five_surf
    elif Board[tile_x,tile_y] == Square.SIX: return six_surf
    elif Board[tile_x,tile_y] == Square.SEVEN: return seven_surf
    elif Board[tile_x,tile_y] == Square.EIGHT: return eight_surf
    
def updatescreen(Screen):
    Screen.blit(background_surf,(0,0))
    if losescreen == False and lost: 
        Screen.blit(lost_surf,(0,0))
    if wonscreen == False and won: 
        Screen.blit(won_surf,(0,0))

    for tile_x in range(length):
        for tile_y in range(width):
            if tile_to_pixel(tile_x, tile_y, xmove, ymove, zoom, round(Tile_Size), "x","downright") < 0 or tile_to_pixel(tile_x, tile_y, xmove, ymove, zoom, round(Tile_Size), "y","downright") < 0 or tile_to_pixel(tile_x, tile_y, xmove, ymove, zoom, round(Tile_Size), "x","upleft") > 1280 or tile_to_pixel(tile_x, tile_y, xmove, ymove, zoom, round(Tile_Size), "y","upleft") > 700: continue
            surf = select_surface(Board,tile_x,tile_y,showbombs)
            Screen.blit(surf,tile_to_pixel(tile_x, tile_y, xmove, ymove, zoom, round(Tile_Size), "both","upleft"))    
    if losescreen: 
        Screen.blit(lost_surf,(0,0))
    if wonscreen: 
        Screen.blit(won_surf,(0,0))
    pygame.display.update()

def changeflag(Board,tile_x,tile_y):
    if Board[tile_x,tile_y] == Square.BOMB: Board[tile_x,tile_y] = Square.FLAGGED_BOMB
    elif Board[tile_x,tile_y] == Square.FLAGGED_BOMB: Board[tile_x,tile_y] = Square.BOMB
    elif Board[tile_x,tile_y] == Square.HIDDEN: Board[tile_x,tile_y] = Square.FLAGGED_NON_BOMB
    elif Board[tile_x,tile_y] == Square.FLAGGED_NON_BOMB: Board[tile_x,tile_y] = Square.HIDDEN
    return Board

def isvalid(length,width,row,column):
    if row < length and row >= 0 and column < width and column >= 0 and type(row) == int and type(column) == int: return True
    return False
        
def pixel_to_tile(pixel_x,pixel_y,xmove,ymove,zoom,Tile_Size,x_or_y):
    if x_or_y == "x": return math.floor((pixel_x-xmove//zoom)/Tile_Size)
    return math.floor((pixel_y-ymove//zoom)/Tile_Size)

def tile_to_pixel(tile_x,tile_y,xmove,ymove,zoom,Tile_Size,x_or_y,where):
    if x_or_y == "x":
        if where == "upleft" or where == "downleft": return tile_x*Tile_Size+xmove//zoom
        if where == "upright" or where == "downright": return (tile_x+1)*Tile_Size+xmove//zoom
    
    if x_or_y == "y":
        if where == "upleft" or where == "upright": return tile_y*Tile_Size+ymove//zoom
        if where == "downleft" or where == "downright": return (tile_y+1)*Tile_Size+ymove//zoom
        
    if x_or_y == "both":
        if where == "upleft": return ((tile_x*Tile_Size+xmove//zoom),(tile_y*Tile_Size+ymove//zoom))
        if where == "upright": return (((tile_x+1)*Tile_Size+xmove//zoom),(tile_y*Tile_Size+ymove//zoom))
        if where == "downleft": return ((tile_x*Tile_Size+xmove//zoom),((tile_y+1)*Tile_Size+ymove//zoom))
        if where == "downright": return (((tile_x+1)*Tile_Size+xmove//zoom),((tile_y+1)*Tile_Size+ymove//zoom))
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
    Tile_Size = 1280//length
else: #Breiti macht us wie gross mers chönd mache
    Tile_Size = 700//width
x = length*Tile_Size
y = width*Tile_Size
Board = np.full((length,width),Square.HIDDEN)

pygame.init()
Screen = pygame.display.set_mode((1280,700))
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load("graphics/flag.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

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
    
            tile_x = pixel_to_tile(event.pos[0], event.pos[1], xmove, ymove, zoom, Tile_Size,"x")
            tile_y = pixel_to_tile(event.pos[0], event.pos[1], xmove, ymove, zoom, Tile_Size,"y")
            if isvalid(length, width, tile_x, tile_y) == False: continue
            if pygame.mouse.get_pressed() == (True,False,False):
                if firstmove:
                    firstmove = False
                    for i in range(-1,2):
                        for j in range(-1,2):
                            if isvalid(length,width,tile_x+i,tile_y+j): Board[tile_x+i,tile_y+j] = Square.ZERO     
                    
                    Board = bombplacing(Board,length,width,Bombs)
                    
                    for i in range(-1,2):
                        for j in range(-1,2):
                                if isvalid(length,width,tile_x+i,tile_y+j): Board[tile_x+i,tile_y+j] = Square.HIDDEN
                    
                    Board[tile_x,tile_y] = Square.ZERO
                    Board = uncover(Board,length,width)
    
                elif Board[tile_x,tile_y] == Square.BOMB or Board[tile_x,tile_y] == Square.FLAGGED_BOMB:
                    Board[tile_x,tile_y] = Square.EXPLOSION
                    lost = True
                    showbombs = True
                    losescreen = True
                    
            
                else:
                    if Board[tile_x,tile_y] == Square.FLAGGED_NON_BOMB: Board[tile_x,tile_y] = Square.HIDDEN
                    Board[tile_x,tile_y] = count(Board,length,width,tile_x,tile_y)
                    Board = uncover(Board,length,width)
    
            if pygame.mouse.get_pressed() == (False,False,True) and firstmove == False: Board = changeflag(Board,tile_x,tile_y)
    
        if event.type == pygame.MOUSEWHEEL:
               if event.y > 0:
                   zoom *= 0.9
                   Tile_Size /= 0.9
               elif event.y < 0:
                   zoom /= 0.9
                   Tile_Size *= 0.9
        
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
    if pressed[pygame.K_s] and width*round(Tile_Size)+ymove//zoom > 700:
       ymove -= 4
       if width*round(Tile_Size)+ymove//zoom < 700: 
           ymove = (700-width*round(Tile_Size))*zoom
    if pressed[pygame.K_w] and ymove < 0:
       ymove += 4
    if pressed[pygame.K_d] and length*round(Tile_Size)+xmove//zoom > 1280:
       xmove -= 4
       if length*round(Tile_Size)+xmove//zoom < 1280: #Falls die -4 zu viel gsi sind
           xmove = (1280-length*round(Tile_Size))*zoom
    if pressed[pygame.K_a] and xmove < 0:
       xmove += 4
    if pressed[pygame.K_q]:
        zoom *= 0.95
        Tile_Size /= 0.95
    if pressed[pygame.K_e]:
        zoom /= 0.95
        Tile_Size *= 0.95

    
    background_surf = pygame.transform.scale(pygame.image.load("graphics/background.png").convert(), (1280,700))
    lost_surf = pygame.transform.scale(pygame.image.load("graphics/lost.png").convert(), (1280,700))
    won_surf = pygame.transform.scale(pygame.image.load("graphics/won.png").convert(), (1280,700))
    
    hidden_surf = pygame.transform.scale(pygame.image.load("graphics/hidden.png").convert(), (Tile_Size,Tile_Size)) #Erstellt es surface für es image und scaleds grad, damits ufd grössi vom Display apasst wird
    flag_surf = pygame.transform.scale(pygame.image.load("graphics/flag.png").convert(), (Tile_Size,Tile_Size))
    bomb_surf = pygame.transform.scale(pygame.image.load("graphics/bomb.png").convert(), (Tile_Size,Tile_Size))
    explosion_surf = pygame.transform.scale(pygame.image.load("graphics/explosion.png").convert(), (Tile_Size,Tile_Size))
    zero_surf = pygame.transform.scale(pygame.image.load("graphics/zero.png").convert(), (Tile_Size,Tile_Size))
    one_surf = pygame.transform.scale(pygame.image.load("graphics/one.png").convert(), (Tile_Size,Tile_Size))
    two_surf = pygame.transform.scale(pygame.image.load("graphics/two.png").convert(), (Tile_Size,Tile_Size))
    three_surf = pygame.transform.scale(pygame.image.load("graphics/three.png").convert(), (Tile_Size,Tile_Size))
    four_surf = pygame.transform.scale(pygame.image.load("graphics/four.png").convert(), (Tile_Size,Tile_Size))
    five_surf = pygame.transform.scale(pygame.image.load("graphics/five.png").convert(), (Tile_Size,Tile_Size))
    six_surf = pygame.transform.scale(pygame.image.load("graphics/six.png").convert(), (Tile_Size,Tile_Size))
    seven_surf = pygame.transform.scale(pygame.image.load("graphics/seven.png").convert(), (Tile_Size,Tile_Size))
    eight_surf = pygame.transform.scale(pygame.image.load("graphics/eight.png").convert(), (Tile_Size,Tile_Size))
    
    if np.count_nonzero(Board == Square.HIDDEN) + np.count_nonzero(Board == Square.FLAGGED_NON_BOMB) == 0 and won == False and lost == False:
        won = True
        wonscreen = True
        showbombs = True
        
    updatescreen(Screen)
    
    clock.tick(60)