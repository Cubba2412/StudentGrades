
import numpy as np




def sortByName(grades):
    
    #Sorts by the second coloumn 
    grades = grades[np.argsort(grades[:, 1])]

    
    return grades




grades = list(sortByName(np.array([[12,  "Hans",  7, 12,  2,  7, 10,  1],
                                   [10,  "Jesper",  2,  4,  4,  4,  7,  5],
                                   [ 7,  "Kim",  4,  2, 11, 10,  4,  3],
                                   [ 4,  "Albert",  2, 12,  4,  7,  7,  4],
                                   [ 2,  "Torben",  0,  2,  None, -3,  7,  2],
                                   [ 7,  "Oliver",  0,  4,  4,  7,  7,  6],
                                   [ 7,  "Peter", 10, 10,  7,  7, 10,  7]])))

for i in range(len(grades)):
    print(grades[i])










