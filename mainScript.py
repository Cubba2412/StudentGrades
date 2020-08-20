#Main Script shared responsibilites
#Lines 16-43: Thomas B. Frederiksen s183729@student.dtu.dk
#lines 45-52: Henrik Riise Nielsen, s183693@student.dtu.dk
#lines 54-74: Casper Grindsted, s183688@student.dtu.dk

import os.path
folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder)
from loadGrades import *
from userInput import *
from GradesPlot import *
from computeFinalGrades import *
from sortingHat import *


#Initiliaze variables
print("Welcome to the python student Grading Analysis program")
dataLoaded = False
#dataChoice = 1
dataNotChecked = 'WARNING: The loaded data contains errors which will affect calculations. Run the \"Check Data\" option to correct this\n'
dataNotLoaded = "Data has not been loaded. Please load data to perform calculations \n"
while True:
    if(dataLoaded and not Errors.empty):
        print(dataNotChecked)
    printMenu()
    #Prompt user for a menu choice, and act upon the choice
    choice = inputChoiceNum("Please choose an option: ", "Menu")            
    if(choice == 1):
       gradesData, dataLoaded, colNum, studentNum = loadGrades()
       Errors = loadErrors(gradesData)
       
    elif(choice == 2):
        #If data has not been loaded, inform the user load data
        if not(dataLoaded):
            print(dataNotLoaded)
        else:
            while True:
               try:
                   Errors = checkData(gradesData)
                   break
               except ValueError:
                   print("Error when checking data")
                   pass  
               
    elif(choice == 3):
        #If data has not been loaded, inform the user load data
       if not(dataLoaded):
            print(dataNotLoaded)
       else:
          grades = gradesData.iloc[0:studentNum,2:colNum+1].to_numpy()
          gradesPlot(grades)
          
    #Display list of grades
    elif(choice == 4):
        
            #If data has not been loaded, inform the user to load data
            if not(dataLoaded):
                print(dataNotLoaded)
                
            else:
                print("\nGenerating list of grades...\n")  
                #Get grade data from gradesData matrix
                grades = gradesData.iloc[0:studentNum,2:colNum].to_numpy()
                
                #Compute final grade for each student  
                gradesF = computeFinalGrades(grades)
                                
                #Add computed final grades to gradesData matrix
                gradesF = np.reshape(gradesF, [studentNum, 1]) #Transverse array so it can be added as a column to the gradesData matrix 
                finalGradesData = np.hstack((gradesData, gradesF))
                
                #Sorts grades for all of the students in alphabetical order and display list
                sortByName(finalGradesData)
                
    #Exit the program, by breaking the loop
    elif(choice == 5):
        print("Goodbye")
        break    
