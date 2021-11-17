#!/usr/bin/python

"""

Student name(s): Rahul Dwivedi
Student ID(s):   21252240
GitHub URL: https://github.com/rahuldwivedi1112/ARC

"""

"""
Summary
Libraries: 
All three tasks were solved by basic python using Loops and conditional statements. i have used Numpy library in one of the task  
for matrix manipulation which i have found to be most useful. It provided built in functions to perform operations such as matrix 
creation with zeros ,extract  a diagonal of the matrix and rotating a matrix 90 degrees, which otherwise would have required complicated
bit of coding. It also provides various functions to rearrange elements of an array which I used for my first iteration but were not required for the final code

Solve functions:
Though all three tasks were different from each other, task eb5a1d5d and 73251a56 both required finding a color pattern list and using 
that to either fill in symmetrical pattern or create a new grid with subset of that pattern. Task 508bd3b6 involved extending the trajectory of an object when it bounces off a red wall. All three tasks assumes that the human or machine should have prior understanding of various techniques.First two tasks require understanding of patterns,symmetry and downscaling of the grid shape where as the third requires knowledge of geometry, shapes and whether the point is inside or outside.

There is no common approach which would work on all of the 3 tasks, making them difficult for a machine to solve compared to a human. Uniqueness of the tasks also adds to the complexity as there is no as such training data which could be used to train the ML models. 

"""

import os, sys
import json
import numpy as np
import math as m
import re
import itertools

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

def solve_eb5a1d5d(x):
    '''
    Description: 
    The task demonstration has a block of color inside another color in layers. The number of colors and block size/position 
    of each color is not constant and varies with each example. The output of transformation is a symmetrical grid with each 
    color making a box of a single cell width and color inside the block follows same sequence as that of test grid. The 
    innermost color would occupy a single cell. The whole example can be treated as creating a Russian doll of colors.  
    
    Solution: 
    The code solves this by first calculating which colors would make up the boxes. This is done by calculating the color changes
    on the input grid. The size of grid is calculated by how many times the color shift happens though doing [(number of color*2) -1]
    would also give the row/column size.As there is no geric position where the inner block of color would be, the code calculates the
    color shift for each column and takes the maximum.The code then uses this color list to populate one half triangle of the grid 
    including the diagonal. It then uses the symmetrical nature of the grid to populate the other half. This is done by first rotating 
    the grid 90 degrees so that populated half is at upper right and then uses the matrix copy formula to copy the upper half into lower.
    
    All the grid examples were solved correctly.
    '''
    #get the row and column size of the input grid
    row,col = x.shape
    #build the list of color changes. after checking mid column and mid row,the more generic way to do it 
    #is to check each row and build the color list having maximum number of colors. this would again require 2 for 
    #loops which is not ideal but would work for all scenarios
    final_color_list =[]
    #Loop through all columns
    for j in range(col):
        color_list = []
        #append the first color of each row
        color_list.append(x[0][j])
        #loop through the second last row as we are comparing next value to previous
        for i in range(row-1):
            if x[i][j]!=x[i+1][j]:
                color_list.append(x[i+1][j])
        #Check for the color list of max length
        if len(final_color_list) <= len(color_list):
            final_color_list = color_list      

    #create new matrix based on the number of color changes
    shape = len(final_color_list),len(final_color_list)
    #create the grid with 0's using numpy 
    y = np.zeros(shape,dtype=int)
    #populate the first half of the grid including the diagonal
    #the first loop is for each color in the color list
    for i in range(len(final_color_list)):
        #the value of j is based on color list and which iteration we are on
        #for first color it goes from 0,0 to 0,max(column) and max(row),0
        #but for second color it should go from 1,1 to 1,(max(col)-1) and (max(row)-1),1
        j = (len(final_color_list)-1)-i
        while(j>=(0+i)):
            #populate the value of that color
            y[i][j]=final_color_list[i]
            y[j][i]=final_color_list[i]
            j -=1
    #rotate the matrix by 90 degrees
    y = np.rot90(y,-1)
    #copy the upper half to lower half using Matrix copy rule.
    y = y + y.T - np.diag(np.diag(y))
    return y


def inside_grid(x,y,shape):
    '''
    Description:
    This function takes in the x and y coordinate and shape of the grid
    and returns whether that coordinate is present inside the grid or not
    '''
    max_row,max_column = shape
    grid = False
    if (x >=0 and x<=max_row-1) and (y>=0 and y <=max_column-1):
        grid = True
    return grid

