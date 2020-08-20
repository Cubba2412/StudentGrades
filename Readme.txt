This program will process grades given to x number of students, for x number of assignments, and calculate 
the final grade which each student should recive. 
(the program can also handle missing grades, as well as a list of other errors)

The Program is run from the mainScript file
As you run that file you will be presented with a menu with 5 options.
1. Load data
2. Check Data for errors
3. Generate plots
4. Display list of grades
5. Quit

Before you load any data you will not be able to run any of the other functions in the program.

Load data
When you choose load data you will be promted to type in the name of the file that should be loaded. 
The program will only be able to load data from comma seperated value tekst files (.txt)

Check data for errors
When you choose this option you will be presented with a new menu of options for which errors you want to correct
Inside here the user is presented with a range of errors to check for and how they want them corrected
Amongst other it will check for grades not on the 7-grade scale.
Furthermore it will test for duplicate student ID's and duplicate Names (on adjacent rows)

Generate plots
Choosing this option before checking for errors in the data may effect some of the plots of which to user is also warned before choosing this option
This function will draw a bar graph over the final grades for all of the assignments. It will allso make a pointplot
that shows the distribution of grades for each assignment and the average grade per assignment.

Display list of grades
Choosing this option before checking for errors in the data may effect some of the printed data of which to user is also warned before choosing this option
Choosing this option will display an alphabetized list of all the students and all their grades, as well as the final grade 
each student should recive (based on the grades the student has recived for the assignments).

Choosing Quit will end the program 

Inside the submitted folder are two test files:
testWOErrors.txt , a large group of students without any grade outside 7-grade scale-, name- and student ID-errors.
testGradesCSV.txt , a data set in which each of the errors(that the program can check forthat the program can check for) occurs (duplicate student ID's, duplicate Names, grades outside the 7-grade scale, missing grades)




