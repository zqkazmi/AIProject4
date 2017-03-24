
# Code from Chapter 10 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008, 2014

# Extended by Megan Olsen 2017
# The Genetic algorithm
# Comment and uncomment fitness functions as appropriate (as an import and the fitnessFunction variable)

import pylab as pl
import numpy as np
#import knapsack as fF

class ga:

    def __init__(self,stringLength,fitness_object,nEpochs,populationSize=100,mutationProb=-1,crossover='un',nElite=4,tournament=True,characters=[0,1]):
        """ Constructor"""
        self.stringLength = stringLength
        self.printrate = 25 #how often best fitness is output

        # Population size should be even
        if np.mod(populationSize,2)==0:
            self.populationSize = populationSize
        else:
            self.populationSize = populationSize+1

        if mutationProb < 0:
             self.mutationProb = 1/stringLength
        else:
             self.mutationProb = mutationProb

        self.nEpochs = nEpochs

        self.problem = fitness_object
        self.characters = characters

        self.crossover = crossover
        self.nElite = nElite
        self.tournment = tournament

        #creates population as random strings of characters from the characters list
        self.population = np.random.choice(characters,self.stringLength*self.populationSize)
        self.population = np.reshape(self.population,(self.populationSize,self.stringLength))
        print("epoch\tfitness\tbest string")#header for future output

    def runGA(self):
        """The basic loop"""
        bestfit = np.zeros(self.nEpochs)
        averagefit = np.zeros(self.nEpochs)
        worstfit = np.zeros(self.nEpochs)

        for i in range(self.nEpochs):
            # Compute fitness of the population
            fitness = self.problem.fitness(self.population)

            # Pick parents -- can do in order since they are randomised
            newPopulation = self.fps(self.population,fitness)

            # Apply the genetic operators
            if self.crossover == 'sp':
                newPopulation = self.spCrossover(newPopulation)
            elif self.crossover == 'un':
                newPopulation = self.uniformCrossover(newPopulation)
            newPopulation = self.mutate(newPopulation)

            # Apply elitism and tournaments if using
            if self.nElite>0:
                newPopulation = self.elitism(self.population,newPopulation,fitness)

            if self.tournament:
                newPopulation = self.tournament(self.population,newPopulation,fitness)

            self.population = newPopulation
            bestfit[i] = fitness.max()
            averagefit[i] = np.average(fitness)
            worstfit[i] = fitness.min()

            if (np.mod(i,self.printrate)==0):
                print( i, fitness.max(), self.population[np.argmax(fitness)],sep="\t")

        return bestfit,averagefit,worstfit #return fitness from all epochs


    ''' choose parents with fitness proportional selection '''
    def fps(self,population,fitness):

        # Scale fitness by total fitness
        fitness = fitness/np.sum(fitness)
        fitness = 10*fitness/fitness.max()

        # Use "roulette selection" approach
        # Put repeated copies of each string in according to fitness
        # Deal with strings with very low fitness
        j=0
        while np.round(fitness[j])<1:
            j = j+1

        newPopulation = np.kron(np.ones((np.round(fitness[j]),1)),population[j,:])

        # Add multiple copies of strings into the newPopulation
        for i in range(j+1,self.populationSize):
            if np.round(fitness[i])>=1:
                newPopulation = np.concatenate((newPopulation,np.kron(np.ones((np.round(fitness[i]),1)),population[i,:])),axis=0)

        # Shuffle the order (note that there are still too many)
        indices = list(range(np.shape(newPopulation)[0]))
        np.random.shuffle(indices)
        newPopulation = newPopulation[indices[:self.populationSize],:]
        return newPopulation

    def spCrossover(self,population):
        # Single point crossover
        newPopulation = np.zeros(np.shape(population))
        crossoverPoint = np.random.randint(0,self.stringLength,self.populationSize)
        for i in range(0,self.populationSize,2):
            newPopulation[i,:crossoverPoint[i]] = population[i,:crossoverPoint[i]]
            newPopulation[i+1,:crossoverPoint[i]] = population[i+1,:crossoverPoint[i]]
            newPopulation[i,crossoverPoint[i]:] = population[i+1,crossoverPoint[i]:]
            newPopulation[i+1,crossoverPoint[i]:] = population[i,crossoverPoint[i]:]
        return newPopulation

    def uniformCrossover(self,population):
        # Uniform crossover
        newPopulation = np.zeros(np.shape(population))
        which = np.random.rand(self.populationSize,self.stringLength)
        which1 = which>=0.5
        for i in range(0,self.populationSize,2):
            newPopulation[i,:] = population[i,:]*which1[i,:] + population[i+1,:]*(1-which1[i,:])
            newPopulation[i+1,:] = population[i,:]*(1-which1[i,:]) + population[i+1,:]*which1[i,:]
        return newPopulation

    def mutate(self,population):
        # Mutation
        whereMutate = np.random.rand(np.shape(population)[0],np.shape(population)[1])
        #population[np.where(whereMutate < self.mutationProb)] = 1 - population[np.where(whereMutate < self.mutationProb)]
        population[np.where(whereMutate < self.mutationProb)] = np.random.choice(self.characters)
        return population

    def elitism(self,oldPopulation,population,fitness):
        best = np.argsort(fitness)
        best = np.squeeze(oldPopulation[best[-self.nElite:],:])
        indices = list(range(np.shape(population)[0]))
        np.random.shuffle(indices)
        population = population[indices,:]
        population[0:self.nElite,:] = best
        return population

    def tournament(self,oldPopulation,population,fitness):
        newFitness = self.problem.fitness(population)
        for i in range(0,np.shape(population)[0],2):
            f = np.concatenate((fitness[i:i+2],newFitness[i:i+2]),axis=0)
            indices = np.argsort(f)

            # if the best ones are the original parents, keep them instead of children
            if indices[-1]<2 and indices[-2]<2:
                population[i,:] = oldPopulation[i,:]
                population[i+1,:] = oldPopulation[i+1,:]
            #otherwise, if best one is original, figure out which child to replace
            elif indices[-1]<2:
                if indices[0]>=2:
                    population[i+indices[0]-2,:] = oldPopulation[i+indices[-1]]
                else:
                    population[i+indices[1]-2,:] = oldPopulation[i+indices[-1]]
            elif indices[-2]<2:
                if indices[0]>=2:
                    population[i+indices[0]-2,:] = oldPopulation[i+indices[-2]]
                else:
                    population[i+indices[1]-2,:] = oldPopulation[i+indices[-2]]
        return population

