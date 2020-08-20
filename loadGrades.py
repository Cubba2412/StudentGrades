import pandas as pd
from userInput import *
import os.path
import numpy as np
#Suppress pandas warnings from user
pd.set_option('mode.chained_assignment', None)

def loadGrades():
    # loadGrades Loads in a CSV file containing N x M data values and
    # returns it as pandas dataframe
    ##
    # Usage: gradesData, dataLoaded, colNum, studentNum = loadGrades()
    ##
    # Output data: N x M pandas dataframe with student data and grades in the  
    # CSV file given
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
   
    
    #Get number of columns and students to return to main script
    colNum = len(gradesData.columns)
    studentNum = gradesData.shape[0]

    return gradesData, dataLoaded, colNum, studentNum


def checkData(gradesData):
    # checkData allows the user to check for various error in the loaded CSV file
    ##
    # Usage: Errors = checkData(gradesData)
    ##
    # Input: gradesData: N x M pandas dataframe with student data and grades
    # Output data: An updated N x 2 pandas dataframe with Error types as well as   
    # the indexes in the given "gradesData" where they are located
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    dataChecked = False
    everything = False
    while True:
        Errors = loadErrors(gradesData)
        #Prompt user for what errors they wish to see.
        #Varies depending on previous choices and errors present in data
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
                        #Inform user of which assignment for which student, 
                        #has a wrong grade with index data from Errors dataframe
                        print("The grade ({}) for student {} with ID {} of \"{}\" is not on the 7 step scale".format(*getPrintData(gradesData, Errors, 'WG', i)))
                if(errorExists(Errors,'ID')):
                    for i in range(len(getNumErrors(Errors, 'ID',False))):
                        #Inform user of which students have the same student ID
                        print("The studentID for student \"{}\" is the same as for student \"{}\"".format(*getPrintData(gradesData,Errors,'ID',i)))
                if(errorExists(Errors,'Name')):
                    for i in range(len(getNumErrors(Errors, 'Name',False))):
                        #Inform user of which students have the same name
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
    # getErrIdxList creates a list of the Error types to get print data for
    ##
    # Usage: ErrIdxList = getErrIdxList(ErrorType)
    ##
    # Input: type of Error in question
    # Output data: list of strings / chars used for which Errortype to locate
    # in the Errors dataframe
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    
    #Wrong Grades
    if(ErrorType == 'WG'):
        ErrIdxList = ['G','N','ID','A']
    #Duplicate ID    
    elif(ErrorType == 'ID'):
        ErrIdxList = ['N','N']
    #Duplicate Name
    elif(ErrorType == 'Name'):
        ErrIdxList = ['ID','ID']
    return ErrIdxList
    

def getPrintData(gradesData,Errors,ErrorType,i):
    # getPrintData creates a list of the Error types to get print data for
    ##
    # Usage: stringValues = getErrIdxList(ErrorType)
    ##
    # Input: gradesData: N x M pandas dataframe with student data and grades
    #        Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        ErrorType: Type of Error in question
    #        i = iterator of for loop
    # Output data: list of strings to print with str.format
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
    # printOptions prints the users options
    ##
    # Usage: printOptions(options)
    ##
    # Input: options = list of string options to print
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    print("\nOptions: ")
    for i in options:
        print(i)
    return

def getNumErrors(Errors,ErrorType,change):
    # getNumErrors finds the index in gradesData of the given error
    ##
    # Usage: num = getNumErrors(Errors,ErrorType,change)
    ##
    # Input: Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        ErrorType: Type of Error in question
    #        change: is the index used for changing a value or simply accessing
    #        an index
    # Output data: index or list of indexes (depending on the bool change)
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    if not(change):
        num = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1][0]
    else:
        num = Errors.loc[Errors['ErrorType'] == ErrorType].iloc[0][1]
    return num
    
