
import numpy as np
from pandas import *


# sortByName prints out a dataframe of the matrix, that is sorted by student names
#
# input: grades(a matrix of size NxM)
# Usage: prints out a dataframe sorted by student names
#
# Author: Henrik Riise Nielsen, s183693@student.dtu.dk, 2020
def sortByName(grades):
    
    grades = grades[np.argsort(grades[:, 1])]                            #Sorts by the second coloumn 

    matrix = np.row_stack(grades)                                        #Turns the list of lists in to a matrix
    
    
    header = np.array(["StudentID", "Name"])                             #creates the two first elements of the first row
    for i in range(len(matrix[0])-3):
        header = np.append(header,("Ass " + str(i+1)))                   #Adds a new element for each assignment
    header = np.append(header, "Final Grade")
    
    df = DataFrame(grades, columns=header).to_string(index=False)        #Creates the dataframe with a costum first row and without the first column

    print(df + '\n')
    
    return