def solve_73251a56(x):
    '''
    Description: 
    This task involves filling the empty portion of the grid with appropriate color based on the existing pattern. 
    the colors closer to the diagonal are exapnding in grid as we move across the diagonal.There is a symmetry around 
    diagonal but that alone is not enough as there are blanks on both sides.Luckily there is an inherent mathamatical pattern 
    inside the grid which can be utilized to solve the problem
    
    Solution:
    The code utilizes a pattern to fill in the correct values and its same for each input grid. We first find out the number of colors 
    present in the grid and their assigned number. Suppose the color list is [2,3,4,5,6] and diagonal color is 4.From first 
    position (0,0) the next row element is (diagonal color -1) i,e, 3 and it repeats (row number +1) times.the next element is 
    then the next color from the color list which repeats (row number +2) times and so on till the grif ends. This pattern is symmetrical 
    for row and coloumn. Using this the code moves along the diagonal, finding and filling missing color in diagnoal and build the 
    pattern in row and column
    
    All the grid examples were solved correctly.
    
    '''
    #get the unique colors in the grid.
    color_list = list(np.unique(x))
    #remove black color
    color_list.pop(0)
    row,col = x.shape
    #get the diagonal element from the array  apart from zero
    dia_elements = x.diagonal()
    dia_element = max(dia_elements[dia_elements !=0])
    #fetching index and value of one element before the diagnonal element
    #this is where the color of the pattern starts
    dia_index = color_list.index(dia_element)
    #handle case when diagonal element is the first elemnt of list 
    #then we need to take the last element
    if dia_index == 0:
        index = len(color_list) - 1
    else:
        index = dia_index-1
    #get the color value at the pattern start index
    value = color_list[index]
    #run the loop through diagonal barring the last element 
    #put last element as diagonal value to handle case if last element is 0
    x[row-1][col-1] = dia_element
    
    for i in range(row-1):
        #put the diagonal value as the diagonal element
        x[i][i]=dia_element
        #Start J as i+1 as we need to start pattern from next cell in row and column
        j = i+1
        #A counter to track when to switch color to the next in the color list 
        color_counter = 0
        curr_col_index = index
        #run the loop till the end of the grid which can be calculated as col-j from each diagonal position
        for a in range((col-j)):
            #There is always a color change from the next cell, below code handles that
            #and chooses the next color
            if a==(i+1):
                #If we reach end of color list we need to start from the beginning
                if (curr_col_index+1) == len(color_list):
                    curr_col_index=0
                else:
                    curr_col_index +=1
                #reset the color counter
                color_counter= 0
            #Choose the next color at i+2 position 
            if color_counter==(i+2):
                if (curr_col_index+1) == len(color_list):
                    curr_col_index=0
                else:
                    curr_col_index +=1
                color_counter= 0
            #get the color value at the current color index
            value = color_list[curr_col_index]
            # fill the value of blank cell in row or column
            if x[i][j] == 0:
                x[i][j] = value
            if x[j][i] == 0:
                x[j][i] = value
            #increment the color and column counter.
            color_counter +=1
            j=j+1
     
    return x

def grid_travel(x,row,col,direction=None):
    '''
    Description:
    the function travels along the direction specified starting from position row,col
    if the next point is inside the grid, it puts the value of 3 on the grid cell.This
    continues until we reach the end of grid.
    
    Parameters:
    x : grid
    row : row position of the start point
    col : column position of the start point
    direction: Direction in which we should move with respect to the starting point
    
    '''
    # an Upper right point would be row -1 and col+1
    if direction == 'ur':
        while(inside_grid(row-1,col+1, x.shape)):
                row -=1
                col +=1
                x[row,col] = 3
    # an Upper left point would be row -1 and col-1
    elif direction == 'ul':
        while(inside_grid(row-1,col-1, x.shape)):
                row -=1
                col -=1
                x[row,col] = 3
    # a lower  left point would be row+1 and col-1
    elif direction == 'll':
        while(inside_grid(row+1,col-1, x.shape)):
                row +=1
                col -=1
                x[row,col] = 3
    # a lower  left point would be row+1 and col-1
    elif direction == 'lr':
        while(inside_grid(row+1,col+1, x.shape)):
                row +=1
                col +=1
                x[row,col] = 3

    return x