def corWrongGrades(gradesData,Errors,everything):
    # corWrongGrades corrects the wrong grades found in the gradesData given
    ##
    # Usage: corWrongGrades(gradesData,Errors,everything)
    ##
    # Input: gradesData:  N x M pandas dataframe with student data and grades
    #        Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        everything: bool value indicating if the option "check everything"
    #        was chosen. Terminal output varies depending on this
    #        The user is prompted throughout the function about how they want 
    #        the data corrected
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
                #Remove grade by setting to nan
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
    # corWrongNames corrects the duplicate names found in the gradesData given
    ##
    # Usage: corWrongNames(gradesData,Errors,everything)
    ##
    # Input: gradesData:  N x M pandas dataframe with student data and grades
    #        Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        everything: bool value indicating if the option "check everything"
    #        was chosen. Terminal output varies depending on this
    #        The user is prompted throughout the function about how they want 
    #        the data corrected
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
                #Change name to users input
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
                    #Find row to remove
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
    # corWrongID corrects the duplicate student ID'sfound in the gradesData given
    ##
    # Usage: corWrongID(gradesData,Errors,everything)
    ##
    # Input: gradesData:  N x M pandas dataframe with student data and grades
    #        Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        everything: bool value indicating if the option "check everything"
    #        was chosen. Terminal output varies depending on this
    #        The user is prompted throughout the function about how they want 
    #        the data corrected
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
                #Change ID to what was given by the user
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
                    #Get row to remove
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
    # corEverything corrects all errors found in the gradesData given.
    ##
    # Usage: corWrongGrades(gradesData,Errors,everything)
    ##
    # Input: gradesData:  N x M pandas dataframe with student data and grades
    #        Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        everything: bool value indicating if the option "check everything"
    #        was chosen. Terminal output varies depending on this
    #        The user is prompted throughout the function about how they want 
    #        the data corrected
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
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
    # errorExists checks if an of error of the given Errorytype in the data
    # Usage: errorExists(Errors,ErrorType)
    ##
    # Input: Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        ErrorType: Type of Error in question
    # Output: Bool value indiciating if the error exists
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    return (Errors['ErrorType'] == ErrorType).any()

def determineOptions(Errors,everything):
    # determineOptions determines which options of datacheck the user has
    #                  depending of which errors are present
    # Usage: options = determineOptions(Errors,ErrorType)
    ##
    # Input: Errors:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        ErrorType: Type of Error in question
    # Output: Bool value indiciating if the error exists
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    options = []
    i = 1
    #Wrong Grade
    if(errorExists(Errors,'WG')):
         options += ['{}. Wrong Grade'.format(i)]
         i += 1
    #Duplicate ID
    if(errorExists(Errors,'ID')):
         options += ['{}. Duplicate Student ID\'s'.format(i)]
         i += 1
    #Duplicate Name
    if(errorExists(Errors,'Name')):
         options += ['{}. Duplicate Names'.format(i)]    
         i += 1
    options += ['{}. Everything'.format(i)]
    i += 1
    #Option to go back to options when "everything" option previously chosen
    if (everything):
         options += ['{}. Go Back\n'.format(i)]
    else:
        options += ['{}. Exit to main menu\n'.format(i)]
       
    return options

def checkChoice(options,userIn):
    # checkChoice determines which option the user chose
    # Usage: userIn = determineOptions(options,userIn)
    ##
    # Input: Options: list of string options   
    #        userIn: the choice of the user (integer value)
    # Output: String corresponding to the users choice
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    for i in range(len(options)):
        if str(userIn) in options[i]:
            #Remove number in string and get raw string choice
            userIn = options[i][3:]
            print("You chose",userIn)
            break
    return userIn

def deleteError(Errors,dropType):
    # deleteError deletes an Error from the Error dataframe of the given 
    #             Errorytype
    # Usage: detleteError(Errors,ErrorType)
    ##
    # Input: Errors:N x 2 pandas dataframe with with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    #        ErrorType: Type of Error in question
    # Output:An updated N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    Errors = Errors.drop(Errors.loc[Errors['ErrorType'] == dropType].index[0])
    return Errors

def loadErrors(gradesData):
    # loadErrors locates the Errors found in the given gradesData dataframe
    # Usage: Errors = loadErrors(gradesData)
    ##
    # Input: gradesData:  N x M pandas dataframe with student data and grades 
    # Output:N x 2 pandas dataframe with Error types as well as   
    #        the indexes in the given "gradesData" where they are located 
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    
    colNum = len(gradesData.columns)
    studentNum = gradesData.shape[0]
    grades = [None, -3, 0, 2, 4, 7, 10, 12]
    #Check if grade exists in valid grades of "grades" array
    #nan (None) included as we wish to determine grades not in the scale, not grades missing
    #convert to list to obtain index:
    wrongGrades = ~gradesData.iloc[0:studentNum,2:colNum].isin(grades).values
    idxGrade = np.where(wrongGrades == True)

    #Find indexes for students with same StudentID's
    duplicateID =  gradesData.duplicated(['StudentID']).values
    idxID = np.where(duplicateID == True)
    #Find indexes for students with the same Names
    duplicateName =  gradesData.duplicated(['Name']).values
    idxName = np.where(duplicateName == True)
    
    #Store all indexes above in a pandas dataframe:
    data = []
    if (len(idxGrade[0]) > 0):
        #Wrong Grade
        data += [['WG',idxGrade]]
    if (len(idxID[0]) > 0):
        #Duplicate Student ID's
        data += [['ID',idxID]] 
    if (len(idxName[0]) > 0):
        #Name
        data += [['Name',idxName]]
    
    Errors = pd.DataFrame(data,columns = ['ErrorType','Index'])
    
    return Errors