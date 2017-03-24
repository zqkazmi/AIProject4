# This code implements the map coloring problem from Chapter 10 of Marsland

# Code written by Megan Olsen 2017

# A class for a specific 3-coloring  problem
import numpy as np
import random
import sys

class coloring:
    #Initialize the map and colors
    def __init__(self,string_length):
        if string_length!= 18:
            print("To run map coloring, the string length must be 13")
            sys.exit(-1)
        self.string_length = string_length

        self.characters = [0,1,2] #the characters representing the possible colors. must be numbers.

        #Boundaries with all higher numbered boxes, to prevent double counting
        self.boundaries = [[1,4,5],[5,6,2],[6,7,3],[7,8],
                            [5,9],[6,9,10],[7,10,11],[8,11,12],[12],
                            [10,13,14],[11,14,15],[12,15,16],[16,17],
                            [14],[15],[16],[17],[]]
        print("Max fitness is 38")

    #Calculate the fitness of each element of a given population
    def fitness(self,pop):
        fitness = np.zeros(pop.shape[0]) #create array to hold fitness

        #Calculate each individual's fitness by number of correct boundaries
        for i in range(pop.shape[0]): #for each string in population by index
            for j in range(len(pop[i])): #for each character in string by index
                for boundary in self.boundaries[j]: #for each index that bounds it
                    #if in population i the colors don't match between box j and boundary box, count it
                    if pop[i][j] != pop[i][boundary]:
                        fitness[i] += 1

        return fitness
