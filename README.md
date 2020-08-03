# Sudoku-Solver
Basically the programs in this repo are used to solve Sudoku problems. I don't think that this was a very difficult project overall. 


The backtrack.py is my implementation of the "backtracking" apprach to solving Sudoku problems which is the first (and only?) thing mentioned on the Wikipedia page for solving Sudoku problems.
What it does is it takes a .txt file where hyphens (-) represent unkown numbers and then it prints out the solution.
On my computer (which I would say is mid-upper tier?) the solution time was allways under 1.5 seconds even for the hardest problems


The backtrack_vis.py is basically the same implemetation as the backtrack.py file. The only difference is that the user is able to visualize how the backtracking works.
To do this I used pygame, and also allowed the user to input the numbers in and then kick s to solve, or r to restart. You can also use text files to set up the Sudoku board,
but you have to uncomment it in the code. 
The solution time for this was actually really slow. I think that the minimum time for my computer was 20 minutes.


I think that I may add additional logic to speed up the task so that the visualization process can be faster as well.
