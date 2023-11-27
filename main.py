import numpy as np
import random

class Minesweeper():
    def __init__(self, length, width, bombs):
        self.length = length
        self.width = width
        self.bombs = bombs
        self.flags = bombs

    def board(self):
        board = np.zeros((self.length, self.width)) 
        for i in range(self.bombs):
            x = random.randint(0 , self.length-1) 
            y = random.randint(0 , self.width-1 ) 
            board[x][y] = -1
            self.original = board.copy() 
        return board

    def lose(self, board, row, column):
        if board[row, column] == -1:
            return True
        
    
    def dig(self, board, row, column):
        board[row, column] = -2
        return board
    
    def flag(self, board, row, column):
        board[row, column] = -3
        return board 

    def remove_flag(self, board, row, column):
        board[row, column] = self.original[row, column]
        print(self.original)
        print(board)
        return board
    def create_user_board(self, board):
        user = np.ndarray.tolist(np.zeros((self.length, self.width)))

        for row in range(self.length):
            for col in range(self.width):
                if board[row][col] == -1 or board[row, col] == 0:
                    user[row][col] = "O"

                elif board[row][col] == -3:
                    user[row][col] = "F"

                elif board[row][col] == -2: 
                    user[row][col] = "D"
        return user

    def count_bombs(self, board, row, col):
        boardl, boardw = board.shape
        print(board)
        surrounding = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        counter = 0
        for x, y in surrounding:
            new_row = row + x
            new_col = col + y
            if new_row != -1 and new_col != -1 and new_row < boardl and new_col < boardw:
                tile = board[new_row][new_col]
                print(tile)
                if tile == -1:
                    counter += 1
        board[row][col] = counter
        return board



bombs = 3 
game = Minesweeper(3, 3, bombs)
board = game.board()
flags = bombs

game.count_bombs(board, 1, 1)
print(board)

# while True:
#     user = game.create_user_board(board)
#     for line in user:
#         print(line)
#     action = input("dig (d) | flag (f) | remove flag (r): ")
#     row = int(input("row: "))
#     col = int(input("col: "))
#
#     if action == "d":
#         finished = game.lose(board, row, col)
#         if finished:
#             break
#         board = game.dig(board, row, col)
#     elif action == "f": 
#         if flags > 0:
#             board = game.flag(board, row, col)
#             print(f"you have {flags} flags left")
#             flags -= 1
#     elif action == "r":
#         if board[row, col] == -3:
#             board = game.remove_flag(board, row, col)
#             flags += 1
#             print(f"you have {flags} flags left")
#         else:
#             print("there is no flag on that tile")
#
# print("KABOOM!! you lost noob")
#
#     
