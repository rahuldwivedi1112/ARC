#!/usr/bin/python

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
    #get the number of rows and columns required for the grid
    #for this we will go to mid row and calculate the change in colors
    #we will also build the color List in the same step
    
    row,col = x.shape
    '''
    mid_col_index = m.ceil(col/2)
    #append first color of the row
    color_list.append(x[0][mid_col_index])
    for i in range(row-1):
        if x[i][mid_col_index]!=x[i+1][mid_col_index]:
            color_list.append(x[i+1][mid_col_index])
    '''
    #after checking mid column and mid row, i think the more generic way to do it 
    #is to check each row and build the color list having maximum number of colors
    # this would again require 2 for loops which is not ideal but would work for all 
    #scenarios
    final_color_list =[]
    for j in range(col):
        color_list = []
        #append the first color of each row
        color_list.append(x[0][j])
        for i in range(row-1):
            if x[i][j]!=x[i+1][j]:
                color_list.append(x[i+1][j])
        if len(final_color_list) <= len(color_list):
            final_color_list = color_list      

    #create new matrix based on the number of color changes
    shape = len(final_color_list),len(final_color_list)
    y = np.zeros(shape,dtype=int)
    for i in range(len(final_color_list)):
        j = (len(final_color_list)-1)-i
        while(j>=(0+i)):
            y[i][j]=final_color_list[i]
            y[j][i]=final_color_list[i]
            j -=1
    y = np.rot90(y,-1)
    y = y + y.T - np.diag(np.diag(y))
    return y


def inside_grid(x,y,shape):
    max_row,max_column = shape
    grid = False
    if (x >=0 and x<=max_row-1) and (y>=0 and y <=max_column-1):
        grid = True
    return grid

def solve_73251a56(x):

    color_list = list(np.unique(x))
    #remove black color
    color_list.pop(0)
    row,col = x.shape
    #get the diagonal elelment from the array  apart from zero
    dia_elements = x.diagonal()
    dia_element = max(dia_elements[dia_elements !=0])
    #fetching index and value of one element before the diagnonal element
    #fetching index and value of one element before the diagnonal element
    #this is where the color of the pattern starts
    
    #handle case when diagonal element is the first elemnt of list 
    #then we need to take the last element
    dia_index = color_list.index(dia_element)

    if dia_index == 0:
        index = len(color_list) - 1
    else:
        index = dia_index-1

    value = color_list[index]
    #run the loop through diagonal barring the last element 
    #put last element as diagonal value to handel case if last element is 0
    x[row-1][col-1] = dia_element
    
    for i in range(row-1):
        x[i][i]=dia_element
        j = i+1
        color_counter = 0
        curr_col_index = index
        for a in range((col-j)):

            if a==(i+1):
                if (curr_col_index+1) == len(color_list):
                    curr_col_index=0
                else:
                    curr_col_index +=1
                color_counter= 0
            if color_counter==(i+2):
                if (curr_col_index+1) == len(color_list):
                    curr_col_index=0
                else:
                    curr_col_index +=1
                color_counter= 0
            value = color_list[curr_col_index]
            if x[i][j] == 0:
                x[i][j] = value
            if x[j][i] == 0:
                x[j][i] = value
            color_counter +=1
            j=j+1
     
    return x

def solve_508bd3b6(x):
    #calculate the size of the grid
    #this would be used to check if a point is inside the grid

    #calculate the occurances of value 8  
    row_pos,col_pos = np.where(x==8)
    #we will start the algorithm from first position of 8 
    frow_8 = row_pos[0]
    fcol_8 = col_pos[0]
    #We need to go in the direction of next 8 until we hit a wall of 2
    #as we take first occurrence of 8 by row, the next 8 can only be 
    #in the lower left or lower right, We then check the oppoesite corner if 
    #its outside grid or is 0. based on that we can define the direction as
    # ul(upperleft),ur(upperright) etc
    direction = None
    if inside_grid(frow_8+1,fcol_8-1, x.shape) and x[frow_8+1,fcol_8-1]==8:
        if inside_grid(frow_8-1,fcol_8+1, x.shape) and x[frow_8-1,fcol_8+1]==0:
            direction = 'ur'
        else:
            direction = 'll'
    if inside_grid(frow_8+1,fcol_8+1, x.shape) and x[frow_8+1,fcol_8+1]==8:
        if inside_grid(frow_8-1,fcol_8-1, x.shape) and x[frow_8-1,fcol_8-1]==0:
            direction = 'ul'
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
    
    #check if wall is vertical or horizontal
    if x[frow_8,fcol_8+1] ==2 or x[frow_8,fcol_8-1] ==2:
        wall = 'vertical'
    else:
        wall = 'horizontal'

    
    #based on wall orientation and our initial direction we can calculate the bounce off direction
    #we need to keep going in new direction and inserting 3 till we hit the end of grid
    
    if wall == 'vertical':
        if direction =='ur':
        #bounce in upper left by going (-1,-1) from current position
            while(inside_grid(frow_8-1,fcol_8-1, x.shape)):
                frow_8 -=1
                fcol_8 -=1
                x[frow_8,fcol_8] = 3
        if  direction =='lr':
            #bounce in lower left by going (+1,-1) from current position
            while(inside_grid(frow_8+1,fcol_8-1, x.shape)):
                frow_8 +=1
                fcol_8 -=1
                x[frow_8,fcol_8] = 3
        if direction =='ul':
            #bounce in upper right by going(-1,+1) from current position
            while(inside_grid(frow_8-1,fcol_8+1, x.shape)):
                frow_8 -=1
                fcol_8 +=1
                x[frow_8,fcol_8] = 3
        if direction =='ll':
            #bounce in lower right by going(+1,+1) from current position
            while(inside_grid(frow_8+1,fcol_8+1, x.shape)):
                frow_8 +=1
                fcol_8 +=1
                x[frow_8,fcol_8] = 3
    #if wall direction is horizontal
    else: 
        if direction =='ur':
        #bounce in lower right by going (+1,+1) from current position
            while(inside_grid(frow_8+1,fcol_8+1, x.shape)):
                frow_8 +=1
                fcol_8 +=1
                x[frow_8,fcol_8] = 3
        if  direction =='lr':
            #bounce in upper right by going (-1,+1) from current position
            while(inside_grid(frow_8-1,fcol_8+1, x.shape)):
                frow_8 -=1
                fcol_8 +=1
                x[frow_8,fcol_8] = 3
        if direction =='ul':
            #bounce in lower left by going (+1,-1) from current position
            while(inside_grid(frow_8+1,fcol_8-1, x.shape)):
                frow_8 +=1
                fcol_8 -=1
                x[frow_8,fcol_8] = 3
        if direction =='ll':
            #bounce in upper left by going (-1,-1) from current position
            while(inside_grid(frow_8-1,fcol_8-1, x.shape)):
                frow_8 -=1
                fcol_8 -=1
                x[frow_8,fcol_8] = 3

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

