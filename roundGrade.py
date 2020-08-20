
import numpy as np

def roundGrade(grades):
    # ROUNDGRADES Recives a serie of numbers between −3 and 12 (in an array),
    # and round each number to the nearst possible grade (with some exeptions e.g. number<1 set grade as 0). 
    #
    # Usage: gradesRounded  = roundGrade(grades)
    #
    # Input: grades (array of floats)
    # Output: gradesRounded (array of floats)
    #
    # Author: Casper Grindsted, s183688@student.dtu.dk, 2020
    
    
    #Array of possible grades
    #pgrades = np.array([-3, 0, 2, 4, 7, 10, 12]) #If value is between 2 grades, using this order of grades will choose the lower one
    pgrades = np.array([12, 10, 7, 4, 2, 0, -3])  #If value is between 2 grades, using this order of grades will choose the higher one
    
    #Skal fjernes
    #test = [min(pgrades, key = lambda x: abs(grades-x)) for grades in grades]
   
    #Create an array for storing final grades for each student
    n = np.size(grades)
    gradesRounded = np.zeros(n)
    
    #Calculate nearst possible grade 
    for i in range(n):
        #Check if index i in grade array contains 0, which means a final grade has already been given in the computeFinalGrades function
        if (grades[i] != 0):
            #If the value of grades[i] is below 2 set grade as 0
            if (grades[i] < 2):
                gradesRounded[i] = 0
             #Round grades[i] to nearst possible grade
             #If grades[i] is between 2 grades, the highest grade will be chosen
            else:
                #Find distance between grades[i] and possible grades
                nearst_index = np.abs(pgrades - grades[i])
                #Set final grade equal the possible grade, which have the smallest distance to grades[i]
                gradesRounded[i] = pgrades[nearst_index.argmin()] 
    
    return gradesRounded




#ALT HERUNDER ER BARE TEST OG SKAL FJERNES
#grades = [3.5, 6, 9, 11]

#print(roundGrade(grades))


