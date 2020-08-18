# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 09:51:10 2020

@author: ThomasBirk
"""

def inputChoiceStr(prompt):
    # Continously prompt the user for a string input 
    while True:
        try:
            string = input(prompt)
            if string.isdigit():
                pass
                print("Please enter a valid string")
            else:
                break
        except ValueError:
            pass
    return string

def inputChoiceNum(prompt, inputType):
    # Continously prompt the user for a number untill a valid option has been given
    
    while True:
        try:
            num = int(input(prompt))
            if not(0 < num < 7) and (inputType == "Data Check"):
                pass
                print("Please enter a number between 1 and 6")
# =============================================================================
#             elif not(0 < num < 5) and (inputType == "Bacteria"):
#                 pass
#                 print("Please enter a number between 1 and 4")
            elif not(0 <= num <= 1) and (inputType == "Y/N"):
                 pass
                 print("Please enter a valid option (No: 0, Yes: 1) ")
#             elif not(0<= num <=1) and (inputType == "Limit"):
#                 pass
#                 print("Please enter a valid growth rate limit (between 0 and 1)")
#             elif not(1<= num <=2) and (inputType == "Filtered data"):
#                 pass
#                 print("Please enter a valid plot option: \n1: Plot original data \n2: Plot Filtered data")
            else:
# =============================================================================
                break
        except ValueError:
            pass
            print("Please enter a number")
    return num


def printMenu():
    print("1. Load new data.")
    print("2. Check for data errors.")
    print("3. Generate plots.")
    print("4. Display list of grades.")
    print("5. Quit.")
    return
