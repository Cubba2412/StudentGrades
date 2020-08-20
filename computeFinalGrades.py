
from roundGrade import *
import os
os.getcwd()
import numpy as np
import pandas as pd

path = os.getcwd()
os.chdir(path)

def computeFinalGrades(grades):
    # COMPUTEFINALGRADES Recives a serie of grades (as rows in a matrix) for each student 
    # and returns the calculated final grade for each student.
    #
    # Usage: gradesFinal = computeFinalGrades(grades)
    #
    # Input: grades (matrix of floats)
    # Output: gradesFinal (array of floats)
    #
    # Author: Casper Grindsted, s183688@student.dtu.dk, 2020
    
    
    #Find number of rows in matrix
    n = len(grades)
    
    #Create an array for storing final grades for each student
    gradesFinal = np.zeros(n)
    #Create an array for storing mean values of a series of grades, so that they can be loaded into the roundGrade function
    meanV = np.zeros(n)
    
    
    #Calculate final grade for each row in the grades matrix 
    for i in range(n):
        
        #Remove NaN (not a number) values from row
        temp = grades[i, :][~(np.isnan(grades[i, :]))]
    
        #If a student has received the grade −3 in one or more assignments, set final grade to −3
        if (any(temp == -3)):
            gradesFinal[i] = -3
        
        #If there is only one (graded) assignment, set final grade equal that one grade
        elif (len(temp) == 1):
            gradesFinal[i] = temp[0]
            
        #If there are two or more assignments, discard the lowest grade and compute the mean value of the rest of the grades
        elif (len(temp) > 1):
            #Delete lowest grade
            x = np.delete(temp, np.argmin(temp))
            
            #Compute mean value and save in meaaV array
            meanV[i] = sum(x) / len(x)
            
            
    #Round mean values of grades to nearest possible grade using the roundGrade function with meanV array as input    
    rGrades = roundGrade(meanV)
    #In the project requrements it states that the function roundGrade should have an 
    #input as "A vector (each element is a number between −3 and 12)". That is why we split up mean values 
    #in one array and final grades in another array.
        
    #Combine the rounded mean values array with the final grades array
    gradesFinal = gradesFinal + rGrades
    
    return gradesFinal




#ALT HERUNDER ER BARE TEST OG SKAL FJERNES
#grades = np.array([[12, 10, 7], [7, np.nan, np.nan], [4, 2, np.nan], [4, 0, 0], [7, 4, 2], [12, 7, 0], [10, 2, -3], [10, 10, 4]])
#grades = np.array([[12, 10, 7], [7, None, None], [4, 2, None], [4, 0, 0], [7, 4, 2], [12, 7, 0], [10, 2, -3], [10, 10, 4]])

#data = np.array([["s1", "a", 12, 10, 7], ["s2", "b", 7, np.nan, np.nan], ["s3", "c", 4, 2, np.nan], ["s4", "d", 4, 0, 0], ["s5", "e", 7, 4, 2], ["s6", "f", 12, 7, 0], ["s7", "g", 10, 2, -3], ["s8", "h", 10, 10, 4]])

#a = np.array([[ 7.,  4.,  4., nan], [12.,  7.,  2., nan], [10.,  4., 12., 7.], [10., nan, 12.,  2.]])
a = np.array([[ 7.,  4.,  -3.], [12.,  np.nan,  np.nan], [10.,  4., np.nan], [10., 12.,  2.]])

print(computeFinalGrades(a))



