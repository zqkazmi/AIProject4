
# Code from Chapter 10 of Machine Learning: An Algorithmic Perspective (2nd Edition)
# by Stephen Marsland (http://stephenmonika.net)

# You are free to use, change, or redistribute the code in any way you wish for
# non-commercial purposes, but please maintain the name of the original author.
# This code comes with no warranty of any kind.

# Stephen Marsland, 2008, 2014

# Modified by Megan Olsen 2017

# A class for the Knapsack problem
import numpy as np
import random

class knapsack:
	#Initialize the item sizes and max size of the knapsack
	def __init__(self,string_length):
		self.characters=[0,1]
		sizelist = []
		self.maxSize = 500

		#create a random set of items of sizes between 10 and max
		for i in range(string_length):
			sizelist.append(random.uniform(10,self.maxSize/2))
		self.sizes = np.array(sizelist)

		#print "sizes are:" 
		#print '[%s]' % ', '.join(map(str, sizelist))
		

	#Calculate the fitness of each element of a given population
	def fitness(self,pop):
		
	 	#sizes = np.array([109.60,125.48,52.16,195.55,58.67,61.87,92.95,93.14,155.05,110.89,13.34,132.49,194.03,121.29,179.33,139.02,198.78,192.57,81.66,128.90])

	 	#Calculate each individual's fitness by size * if its included
		fitness = np.sum(self.sizes*pop,axis=1)

		#For any fitness > max, decrease by 2 * amount_over
		#print fitness
		fitness = np.where(fitness>self.maxSize,self.maxSize-2*(fitness-self.maxSize),fitness)
		#print fitness

		return fitness
