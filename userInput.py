# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:51:10 2020

@author: ThomasBirk
"""

def inputChoiceStr(prompt, inputType):
    # inputChoiceStr prompts the user for string input
    # Usage: choice = inputChoiceStr(prompt,inputType)
    ##
    # Input: prompt: what question is presented to user
    #        inputType: used for validation criteria for specific question
    # Output: The user inputted string 
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    # Continously prompt the user for a string input 
    while True:
        try:
            string = input(prompt)
            if string.isdigit():
                pass
                print("Please enter a valid string")
            elif((len(string) < 7) or (string[0] != 's')) and (inputType == "StudentID"):
                pass
                print("Please enter a valid 6 digit student number with the prefix 's' (example s123456)")
            elif not(' ' in string) and (inputType == "Name"):
               pass
               print("Please enter a first and last name of the student, seperated by a space")
            else:
                break
        except ValueError:
            pass
    return string

def inputChoiceNum(prompt, inputType):
    # inputChoiceNum prompts the user for integer input
    # Usage: choice = inputChoicenum(prompt,inputType)
    ##
    # Input: prompt: what question is presented to user
    #        inputType: used for validation criteria for specific question
    # Output: The user inputted integer 
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    
    # Continously prompt the user for a number untill a valid option has been given
    while True:
        try:
            num = int(input(prompt))
            #Only allow user to choose a valid option
            if not(0 < num < 7) and (inputType == "Data Check"):
                pass
                print("Please enter a number between 1 and 6")
            #Only allow a yes or no
            elif not(0 <= num <= 1) and (inputType == "Y/N"):
                 pass
                 print("Please enter a valid option (No: 0, Yes: 1) ")
            else:
                break
        except ValueError:
            pass
            print("Please enter a number")
    return num


def printMenu():
    # printMenu() prints the main menu options to the user
    # Usage: printMenu()
    ##
    ##
    # Author: Thomas B. Frederiksen s183729@student.dtu.dk, 2020
    print("1. Load new data.")
    print("2. Check for data errors.")
    print("3. Generate plots.")
    print("4. Display list of grades.")
    print("5. Quit.")
    return
