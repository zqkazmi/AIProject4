
# Code from Chapter 10 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008, 2014

# Modified by Megan Olsen 2017

# A runner for the Genetic Algorithm
import ga
import pylab as pl
import coloring #import our fitness function

#Set up the GA parameters
string_length = 18 #how long the string is; coloring problem requires a set length, knapsack can use any length
epoch_count = 200 #how many times to run the GA
population_size = 50 #number of strings in population
mutation_probability = 0.001 #set to -1 to use 1/length as probability
crossover_type = 'un' #options: sp (single-point) and un (random)
elitism_count = 0 #number of strings to keep using elitism
use_tournaments = False #True or False for using tournaments when creating new generation

#set up the fitness function as an object from the knapsack class
fitness_class = coloring.coloring(string_length)

#Create the GA and run it with above parameters
ga = ga.ga(string_length,fitness_class,epoch_count,population_size,mutation_probability,crossover_type,elitism_count,
           use_tournaments,fitness_class.characters)
bestfit,averagefit,worstfit = ga.runGA()

#Create plot with fitness returned from running GA
pl.plot(list(range(len(bestfit))),bestfit,'kx-',list(range(len(averagefit))),averagefit,'ko-',list(range(len(worstfit))),worstfit,'k*-')
pl.show()
pl.pause(0)