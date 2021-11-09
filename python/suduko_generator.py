# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 12:23:39 2021

@author: keith
@title: suduko generator
@activity: generates board
@activity: initialise with random values taken from list
@activity: solves suduko based on those values
@@activity: writes to txt file
"""

import math
import numpy as np
from random import shuffle, randint

## creation
def create_square(arr, root):
    shuffle(arr)
    return np.array(arr).reshape(root, root)

def start_board(arr):
    board = np.zeros((len(arr),len(arr)), dtype=np.int)
    position = 0
    root = math.floor(math.sqrt(len(arr)))
    for x in range(root):
        square = create_square(arr,root)
        board[position:position+root, position:position+root] = square
        position += root
    return board

## checks
def check_row(grid, num, xpos):
    if num in grid[xpos,:]: return False
    else: return True
    
def check_col(grid, num, ypos):
    if num in grid[:,ypos]: return False
    else: return True

def check_square(grid, num, xpos, ypos, root):
    corner_x = math.floor(xpos / root) * root
    corner_y = math.floor(ypos / root) * root
    
    square = grid[corner_x:corner_x+root, corner_y:corner_y+root].flatten()
    
    if num in square: return False
    else: return True
    
def check(grid, num, xpos, ypos):
    root = math.floor(math.sqrt(len(grid)))
    row = check_row(grid, num, xpos)
    col = check_col(grid, num, ypos)
    sq = check_square(grid, num, xpos, ypos, root)
    if row and col and sq:
        return True
    else: return False
    
    
## solve
def find_empty(grid):
    for x in range(len(grid)):
        for y in range(len(grid)):
            if grid[x,y] == 0:
                return (x,y)
    return None
    
    
def solve(grid):
    next_empty = find_empty(grid)
    if not next_empty:
        return True
    else:
        x, y = next_empty
    for number in range(1, len(grid) + 1):
        if check(grid, number, x, y):
            grid[x,y] = number
            if solve(grid):
                return True
            grid[x,y] = 0
    return False

## create player board
def create_player_board(grid, to_be_removed):
    while to_be_removed > 0:
        x = randint(0, len(grid)-1)
        y = randint(0, len(grid)-1)
        if grid[x, y] != 0:
            grid[x,y] = 0
            to_be_removed -= 1
    return grid
    
                    
## main - run functions and write to file
nums = [1,2,3,4,5,6,7,8,9]
remove = 55
Number_to_generate = 10

for x in range(Number_to_generate):
    game = start_board(nums)
    solve(game)
    solved = np.copy(game)
    player_board = create_player_board(game, remove)
    
    txt_solved = np.array2string(solved, separator=',')
    txt_player = np.array2string(player_board, separator=',')
    
    with open("grids.txt", "a+") as file:
            file.seek(0)
            data = file.read(100)
            if len(data) > 0 :
                file.write("\n")
            file.write(f"#solved {x} \n")
            file.write(txt_solved)
            file.write("\n")
            file.write(f"#player {x} \n")
            file.write(txt_player)
            file.write("\n")
        
    
print("done")




    
