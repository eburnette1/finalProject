#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 09:47:47 2017

@author: Emily, Julia, Nick

Final Project 3: Quorum Sensing
"""
import csv 
import matplotlib.pyplot as plt  
import matplotlib.patches as mpatches

import numpy as np
import pandas as pd

class pReaction:
    def __init__(self, P, k, n, beta, eta):
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        
        self.P = P
        self.AI = 0
        
    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.P = self.P + time*(-self.eta*self.P)
        print(self.P)
    
class totalReaction: #class that has properties for a reaction with both P and AI
    def __init__(self, P, AI, k, n, beta, eta, epsilon, alpha): #initializing function
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        self.epsilon = epsilon
        self.alpha = alpha
        
        self.P = P
        self.AI = AI

    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.P = self.P + time*(self.beta*((self.AI**self.n)/(self.k**self.n+self.AI**self.n))-self.eta*self.P)
        self.AI = self.AI + time*(self.epsilon*self.P-self.alpha*self.AI)




def main():
    
    reactOne = pReaction(1000,1*10**(-9),3,10,3)
    reactOneValues = []
    while reactOne.P>1:
        reactOneValues.append(reactOne.P)
        reactOne.update(.1)
    plt.plot(reactOneValues)
    print(reactOneValues)
#    fileName = input("Input file name: ")
#    infile = open(fileName, 'r')
#    quorum_csv = csv.reader(infile)
#    next(quorum_csv) # skips first line to get rid of the headings
#    print(quorum_csv)
#    
#    #values taken from the CSV file
#    givenTime = [];
#    givenA = [];
#    givenP = [];
#    
#    for line in infile.readlines():
#        field = line.strip().split(",")
#        givenTime.append(float(field[0]))
#        givenA.append(float(field[1]))
#        givenP.append(float(field[2]))
#
#    data = {'time': givenTime, 'A' : givenA, 'P' : givenP}
#    graph = pd.DataFrame(data, columns=['time', 'A', 'P'])
#    outfile = open("quorumOutfile.csv", "w")     
#    graph.to_csv(outfile)
#    
#    infile.close();
main();
