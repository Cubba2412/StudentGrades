# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:56:46 2020

@author: ThomasBirk
"""

  # MAINMENU Main script to run the bacterial analysis program utilizing 
  #          the functions of the other files imported from the same directory
  ##
  # Usage: mainMenu()
  ##
  # Author: Thomas B. Frederiksen, s183729@student.dtu.dk, 2020

import os.path
folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder)
from loadGrades import *
from userInput import *

#Initiliaze variables
print("Welcome to the python student Grading Analysis program")
dataLoaded = False
#dataChoice = 1
dataNotLoaded = "Data has not been loaded. Please load data to perform calculations"
while True:
   
        printMenu()
        #If the data has been filtered, inform the user
# =============================================================================
#         if(dataFiltered):
#             print("\n\nFiltered data available")
#             print("Current data filter parameters: ")
#             print("Bacteria Type:",bacteriaTypes[bacteria])
#             print("Lower and Upper limit [{:.2f}, {:.2f}]".format(l_lim,u_lim))
#         
# =============================================================================
        #Prompt user for a menu choice, and act upon the choice
        choice = inputChoiceNum("Please choose an option: ", "Menu")            
        if(choice == 1):
           gradesData, dataLoaded, colNum, studentNum = loadGrades()
           
        elif(choice == 2):
            #If data has not been loaded, inform the user load data
            if not(dataLoaded):
                print(dataNotLoaded)
            else:
                while True:
                   try:
                       Errors = checkData(gradesData,studentNum,colNum)
                       break
                   except ValueError:
                       print("Error when checking data")
                       pass  
                   
        elif(choice == 3):
            #If data has not been loaded, inform the user load data
           if not(dataLoaded):
                print(dataNotLoaded)
           else:
              print("option 3 chosen")
              
# =============================================================================
#                while True:
#                    try:
#                      
#                        else:
#                            break
#                    except ValueError:
#                        print("\nStatistic not found \nPlease enter one of the following valid statistics: \n")
#                        
#                        pass
# =============================================================================
        
        elif(choice == 4):
            #If data has not been loaded, inform the user load data
            if not(dataLoaded):
                print(dataNotLoaded)
# =============================================================================
#             elif(dataFiltered):
#                 while True:
#                    try:       
#                        #Prompt if the plot should be generated from the 
#                        #original or filtered data
#                        dataChoice = inputChoiceNum("Would you like to plot the original data (1) or the filtered data (2): ", "Filtered data")
#                        if(dataChoice == 2):
#                            dataPlot(newDat)
#                            break
#                        else:
#                            dataPlot(data)
#                            break
#                    except ValueError:
#                        print("Error when creating plots")
#                        pass
# =============================================================================
            else:
                print("\nGenerating list of grades...\n")
        #Exit the program, by breaking the loop
        elif(choice == 5):
            print("Goodbye")
            break    
