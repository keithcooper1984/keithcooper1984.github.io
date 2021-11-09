# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 13:30:34 2021

@author: keith
@title: solvable suduko
@activity: read solved suduko from text file
@activity: remove a set amount of digits
@activity: check for unique solution
@@activity: write solved suduko and solvalbe suduko to txt file
"""

import numpy as np
from random import randint

remove = 55



def solve():
    global game
    global grid
    global count
    #print(game)
    length = len(game)
    for x in range(length):
        for y in range(length):
            if game[x,y] == 0:
                for number in range(1, length + 1):
                    if suduko_generator.check(number, x, y):
                        game[x,y] = number
                        solve()
                        game[x,y] = 0
                        print(game)
                return "hello"
    count += 1
    print(game)
    print(count)

with open("grids.txt", "r") as file:
    lines = file.readlines()
    
    grid = []
    
    for line in lines:
        #print(line)
        new_line = ",".join(e for e in line if e.isdigit())
        lst = [int(x) for x in line if x.isdigit()]
        
        
        if new_line == "":
            break
        grid.append(lst)
        
    np_grid = np.array(grid)
    
    game = np.copy(np_grid)
    
    togo = remove
    
    while togo > 0:
        x = randint(0, len(grid)-1)
        y = randint(0, len(grid)-1)
        if game[x, y] != 0:
            game[x,y] = 0
            togo -= 1

    count = 0
    
    var = solve()
    print(var)
    
    
            
            count += 1
    with open("grids.txt", "a+") as file:
        file.seek(0)
        data = file.read(100)
        if len(data) > 0 :
            file.write("\n")
        text = np.array2string(game, separator=',')
        file.write(text)
        file.write("\n")
        