import numpy as np
import random
def bombplacing(Board,length,width,Bombs):
    while np.count_nonzero(Board == 10) < Bombs:
        randcolumn = random.randint(0,width-1)
        randrow = random.randint(0,length-1)
        if Board[randrow, randcolumn] == -1:
            Board[randrow, randcolumn] = 10
    return Board
def count(Board,length,width,row,column):
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
        if Board[row-1,column+1] == 10:
            count += 1
    except:
        pass
    try:
        if Board[row,column+1] == 10:
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
                        Board[i-1,j-1] = count(Board,length,width,i-1,j-1)
                    except:
                       pass
                    try:
                        Board[i,j-1] = count(Board,length,width,i,j-1)
                    except:
                        pass
                    try:
                        Board[i+1,j-1] = count(Board,length,width,i+1,j-1)
                    except:
                        pass
                    try:
                        Board[i-1,j] = count(Board,length,width,i-1,j)
                    except:
                        pass
                    try:
                        Board[i+1,j] = count(Board,length,width,i+1,j)
                    except:
                        pass
                    try:
                        Board[i-1,j+1] = count(Board,length,width,i-1,j+1)
                    except:
                        pass
                    try:
                        Board[i,j+1] = count(Board,length,width,i,j+1)
                    except:
                        pass
                    try:
                        Board[i+1,j+1] = count(Board,length,width,i+1,j+1)
                    except:
                        pass
                    Board[i,j] = -2
    return Board
def showboard(Board,length,width,showbombs):
    for i in range(length):
        print("")
        for j in range(width):
            if Board[i,j] == -1: print("⚫", end = "")
            if Board[i,j] == -10 or Board[i,j] == -3: print("🚩", end = "")
            if showbombs and Board[i,j] == 10: print("💣", end = "")
            if showbombs == False and Board[i,j] == 10: print("⚫", end = "")
            if Board[i,j] == 11: print("💥", end = "")
            if Board[i,j] == 0 or Board[i,j] == -2: print("⚪", end = "")
            if Board[i,j] == 1: print(" ❶", end = "")
            if Board[i,j] == 2: print(" ❷", end = "")
            if Board[i,j] == 3: print(" ❸", end = "")
            if Board[i,j] == 4: print(" ❹", end = "")
            if Board[i,j] == 5: print(" ❺", end = "")
            if Board[i,j] == 6: print(" ❻", end = "")
            if Board[i,j] == 7: print(" ❼", end = "")
            if Board[i,j] == 8: print(" ❽", end = "")
    print("")
    pass
def setflag(Board,row,column):
    if Board[row,column] == 10: return -10
    elif Board[row,column] == -10: return 10
    elif Board[row,column] == -1: return -3
    elif Board[row,column] == -3: return -1
    else:
        print("you already uncovered this, why flag it, bruh")
        return Board[row,column]
    
print("Henlo Player!\nwe're gonna play some Minesweeper Today :D\nAre you excited?\nfirst i have a few questions for you tho:")
while True:
    try:
        length = int(input("How long should the board be?\n"))
        width = int(input("How wide should the board be?\n"))
        Bombs = int(input("how many Bombs do you want to be placed?\n"))
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
        firstrow = int(input("In which row do you want to dig first?\n"))
        firstcolumn = int(input("In which column do you want to dig first?\n"))
    except:
        print("Those are not numbers idiot")
        continue
    if firstrow < 1 or firstrow > length or firstcolumn < 1 or firstcolumn > width:
        print("you're out of bounds idiot")
        continue
    break
for i in range(-2,1):
    for j in range(-2,1):
        try:
            Board[firstrow+i,firstcolumn+j] = 0
        except:
            continue
print(Board)
Board = bombplacing(Board,length,width,Bombs)
for i in range(-2,1):
    for j in range(-2,1):
        try:
            Board[firstrow+i,firstcolumn+j] = -1
        except:
            continue
Board[firstrow-1,firstcolumn-1] = 0
print(Board)
Board = uncover(Board,length,width)
print(Board)
showboard(Board,length,width,False)
while np.count_nonzero(Board == -1) + np.count_nonzero(Board == -3) > 0:
    marker = input("do you want to set/remove a mark(m) or to dig somewhere(d)?")
    if marker == "m":
        try:
            row = int(input("which row do you want to set/remove your mark?\n"))
            column = int(input("which column do you want to set/remove your mark?\n"))
            Board[row-1,column-1] = setflag(Board,row-1,column-1)
            showboard(Board,length,width,False)
        except:
            showboard(Board,length,width,False)
            print("Not a valid response, please try again.")
    elif marker == "d":
        row = int(input("in which row do you want to dig?\n"))
        column = int(input("in which column do you want to dig?\n"))
        if Board[row-1,column-1] == 10:
            Board[row-1,column-1] = 11
            showboard(Board,length,width,True)
            print("You have lost you idiot, now go crying")
            break
        elif Board[row-1,column-1] == -3 or Board[row-1,column-1] == -10:
            showboard(Board,length,width,False)
            print("you have to remove the mark before you mine, try again")
        elif Board[row-1,column-1] == -1:
            Board[row-1,column-1] = count(Board,length,width,row-1,column-1)
            showboard(Board,length,width,False)
        else:
            showboard(Board,length,width,False)
            print("you have already uncovered that Field. Please try again.")
else:
    showboard(Board,length,width,True)
    print("you have won the Game, Congratulations!!!")
