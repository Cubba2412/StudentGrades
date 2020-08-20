

import numpy as np
import matplotlib.pylab as plt
import matplotlib.collections as mc
import pandas as pd




# gradesPlot creates and draws plots for final grades and per assignment
#
# input: grades(a matrix of size NxM)
# Usage: creates plots
#
# Author: Henrik Riise Nielsen, s183693@student.dtu.dk, 2020
def gradesPlot(grades):
    
    
    
    #######################################################################################
    #Here we do the setup necessary to be able to do the other parts in a clean neat way.
    example = np.array([-3, 0, 2, 4, 7, 10, 12])                               #creates a referencelist of the different grades. 
    labels= np.array(["-3", "00", "02", "4", "7", "10", "12"])                 #Creates a list of names to be used on the axis.
    grades[grades == np.nan]=42                                                 #Replace all None-values with an unused value
     
    
    hist = np.array([np.count_nonzero(grades[:,0: len(grades[0])-1] == example[0]),    #Looks through the data except for the 
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[1]),    #last coloumn where the amount of finished
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[2]),    #assignments are stored.
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[3]),
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[4]),
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[5]),
                     np.count_nonzero(grades[:,0: len(grades[0])-1] == example[6])])
    #######################################################################################




    #######################################################################################
    #This part of the function creates the bargraph of the Final grades.
    fig, ax=plt.subplots()                      #starts a new figure.
    ax.bar(range(1,8), hist)                    #loades in the data.
    ax.set_xticks(range(1,8))
    ax.set_xticklabels(labels)
    ax.set_title("Final Grades")
    ax.set_ylabel("Amount of students")
    ax.set_xlabel("Grade")
    plt.show()                                  #Display the firgure
    #######################################################################################
   
    

    
    
    #########################################################################################
    #This part of the function creates the pointplot with markers for the average for each assignment
    assignments=max(grades[:,len(grades[0])-1])
    x = np.arange(0,assignments)
    
    fig, pp=plt.subplots()                                      #Starts a new figure.
    pp_lab=[]                                                   #creates an empty array, for use in nameing the x-axis.
    for i in x:                                                 
        i = int(i)                                              #Cast i from float to int
        pp_lab=np.append(pp_lab,("Assignment " + str(int(x[i]+1))))  #Adds a new name to the array.
        summa=0
        length=0
        for j in range(len(grades)):
            if(any(grades[j,i]==example)):
                pp.plot(x[i],(grades[j,i]+(0.1*(np.random.randint(-1,1)*j))), 'o')  #draws one point in with a random ofset proportional to position in the "example"-array. 
                summa=summa+grades[j,i]                         #sums op the valid values
                length = length+1                               #increments the valid length of this part of the array
            
        avrg = (summa/length)                                   #calculates the average for a specific assignment.
        lines = [[(-0.4+i, avrg), (0.4+i, avrg)]]               #finds the endpoint of the line-marker of the average.
        lc = mc.LineCollection(lines, linewidths=2)             #Creates the lines.
        pp.text(i+0.2,avrg+0.2, "%.2f" % round(avrg, 2))
        pp.add_collection(lc)
            
    
    
    pp.set_xticks(x)
    pp.set_xticklabels(pp_lab)
    pp.set_yticklabels(labels)
    pp.set_yticks(example)
    pp.grid(color='grey', linewidth=0.2)
    pp.set_title("Grades per assignment")
    
    plt.xticks(rotation = 35)
    plt.show()
    ########################################################################################## 


    return







gradesPlot(np.array([[12,  4,  7, 12,  2,  7, 10,  1],
                     [10,  4,  2,  4,  4,  4,  7,  2],
                     [ 7,  2,  4,  2, 11, 10,  4,  3],
                     [ 4,  4,  2, 12,  np.nan,  7,  7,  4],
                     [ 2,  4,  0,  2,  4, -3,  7,  5],
                     [ 7,  0,  0,  4,  4,  7,  7,  6],
                     [ 7,  4, 10, 10,  7,  7, 10,  7]]))

"""
a = np.array([[ 7.,  4.,  -3., 3], [12.,  np.nan,  np.nan, 1], [10.,  4., np.nan, 2], [10., 12.,  2., 3]])
gradesPlot(a)
"""













