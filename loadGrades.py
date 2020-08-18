# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:48:19 2020

@author: ThomasBirk
"""

import pandas as pd
from userInput import *
import os.path
import numpy as np

def loadGrades():
    while True:
            try:
                #Load datafile if it is a valid filename, otherwise
                #reprompt for valid filename
                filename = inputChoiceStr("Please enter the name of the datafile to load: ")
                if(os.path.isfile(filename)):
                    gradesData = pd.read_csv(filename)
                    dataLoaded = True
                    break
                else:
                    print("\nFile not found. Please enter valid filename")
            except:
                print("\nError while loading datafile")
   
    
    #Create column dataframe to add to the main data, indicating number of 
    #of assignments per student for each student
    colNum = len(gradesData.columns)
    studentNum = gradesData.shape[0]
    studentAssign = pd.DataFrame(np.arange(studentNum).reshape(-1,1), columns=['Number of Assignments'])
    assignNum = 0
    
    
    for i in range(0,studentNum):
       for j in range(0,colNum-2):
           #If the student completed the assignment, (value is not null (nan))
           #increment assignment count
           if not(gradesData.isnull().iloc[i:i+1,2:colNum].values[0,j]):
               assignNum += 1
       #Acess first column at row index i and set value to number of assignments for the student
       studentAssign.iloc[:,0].iloc[i] = assignNum
       assignNum = 0
           
    #Join the number of assignments column with original data.
    gradesData = gradesData.join(studentAssign)
    
    
    return gradesData, dataLoaded, colNum, studentNum


def checkData(gradesData,studentNum,colNum):
    
    
    grades = [None, -3, 0, 2, 4, 7, 10, 12]
    #Check if grade exists in valid grades of "grades" array
    #nan (None) included as we wish to determine grades not in the scale, not grades missing
    #convert to Numpy array to obtain index:
    wrongGrades = ~gradesData.iloc[0:studentNum,2:colNum].isin(grades).values
    idxGrade = np.where(wrongGrades == True)
    #Find indexes of assignments not graded:
    noAssign = gradesData.iloc[0:studentNum,2:colNum].isnull().values
    idxAssign = np.where(noAssign == True)
    #Find indexes for students with same StudentID's
    duplicateID =  gradesData.duplicated(['StudentID']).values
    idxID = np.where(duplicateID == True)
    duplicateName =  gradesData.duplicated(['Name']).values
    #Find indexes for students with the same Names
    idxName = np.where(duplicateName == True)
    #Store all indexes above in a pandas dataframe:
    data = [['Wrong Grade',idxGrade],['No Assignment',idxAssign],['Duplicate studentID',idxID],['Duplicate Name',idxName]]
    Errors = pd.DataFrame(data,columns = ['ErrorType','Index'])
    dataChecked = False
    checkedAll = False
    while True:
        #Prompt user for what errors they wish to see.
        print("\nOptions:")
        print("1. Wrong Grades\n2. Uncompleted Assignments\n3. Duplicate StudentID's \n4. Duplicate Names\n5. Everything \n6. Exit to main Menu")
        if(dataChecked & checkedAll):
             choice = inputChoiceNum("Data checked for all Errors. Would you like to exit to the main menu? (Y:1,N:0)", "Y/N")
             if(choice == 1):
                 break
             else:
                 checkedAll = False
        elif(dataChecked):
            choice = inputChoiceNum("Which other Errors would you like to check for?", "Data Check")
        
        else:
            choice = inputChoiceNum("What errors would you like to check the data for?", "Data Check")
         
        if (choice == 5):
            dataChecked = True
            checkedAll = True
            for i in range(len(Errors.iloc[0][1])):
                    #Inform user of which assignment for which student, has a wrong grade
                    #with index data from Errors dataframe
                    print("The grade ({}) for student {} of \"{}\" is not on the 7 step scale".format(gradesData.iloc[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2],gradesData.iloc[Errors.iloc[0][1][0][i],1],gradesData.columns[Errors.iloc[0][1][1][i]+2]))
                    print(wrongGrades)
            for i in range(len(Errors.iloc[1][1])):
                #Inform user of which assignment for which student, has a wrong grade
                print("The student {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.iloc[1][1][0][i],1],gradesData.columns[Errors.iloc[1][1][1][i]+1]))
            for i in range(len(Errors.iloc[2][1])):
                #Inform user of which students have the same student ID
                print("The studentID for student \"{}\" is the same as for student \"{}\"".format(gradesData.iloc[Errors.iloc[2][1][0][i]-1,1],gradesData.iloc[Errors.iloc[2][1][0][i],1]))
            for i in range(len(Errors.iloc[3][1])):
                #Inform user of which students have the same name
                print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(gradesData.iloc[Errors.iloc[3][1][0][i]-1,0],gradesData.iloc[Errors.iloc[3][1][0][i],0]))
        elif(choice == 6):
            break
        else:
            if(choice == 1):
                dataChecked = True
                for i in range(len(Errors.iloc[0][1])):
                    #Inform user of which assignment for which student, has a wrong grade
                    #with index data from Errors dataframe
                    print("The grade ({}) for student {} of \"{}\" is not on the 7 step scale".format(gradesData.iloc[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2],gradesData.iloc[Errors.iloc[0][1][0][i],1],gradesData.columns[Errors.iloc[0][1][1][i]+2]))
            
            elif(choice == 2):
                dataChecked = True
                for i in range(len(Errors.iloc[1][1])):
                    #Inform user of which assignment for which student, has a wrong grade
                    print("The student {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.iloc[1][1][0][i],1],gradesData.columns[Errors.iloc[1][1][1][i]+1]))
                
            elif(choice == 3):
                dataChecked = True
                for i in range(len(Errors.iloc[2][1])):
                    #Inform user of which students have the same student ID
                    print("The studentID for student \"{}\" is the same as for student \"{}\"".format(gradesData.iloc[Errors.iloc[2][1][0][i]-1,1],gradesData.iloc[Errors.iloc[2][1][0][i],1]))
            elif(choice == 4):
                dataChecked = True
                for i in range(len(Errors.iloc[3][1])):
                    #Inform user of which students have the same name
                    print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(gradesData.iloc[Errors.iloc[3][1][0][i]-1,0],gradesData.iloc[Errors.iloc[3][1][0][i],0]))
            
    return Errors