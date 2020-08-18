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
                filename = inputChoiceStr("Please enter the name of the datafile to load: ",'')
                if(os.path.isfile(filename)):
                    gradesData = pd.read_csv(filename)
                    dataLoaded = True
                    break
                else:
                    print("\nFile not found. Please enter valid filename with file extension suffix")
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
    #convert to list to obtain index:
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
    everything = False
    while True:
        #Prompt user for what errors they wish to see.
        
        if(dataChecked & everything):
             choice = inputChoiceNum("Data checked for all Errors. Would you like to exit to the main menu? (Y:1,N:0) ", "Y/N")
             if(choice == 1):
                 break
             else:
                 everything = False
        else:
            checkDataOptions([0,1,2,3,4,5],everything)
            if(dataChecked):
                choice = inputChoiceNum("Which other Errors would you like to check for? ", "Data Check")
            else:
                choice = inputChoiceNum("What errors would you like to check the data for? ", "Data Check")
        if (choice == 5):
            dataChecked = True
            everything = True
            for i in range(len(Errors.iloc[0][1][0])):
                    #Inform user of which assignment for which student, has a wrong grade
                    #with index data from Errors dataframe
                    print("The grade ({}) for student {} with ID {} of \"{}\" is not on the 7 step scale".format(gradesData.iloc[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2],gradesData.iloc[Errors.iloc[0][1][0][i],1],gradesData.iloc[Errors.iloc[0][1][0][i],0],gradesData.columns[Errors.iloc[0][1][1][i]+2]))
            for i in range(len(Errors.iloc[1][1][0])):
                #Inform user of which assignment for which student, has a wrong grade
                print("The student {} with ID {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.iloc[1][1][0][i],1],gradesData.iloc[Errors.iloc[1][1][0][i],0],gradesData.columns[Errors.iloc[1][1][1][i]+2]))
            print("These missing grades will be ignored in calculations performed in the rest of the program")
            for i in range(len(Errors.iloc[2][1][0])):
                #Inform user of which students have the same student ID
                print("The studentID for student \"{}\" is the same as for student \"{}\"".format(gradesData.iloc[Errors.iloc[2][1][0][i]-1,1],gradesData.iloc[Errors.iloc[2][1][0][i],1]))
            for i in range(len(Errors.iloc[3][1][0])):
                #Inform user of which students have the same name
                print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(gradesData.iloc[Errors.iloc[3][1][0][i]-1,0],gradesData.iloc[Errors.iloc[3][1][0][i],0]))
                checkDataOptions([0,2,3,4,5,],everything)
                choice = inputChoiceNum("What errors would you like to correct (if any)? ", "Data Check")
                if(choice == 1):
                    corWrongGrades(gradesData,Errors,everything)
                elif(choice == 3):
                    corWrongID(gradesData,Errors,everything) 
                elif(choice == 4):
                    corWrongNames(gradesData, Errors, everything)
                elif(choice == 5):
                     corEverything(gradesData, Errors,everything)
                elif(choice == 6):
                    continue
                   
        elif(choice == 6):
            break
        else:
            if(choice == 1):
                corWrongGrades(gradesData,Errors,everything)          
            elif(choice == 2):
                dataChecked = True
                for i in range(len(Errors.iloc[1][1][0])):
                    #Inform user of which assignment for which student, has a wrong grade
                    #Is not prompted for data removal as the data simply doesn't exist
                    print("The student {} with ID {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.iloc[1][1][0][i],1],gradesData.iloc[Errors.iloc[1][1][0][i],0],gradesData.columns[Errors.iloc[1][1][1][i]+2]))
                print("These missing grades will be ignored in calculations performed in the rest of the program")
            elif(choice == 3):
                corWrongID(gradesData,Errors)
            elif(choice == 4):
                corWrongNames(gradesData, Errors, everything)
            
    return Errors


def checkDataOptions(printChoice,everything):
    Options = list(['\n1. Wrong Grades\n','2. Uncompleted Assignments\n','3. Duplicate StudentIDs \n','4. Duplicate Names\n','5. Everything \n','6. Exit to main Menu\n'])
    print("\nOptions: ")
    if (everything):
        Options[5] = '6. Go Back\n'
    for i in printChoice:
        print(Options[i])
    return
    
def corWrongGrades(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    print("\nIncorrect Grades: ")
    for i in range(len(Errors.iloc[0][1][0])):
        #Inform user of which assignment for which student, has a wrong grade
        #with index data from Errors dataframe
        if not(everything):
            print("\nThe grade ({}) for student {} with ID {} of \"{}\" is not on the 7 step scale".format(gradesData.iloc[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2],gradesData.iloc[Errors.iloc[0][1][0][i],1],gradesData.iloc[Errors.iloc[0][1][0][i],0],gradesData.columns[Errors.iloc[0][1][1][i]+2]))
            choice = inputChoiceNum("Would you like to remove this data? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                 gradesData.iat[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2] = None
            else:
                choice = inputChoiceNum("This will effect all other data analysis. Are you sure? (Yes:1, No Remove it:0) ", "Y/N")
                if(choice ==1):
                    continue
                else:
                    gradesData.iat[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2] = None    
        else:
           
            gradesData.iat[Errors.iloc[0][1][0][i],Errors.iloc[0][1][1][i]+2] = None
    print("\nRemoving incorrect grades...")
    print("Successfully removed grades in data which are not part of the 7 step scale")
    return

def corWrongNames(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    for i in range(len(Errors.iloc[3][1][0])):
        if not(everything):
            #Inform user of which students have the same name
            print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\": ".format(gradesData.iloc[Errors.iloc[3][1][0][i]-1,0],gradesData.iloc[Errors.iloc[3][1][0][i],0]))
        else:
            print("\nDuplicate Names")
        choice = inputChoiceNum("Would you like to correct the name? (Y:1, N:0) ", "Y/N")
                  
        if(choice == 1):
            print("\n Rows of students with same name:\n",gradesData.loc[gradesData['Name'] == gradesData.iloc[Errors.iloc[3][1][0][i]-1,1]].to_string(index = False, na_rep = ''))
            newName = inputChoiceStr("Please enter the name of the student: ", "Name")
            choice = inputChoiceNum("Do you want to change the name for the first or second occurence of the duplicated name? (First:0, Second: 1) ", "Y/N")
            if (choice == 1):
               gradesData.iat[Errors.iloc[3][1][0][i],1] = newName
            else:
                gradesData.iat[Errors.iloc[3][1][0][i]-1,1] = newName
        else:
            print("\n Rows of students with same name:\n",gradesData.loc[gradesData['Name'] == gradesData.iloc[Errors.iloc[3][1][0][i]-1,1]].to_string(index = False, na_rep = ''))
            choice = inputChoiceNum("Would you like to remove the data for this student ID? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                choice = inputChoiceNum("First or second occurence of the ID? (First:0, Second: 1) ", "Y/N")
                if (choice == 1):
                    dropID = Errors.iloc[3][1][0][i]
                else:
                    dropID = Errors.iloc[3][1][0][i]-1
                #Remove row from data and reset index
                gradesData.drop(dropID, inplace = True)
                gradesData.reset_index(inplace = True)
    return

def corWrongID(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    for i in range(len(Errors.iloc[2][1][0])):
        if not(everything):
            #Inform user of which students have the same student ID
            print("The studentID for student \"{}\" is the same as for student \"{}\"".format(gradesData.iloc[Errors.iloc[2][1][0][i]-1,1],gradesData.iloc[Errors.iloc[2][1][0][i],1]))
            #Prompt user for action to be taken for this data
        else:
            print("\nDuplicate ID's: ")
        choice = inputChoiceNum("Would you like to correct the students ID? (Y:1, N:0) ", "Y/N")
        if(choice == 1):
            print("\nRows of students wih same studentID\n",gradesData.loc[gradesData['StudentID'] == gradesData.iloc[Errors.iloc[2][1][0][i]-1,0]].to_string(index = False, na_rep = ''))
            newID = inputChoiceStr("Please enter the students ID: ", "StudentID")
            choice = inputChoiceNum("Which ID should be replaced? First or second occurence of the ID? (First:0, Second: 1) ", "Y/N")
            if (choice == 1):
                gradesData.iat[Errors.iloc[2][1][0][i],0] = newID
            else:
                gradesData.iat[Errors.iloc[2][1][0][i]-1,0] = newID
        else:
            print("\nRows of students wih same studentID\n",gradesData.loc[gradesData['StudentID'] == gradesData.iloc[Errors.iloc[2][1][0][i]-1,0]].to_string(index = False, na_rep = ''))
            choice = inputChoiceNum("Would you like to remove the data for this student ID? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                choice = inputChoiceNum("First or second occurence of the ID? (First:0, Second: 1) ", "Y/N")
                if (choice == 1):
                    dropID = Errors.iloc[2][1][0][i]
                else:
                    dropID = Errors.iloc[2][1][0][i]-1
                #Remove row from data and reset index
                gradesData.drop(dropID, inplace = True)
                gradesData.reset_index(inplace = True)
            else:
                continue
    return

def corEverything(gradesData,Errors,everything):
        corWrongGrades(gradesData, Errors, everything)
        corWrongID(gradesData, Errors, everything)
        corWrongNames(gradesData, Errors, everything)
        return