def solve_508bd3b6(x):
    '''
    Description: 
    The task can be viewed as an instrument firing an object towards a wall. Upon hitting the wall, the object then bounces off
    and travels towards the end of the grid. Here the Orientation of wall can be vertical or horizontal and it can be of varied thickness.
    The length of the instrument can also vary but it will start from a point which is on edge of the grid. The solution needs to find the
    trajectory of the object and put the color on its path based on which direct it was fired from and from what length instrument. The
    bounce of direction also depends on the direction the object hit the wall and orientation of the wall
    
    
    Solution: 
    The codes first find the position of an edge of the firing instrument by looking row wise. It will always get the bottom edge or top 
    edge but never the middle of the instrument. Based on the direction of other points of the instrument the code calculates the firing
    direction and then starts coloring the trajectory until it hits the wall. The code then calculates the orientation of wall but checking
    its nearby cells. Once it has calculated the wall position and hitting direction it then paints the trajectory in bounce off direction
    until it reaches the end of the grid
    
    All the grid examples were solved correctly.
    
    '''
    #calculate the occurances of value 8 which gives us the edge of instrument 
    row_pos,col_pos = np.where(x==8)
    #we will start the algorithm from first position of 8 
    frow_8 = row_pos[0]
    fcol_8 = col_pos[0]
    #We need to go in the direction of next 8 until we hit a wall of 2
    #as we take first occurrence of 8 by row, the next 8 can only be 
    #in the lower left or lower right, We then check the oppoesite corner if 
    #its outside grid or its 8 or 0. based on that we can define the direction as
    # ul(upperleft),ur(upperright) etc
    direction = None
    #if lowerleft is 8 and upper right is 0 then we need to fire in upper right
    if inside_grid(frow_8+1,fcol_8-1, x.shape) and x[frow_8+1,fcol_8-1]==8:
        if inside_grid(frow_8-1,fcol_8+1, x.shape) and x[frow_8-1,fcol_8+1]==0:
            direction = 'ur'
        #else we have to fire in opposite direction which is lower left
        else:
            direction = 'll'
    if inside_grid(frow_8+1,fcol_8+1, x.shape) and x[frow_8+1,fcol_8+1]==8:
        #if lowerright is 8 and upper right is 0 then we need to fire in upper right
        if inside_grid(frow_8-1,fcol_8-1, x.shape) and x[frow_8-1,fcol_8-1]==0:
            direction = 'ul'
        #else we have to fire in opposite direction which is lower right
        else:
            direction = 'lr'
    

    #once direction is decided we need to keep going untill we hit the wall
    if direction =='ur':
        #upper right and upper left wont have an occurrence of 8 else those would have been our starting location
        while(x[frow_8-1,fcol_8+1]!=2):
            frow_8 -=1
            fcol_8 +=1
            x[frow_8,fcol_8] = 3
    if direction == 'ul':
        while(x[frow_8-1,fcol_8-1]!=2):
            frow_8 -=1
            fcol_8 -=1
            x[frow_8,fcol_8] = 3
    if direction == 'll':
        # direction of lower left and lower right can have a occurence of 8
        while(x[frow_8+1,fcol_8-1]!=2):
            frow_8 +=1
            fcol_8 -=1
            #extra condition for occurrence of 8 
            if x[frow_8,fcol_8] != 8:
                x[frow_8,fcol_8] = 3
    if direction == 'lr':
        while(x[frow_8+1,fcol_8+1]!=2):
            frow_8 +=1
            fcol_8 +=1
            #extra condition for occurrence of 8 
            if x[frow_8,fcol_8] != 8:
                x[frow_8,fcol_8] = 3
        
    #Once we hit the wall we have decide the bounce direction based on the orientation of wall
    #for example, if wall is horizontal , upper right will bounce off to lower right
    #and if wall is vertical, upper right will bounce off to upper left
    
    #check if wall is vertical or horizontal by checking neighbors in vertical corners.
    if x[frow_8,fcol_8+1] ==2 or x[frow_8,fcol_8-1] ==2:
        wall = 'vertical'
    else:
        wall = 'horizontal'

    
    #based on wall orientation and our initial direction we can calculate the bounce off direction
    #we need to keep going in new direction and inserting 3 till we hit the end of grid
    
    if wall == 'vertical':
        if direction =='ur':
        #bounce in upper left by going (-1,-1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ul')

        if  direction =='lr':
            #bounce in lower left by going (+1,-1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ll')

        if direction =='ul':
            #bounce in upper right by going(-1,+1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ur')

        if direction =='ll':
            #bounce in lower right by going(+1,+1) from current position
            x = grid_travel(x,frow_8,fcol_8,'lr')

    #if wall direction is horizontal
    else: 
        if direction =='ur':
            #bounce in lower right by going (+1,+1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ll')

        if  direction =='lr':
            #bounce in upper right by going (-1,+1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ur')
        if direction =='ul':
            #bounce in lower left by going (+1,-1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ll')

        if direction =='ll':
            #bounce in upper left by going (-1,-1) from current position
            x = grid_travel(x,frow_8,fcol_8,'ul')

    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    if y.shape != yhat.shape:
        print(f"False. Incorrect shape: {y.shape} v {yhat.shape}")
    else:
        print(np.all(y == yhat))


if __name__ == "__main__": main()

