
from roundGrade import *
import numpy as np


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


