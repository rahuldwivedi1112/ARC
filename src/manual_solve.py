#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.
'''
def solve_6a1e5592(x):
    return x

def solve_b2862040(x):
    return x

def solve_05269061(x):
    return x
'''
def inside_grid(x,y,shape):
    max_row,max_column = shape
    grid = False
    if (x >=0 and x<=max_row-1) and (y>=0 and y <=max_column-1):
        grid = True
    return grid

def solve_73251a56(x):
    #there seems to be symmetry accross diagnal
    #if we move along the diagnal the values in rows and columns are symmetrical
    #we can use this symmetry to solve this problem.
    row,col = x.shape
    # we need to move through points (0,0)->(1,1)...(max,max)
    for i in range(row):
        j=i
        while(inside_grid(i,j, x.shape)):
            #handle case when value in diagonal is missing replace it with previous value
            if x[i,i] ==0 and i !=0:
                x[i,i] = x[i-1,i-1]
            if x[i,j] != x[j,i]:
                if x[i,j]==0:
                    x[i,j] = x[j,i]
                if x[j,i]==0:
                    x[j,i] = x[i,j]
            #case when we dont have value at either side of dialgonal
            if x[i,j] == x[j,i] and x[i,j] ==0:
                pass
                
            j += 1
                
    print(np.unique(x))
    return x

"""
def solve_508bd3b6(x):
    #calculate the size of the grid
    #this would be used to check if a point is inside the grid

    #calculate the occurances of value 8  
    row_pos,col_pos = np.where(x==8)
    #we will start the algorithm from first position of 8 
    frow_8 = row_pos[0]
    fcol_8 = col_pos[0]
    print(x[frow_8,fcol_8])
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
    
    print(direction)
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
    print(wall)
    
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
"""
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

