# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:48:19 2020

@author: ThomasBirk
"""

import pandas as pd
from userInput import *
import os.path
import numpy as np
#Suppress pandas warnings from user
pd.set_option('mode.chained_assignment', None)

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
# =============================================================================
#     studentAssign = pd.DataFrame(np.arange(studentNum).reshape(-1,1), columns=['Number of Assignments'])
#     assignNum = 0
#     
#     
#     for i in range(0,studentNum):
#        for j in range(0,colNum-2):
#            #If the student completed the assignment, (value is not null (nan))
#            #increment assignment count
#            if not(gradesData.isnull().iloc[i:i+1,2:colNum].values[0,j]):
#                assignNum += 1
#        #Acess first column at row index i and set value to number of assignments for the student
#        studentAssign.iloc[:,0].iloc[i] = assignNum
#        assignNum = 0
#            
#     #Join the number of assignments column with original data.
#     gradesData = gradesData.join(studentAssign)
# =============================================================================
    
    
    return gradesData, dataLoaded, colNum, studentNum


def checkData(gradesData,studentNum,colNum):
    dataChecked = False
    everything = False
    while True:
        Errors = loadErrors(gradesData)
        #Prompt user for what errors they wish to see.
        if not(Errors.empty):
            if(dataChecked & everything):
                 choice = inputChoiceNum("Data checked for all Errors. Would you like to exit to the main menu? (Y:1,N:0) ", "Y/N")
                 if(choice == 1):
                     break
                 else:
                     everything = False
            else:
                options = determineOptions(Errors,everything)
                printOptions(options)
                if(dataChecked):
                    userIn = inputChoiceNum("Which other Errors would you like to check for? ", "Data Check")
                    choice = checkChoice(options,userIn)
                    
                else:
                    userIn = inputChoiceNum("What errors would you like to check the data for? ", "Data Check")
                    choice = checkChoice(options,userIn)
            if (choice == 'Everything'):
                dataChecked = True
                everything = True
                if(errorExists(Errors,'WG')):
                    for i in range(len(getNumErrors(Errors, 'WG',False))):
                        #Inform user of which assignment for which student, has a wrong grade
                        #with index data from Errors dataframe
                        print("The grade ({}) for student {} with ID {} of \"{}\" is not on the 7 step scale".format(*getPrintData(gradesData, Errors, 'WG', i)))
# =============================================================================
#                 if(errorExists(Errors,'No Assignment')):
#                     for i in range(len(Errors.loc[Errors['ErrorType'] == 'No Assignment'].iloc[0][1][0])):
#                         #Inform user of which assignment for which student, has a wrong grade
#                         print("The student {} with ID {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.loc[1][1][0][i],1],gradesData.iloc[Errors.loc[1][1][0][i],0],gradesData.columns[Errors.loc[1][1][1][i]+2]))
#                     print("These missing grades will be ignored in calculations performed in the rest of the program")
#                     deleteError(Errors,"noAssign")
                if(errorExists(Errors,'ID')):
                    for i in range(len(getNumErrors(Errors, 'ID',False))):
                        #Inform user of which students have the same student ID
                      #  print("The studentID for student \"{}\" is the same as for student \"{}\"".format(gradesData.iloc[Errors.loc[2][1][0][i]-1,1],gradesData.iloc[Errors.loc[2][1][0][i],1]))
                        print("The studentID for student \"{}\" is the same as for student \"{}\"".format(*getPrintData(gradesData,Errors,'ID',i)))
                if(errorExists(Errors,'Name')):
                    for i in range(len(getNumErrors(Errors, 'Name',False))):
                        #Inform user of which students have the same name
                        #print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(gradesData.iloc[Errors.loc[3][1][0][i]-1,0],gradesData.iloc[Errors.loc[3][1][0][i],0]))
                        print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(*getPrintData(gradesData,Errors,'Name',i)))
                if not(Errors.empty):
                    options = determineOptions(Errors,everything)
                    printOptions(options)
                    userIn = inputChoiceNum("What errors would you like to correct (if any)? ", "Data Check")
                    choice = checkChoice(options,userIn)
                    if(choice == 'Wrong Grade'):
                            corWrongGrades(gradesData,Errors,everything)
                            everything = False
                    elif(choice == 'Duplicate Student ID\'s'):
                            corWrongID(gradesData,Errors,everything) 
                            everything = False
                    elif(choice == 'Duplicate Names'):
                        corWrongNames(gradesData, Errors, everything)
                        everything = False
                    elif(choice == 'Everything'):
                         corEverything(gradesData, Errors,everything)
                         everything = False
                    elif(choice == 'Go Back\n'):
                        everything = False
                        continue
                       
            elif(choice == 'Exit to main menu\n'):
                print("Reverting back to main menu\n")
                break
            elif(choice == 'Wrong Grade'):
                    dataChecked = True
                    corWrongGrades(gradesData,Errors,everything)     
# =============================================================================
#             elif(choice == 'No Assignment'):
#                     dataChecked = True
#                     for i in range(len(Errors.loc[Errors['ErrorType'] == 'No Assignment'].iloc[0][1][0])):
#                         #Inform user of which assignment for which student, has a wrong grade
#                         #Is not prompted for data removal as the data simply doesn't exist
#                         print("The student {} with ID {} did not receive a grade for \"{}\"".format(gradesData.iloc[Errors.loc[1][1][0][i],1],gradesData.iloc[Errors.loc[1][1][0][i],0],gradesData.columns[Errors.loc[1][1][1][i]+2]))
#                     print("These missing grades will be ignored in calculations performed in the rest of the program")
#                     deleteError(Errors,"noAssign")
# =============================================================================
            elif(choice == 'Duplicate Student ID\'s'):
                    dataChecked = True
                    corWrongID(gradesData,Errors,everything)
            elif(choice == 'Duplicate Names'):
                    dataChecked = True
                    corWrongNames(gradesData, Errors, everything)
        else:
            if(dataChecked):
                print("\nNo other errors found in the data. Reverting back to main menu...")
            else:
                print("\nNo errors found in the data. Reverting to main menu...")
            break
    return Errors

def getErrIdxList(ErrorType):
    #Wrong Grades
    if(ErrorType == 'WG'):
        ErrIdxList = ['G','N','ID','A']
        
    elif(ErrorType == 'ID'):
        ErrIdxList = ['N','N']
    elif(ErrorType == 'Name'):
        ErrIdxList = ['ID','ID']
    return ErrIdxList
    

def getPrintData(gradesData,Errors,ErrorType,i):
    First = True
    stringValues = []
    ErrIdxList = getErrIdxList(ErrorType)
    for j in range(len(ErrIdxList)):
        #Grade
        if (ErrIdxList[j] == 'G'):
            #Row index:
            row = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0][i]
            #Column index
            column = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][1][i]+2
            stringValues += [gradesData.iloc[(row,column)]]
        #Student Name
        elif (ErrIdxList[j] == 'N'):
            if((ErrorType == 'ID') and First):
                #Row index:
                row = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0][i]-1
                First = False
            else:
                row = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0][i]
            #Column index
            column = 1
            stringValues += [gradesData.iloc[(row,column)]]
        #Student ID
        elif (ErrIdxList[j] == 'ID'):
            if((ErrorType == 'Name') and First):
                row = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0][i]-1
                First = False
            else:
                #Row index:
                row = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0][i]
            #Column index
            column = 0
            stringValues += [gradesData.iloc[(row,column)]]
        #Assignment
        elif (ErrIdxList[j] == 'A'):
            #Get column name directly
            columnName = gradesData.columns[Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][1][i]+2]
            stringValues += [columnName]
    return stringValues

def printOptions(options):
    print("\nOptions: ")
    for i in options:
        print(i)
    return

def getNumErrors(Errors,ErrorType,change):
    if not(change):
        num = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0]
    else:
        num = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1]
    return num
    
def corWrongGrades(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    removed = False
    print("\nIncorrect Grades: ")
    for i in range(len(getNumErrors(Errors, 'WG',False))):
        #Inform user of which assignment for which student, has a wrong grade
        #with index data from Errors dataframe
        if not(everything):
            print("The grade ({}) for student {} with ID {} of \"{}\" is not on the 7 step scale".format(*getPrintData(gradesData, Errors, 'WG', i)))
            choice = inputChoiceNum("Would you like to remove this data? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                 gradesData.iat[getNumErrors(Errors,'WG',True)[0][i],getNumErrors(Errors,'WG',True)[1][i]+2] = None
                 removed = True
            else:
                choice = inputChoiceNum("This will effect all other data analysis. Are you sure? (Yes:1, No Remove it:0) ", "Y/N")
                if(choice ==1):
                    continue
                else:
                    removed = True
                    gradesData.iat[getNumErrors(Errors,'WG',True)[0][i],getNumErrors(Errors,'WG',True)[1][i]+2] = None
              
        else:
           removed = True
           gradesData.iat[Errors.loc[0][1][0][i],Errors.loc[0][1][1][i]+2] = None
    if(removed):
        print("\nRemoving incorrect grades...")
        deleteError(Errors, "WG")
        print("Successfully removed grades in data which are not part of the 7 step scale")
    
    return

def corWrongNames(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    for i in range(len(getNumErrors(Errors, 'Name',False))):
        if not(everything):
            #Inform user of which students have the same name
            print("The name for the student with studentID \"{}\" is the same as for the student with studentID \"{}\"".format(*getPrintData(gradesData,Errors,'Name',i)))
        else:
            print("\nDuplicate Names")
        choice = inputChoiceNum("Would you like to correct the name? (Y:1, N:0) ", "Y/N")
                  
        if(choice == 1):
            print("\n Rows of students with same name:\n",gradesData.loc[gradesData['Name'] == gradesData.iloc[getNumErrors(Errors, 'Name',False)[i]-1,1]].to_string(index = False, na_rep = ''))
            newName = inputChoiceStr("Please enter the name of the student: ", "Name")
            choice = inputChoiceNum("Do you want to change the name for the first or second occurence of the duplicated name? (First:0, Second: 1) ", "Y/N")
            if (choice == 1):
               gradesData.iat[getNumErrors(Errors, 'Name',False)[0],1] = newName
            else:
                gradesData.iat[getNumErrors(Errors, 'Name',False)[0]-1,1] = newName
            print("\nEditing Name of student...")
            deleteError(Errors, "Name")
            print("Succesfully edited name of the student")
        else:
            print("\n Rows of students with same name:\n",gradesData.loc[gradesData['Name'] == gradesData.iloc[getNumErrors(Errors, 'Name',False)[i],1]].to_string(index = False, na_rep = ''))
            choice = inputChoiceNum("Would you like to remove the data for the student with duplicate name? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                choice = inputChoiceNum("First or second occurence of the Name? (First:0, Second: 1) ", "Y/N")
                if (choice == 1):
                    dropID = getNumErrors(Errors, 'Name',False)[0]
                else:
                    dropID = getNumErrors(Errors, 'Name',False)[0]-1
                print(dropID)
                
                #Remove row from data and reset index
                gradesData.drop(dropID,inplace = True)
                gradesData.reset_index(inplace = True, drop = True)
                print(gradesData)
                print("\nRemoving data with duplicate Name...")
                deleteError(Errors, "Name")
                print("Successfully removed data for duplicate Name")
            print("\nReverting back to main menu")
            
    return

def corWrongID(gradesData,Errors,everything):
    dataChecked = True
    choice = 0
    for i in range(len(getNumErrors(Errors, 'ID',False))):
        if not(everything):
            #Inform user of which students have the same student ID
            print("The studentID for student \"{}\" is the same as for student \"{}\"".format(*getPrintData(gradesData,Errors,'ID',i)))
            #Prompt user for action to be taken for this data
        else:
            print("\nDuplicate ID's: ")
        choice = inputChoiceNum("Would you like to correct the students ID? (Y:1, N:0) ", "Y/N")
        if(choice == 1):
            print("\nRows of students wih same studentID\n",gradesData.loc[gradesData['StudentID'] == gradesData.iloc[getNumErrors(Errors, 'ID',False)[i]-1,0]].to_string(index = False, na_rep = ''))
            newID = inputChoiceStr("Please enter the students ID: ", "StudentID")
            choice = inputChoiceNum("Which ID should be replaced? First or second occurence of the ID? (First:0, Second: 1) ", "Y/N")
            if (choice == 1):
                gradesData.iat[getNumErrors(Errors, 'ID',False)[0],0] = newID
            else:
                gradesData.iat[getNumErrors(Errors, 'ID',False)[0]-1,0] = newID
            print("\nEditing studentID...")
            deleteError(Errors, "ID")
            print("Successfully edited StudentID")
        else:
            print("\nRows of students wih same studentID\n",gradesData.loc[gradesData['StudentID'] == gradesData.iloc[getNumErrors(Errors, 'ID',False)[i]-1,0]].to_string(index = False, na_rep = ''))
            choice = inputChoiceNum("Would you like to remove the data for this student ID? (Y:1, N:0) ", "Y/N")
            if(choice == 1):
                choice = inputChoiceNum("First or second occurence of the ID? (First:0, Second: 1) ", "Y/N")
                if (choice == 1):
                    dropID = getNumErrors(Errors, 'ID',False)[0]
                else:
                    dropID = getNumErrors(Errors, 'ID',False)[0]-1
                #Remove row from data and reset index
                gradesData.drop(dropID, inplace = True)
                gradesData.reset_index(inplace = True, drop=True)
                print("\nRemoving data with duplicate ID...")
                deleteError(Errors, "ID")
                print("Successfully removed data for duplicate ID")
            else:
                continue
    return

def corEverything(gradesData,Errors,everything):
        if(errorExists(Errors,'WG')):
            corWrongGrades(gradesData, Errors, everything)
        if(errorExists(Errors,'ID')):   
            corWrongID(gradesData, Errors, everything)
        #Reload Errors to check if a removal of row with ID also fixed error
        #with same name
        Errors = loadErrors(gradesData)
        if(errorExists(Errors,'Name')):
            corWrongNames(gradesData, Errors, everything)
        else:
            print("No Errors present. Nothing corrected")
        return
    
    
def errorExists(Errors,ErrorType):
    return (Errors['ErrorType'] == ErrorType).any()

def determineOptions(Errors,everything):
    options = []
    i = 1
    if(errorExists(Errors,'WG')):
         options += ['{}. Wrong Grade'.format(i)]
         i += 1
    if(errorExists(Errors,'ID')):
         options += ['{}. Duplicate Student ID\'s'.format(i)]
         i += 1
    if(errorExists(Errors,'Name')):
         options += ['{}. Duplicate Names'.format(i)]    
         i += 1
    options += ['{}. Everything'.format(i)]
    i += 1
    if (everything):
         options += ['{}. Go Back\n'.format(i)]
    else:
        options += ['{}. Exit to main menu\n'.format(i)]
       
    return options

def checkChoice(options,userIn):
    for i in range(len(options)):
        if str(userIn) in options[i]:
            userIn = options[i][3:]
            print("You chose",userIn)
            break
    return userIn

def deleteError(Errors,dropType):
    Errors = Errors.drop(Errors.loc[Errors['ErrorType'] == dropType].index[0])
    return Errors

def loadErrors(gradesData):
    
    colNum = len(gradesData.columns)
    studentNum = gradesData.shape[0]
    grades = [None, -3, 0, 2, 4, 7, 10, 12]
    #Check if grade exists in valid grades of "grades" array
    #nan (None) included as we wish to determine grades not in the scale, not grades missing
    #convert to list to obtain index:
    wrongGrades = ~gradesData.iloc[0:studentNum,2:colNum].isin(grades).values
    idxGrade = np.where(wrongGrades == True)
# =============================================================================
#     #Find indexes of assignments not graded:
#     noAssign = gradesData.iloc[0:studentNum,2:colNum].isnull().values
#     idxAssign = np.where(noAssign == True)
# =============================================================================
    #Find indexes for students with same StudentID's
    duplicateID =  gradesData.duplicated(['StudentID']).values
    idxID = np.where(duplicateID == True)
    duplicateName =  gradesData.duplicated(['Name']).values
    #Find indexes for students with the same Names
    idxName = np.where(duplicateName == True)
    #Store all indexes above in a pandas dataframe:
    data = []
    if (len(idxGrade[0]) > 0):
        #Wrong Grade
        data += [['WG',idxGrade]]
# =============================================================================
#     if (len(idxAssign[0]) > 0):
#         data += [['No Assignment',idxAssign]]
# =============================================================================
    if (len(idxID[0]) > 0):
        #Duplicate Student ID's
        data += [['ID',idxID]] 
    if (len(idxName[0]) > 0):
        #Name
        data += [['Name',idxName]]
    
    Errors = pd.DataFrame(data,columns = ['ErrorType','Index'])
    
    return Errors