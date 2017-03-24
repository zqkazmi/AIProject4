# assignment6

# Files

* Running the GA:
  * ga.py defines the genetic algorithm
  * run_ga.py is the file you run to use the genetic algorithm
* Fitness functions:
  * knapsack.py defines the fitness function for the knapsack problem
  * coloring.py defines the fitness function for the coloring problem
* Other:
  * greedyKnapsack.py implements the greedy algorithm for solving knapsack
  * exhaustiveKnapsack.py implements the exhaustive search to find the optimal solution to knapsack

# Running the Code
All code runs in Python 3.

To test the GA, run run_ga.py with Python 3. On my machine, that's ```python run_ga.py``` on the command line. 
Or, run the file in PyCharm.

To run greedy knapsack, run greedyKnapsack.py.

To run exhaustive search on knapsack to find the optimal solution, run exhaustiveKnapsack.py.

# Changing the Code

To change how the GA runs, you can change the parameters sent to the GA in run_ga.py

To change which problem you are solving with the GA, you have to change the fitness function. This change involves 2 steps in the code: change the import statement to the other fitness file, and change the line that calls the constructor so that "coloring" becomes the name of the fitness function you want to test with:

'''fitness_class = coloring.coloring(string_length)'''

# The Output

The console output of the GA shows the best fitness and the best string after every 25 timesteps. In the init function in ga.py you can change how frequently this is output.

The plot shows the best, average, and worst fitnesses at every generation (epoch).