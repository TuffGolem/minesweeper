import numpy as np
import random
def bombplacing(Board,length,width,Bombs):
    while np.count_nonzero(Board == 10) < Bombs:
        randcolumn = random.randint(0,width-1)
        randrow = random.randint(0,length-1)
        if Board[randrow, randcolumn] == -1: 
            Board[randrow, randcolumn] = 10
    return Board
def count(Board,row,column):
    if Board[row,column] != -1:
        return Board[row,column]
    count = 0
    try:
        if Board[row-1,column-1] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row,column-1] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row+1,column-1] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row-1,column] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row+1,column] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row+1,column-1] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row+1,column] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row+1,column+1] == 10:
            count += 1
    except:
        pass
    return count
def uncover(Board,length,width):
    while np.count_nonzero(Board == 0) > 0:
        for i in range(length):
            for j in range(width):
                if Board[i,j] == 0:
                    try:
                        Board[i-1,j-1] = count(Board,i-1,j-1)
                    except:
                        pass
                    try:
                        Board[i,j-1] = count(Board,i,j-1)
                    except:
                        pass
                    try:
                        Board[i+1,j-1] = count(Board,i+1,j-1)
                    except:
                        pass
                    try:
                        Board[i-1,j] = count(Board,i-1,j)
                    except:
                        pass
                    try:
                        Board[i+1,j] = count(Board,i+1,j)
                    except:
                        pass
                    try:
                        Board[i-1,j+1] = count(Board,i-1,j+1)
                    except:
                        pass
                    try:
                        Board[i,j+1] = count(Board,i,j+1)
                    except:
                        pass
                    try:
                        Board[i+1,j+1] = count(Board,i+1,j+1)
                    except:
                        pass
                    Board[i,j] = -2
    return Board
def showboard(Board,length,width,showbombs):
    for i in range(length):
        print("")
        for j in range(width):
            if Board[i,j] == -1: print("⚫", end = "")
            if Board[i,j] == 0 or Board[i,j] == -2: print("⚪", end = "")
            if Board[i,j] == 1: print(" ❶", end = "")
            if Board[i,j] == 2: print(" ❷", end = "")
            if Board[i,j] == 3: print(" ❸", end = "")
            if Board[i,j] == 4: print(" ❹", end = "")
            if Board[i,j] == 5: print(" ❺", end = "")
            if Board[i,j] == 6: print(" ❻", end = "")
            if Board[i,j] == 7: print(" ❼", end = "")
            if Board[i,j] == 8: print(" ❽", end = "")
            if showbombs and Board[i,j] == 10: print("💣", end = "")
            if showbombs == False and Board[i,j] == 10: print("⚫", end = "")
    print("")
    pass
print("Henlo Player!\nwe're gonna play some Minesweeper Today :D\nAre you excited?\nfirst i have a few questions for you tho:")
while True:
    try:
        length = int(input("How long should the board be?\n"))
        width = int(input("How wide should the board be?\n"))
        Bombs = int(input("how many Bombs do you want to be placed\n"))
    except:
        print("Those are not numbers you idiot")
        continue
    if 1 > length or 1 > width or length*width > 5000 or Bombs >= length*width or Bombs < 0: 
        print("this won't work idiot")
        continue
    break
Board = np.zeros((length,width))
Board[Board == 0] = -1
print("this is the Board:")
showboard(Board,length,width,True)
while True:
    try:
        firstrow = int(input("Which row do you want to dig first?\n"))
        firstcolumn = int(input("which column do you want to dig first"))
    except:
        print("Those are not numbers idiot")
        continue
    if firstrow < 1 or firstrow > length or firstcolumn < 1 or firstcolumn > width:
        print("you're out of bounds idiot")
        continue
    break
Board[firstrow-1,firstcolumn-1] = 0
Board = bombplacing(Board,length,width,Bombs)
Board[firstrow-1,firstcolumn-1] = count(Board,firstrow-1,firstcolumn-1)
Board = uncover(Board,length,width)
showboard(Board,length,width,True)
