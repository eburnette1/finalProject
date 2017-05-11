#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 09:47:47 2017
@author: Emily, Julia, Nick, the squad goals
Final Project 3: Quorum Sensing
"""
import csv 
import matplotlib.pyplot as plt  
import matplotlib.patches as mpatches

import numpy as np
import pandas as pd

class pReaction:
    def __init__(self, P, AI, k, n, beta, eta):
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        
        self.P = P
        self.AI = 0
        
    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.P = self.P + time*(self.beta*((self.AI**self.n)/(self.k**self.n+self.AI**self.n))-self.eta*self.P)
        print(self.P)
    
        
class aReaction: #class that has properties for a reaction with constant P
    def __init__(self, P, AI, epsilon, alpha): #initializing function
        self.epsilon = epsilon
        self.alpha = alpha
        
        self.P = P
        self.AI = AI

    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        #self.P = self.P - 10 #is she supposed to be -10 for each time interval?
        self.AI = self.AI + time*(self.epsilon*self.P-self.alpha*self.AI)

        
class totalReaction: #class that has properties for a reaction with both P and AI
    def __init__(self, P, AI, k, n, beta, eta, epsilon): #initializing function
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        self.epsilon = epsilon
        self.time = 0
        self.alpha = 0
        
        self.P = P
        self.AI = AI

    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        p1 = self.P    
        self.P = self.P + time*(self.beta*((self.AI**self.n)/(self.k**self.n+self.AI**self.n))-self.eta*self.P)
        self.AI = self.AI + time*(self.epsilon*p1-self.alpha*self.AI)

        self.time = self.time + time
#        self.alpha = self.time*0.01 #for linearly dependent alpha
        if self.time < 4:
            self.alpha = 0.01
        else:
            self.alpha = 0.1
#        print(self.alpha)  u can check time varying alpha here
#        print('P', self.P)
#        print('AI', self.AI)
#        


 #       print('P', self.P)
 #       print('AI', self.AI)
        
 
        
        
def rss(raw,sim):    # residual sum of squares 
    sum = 0
    for i in range(len(sim)):
        sum+= (raw[i]-sim[i])**2
        
    return sum




def main():
    
#    reactOne = pReaction(1000,1*10**(-9),3,10,3)
#    reactOneValues = []
#    while reactOne.P>1:
#        reactOneValues.append(reactOne.P)
#        reactOne.update(.1)
#    plt.plot(reactOneValues)
#    print(reactOneValues)
    
    reactTwo = totalReaction(5,0,10**(-9),3,10,3,5*10**(-10))
    reactTwoP = []
    reactTwoAI = []
    #r1 =pReaction(1000, 0,1*10**(-9), 3,10,3)
    #P=[]
    #AI = []
    
    for i in range(100):
        #AI.append(r1.AI)
        #P.append(r1.P)
        #r1.update(.1)
        reactTwoP.append(reactTwo.P)
        reactTwoAI.append(reactTwo.AI)
        reactTwo.update(.1)
    t = np.arange(0., 10, 0.1)

    plt.plot(t,reactTwoP)
    #plt.plot(P)
    plt.title('Simulated Concentration of P')
    plt.figure()
    #plt.plot(r1AI)
    plt.plot(t,reactTwoAI)
    plt.title('Simulated Concentration of AI')
    plt.figure()
    
    
    
    
    
   # print(reactTwoAI)
   # fileName = input("Input file name: ")
    infile = open('quorum.csv', 'r')
    quorum_csv = csv.reader(infile)
    next(quorum_csv) # skips first line to get rid of the headings
    print(quorum_csv)
#    
    #values taken from the CSV file
    givenTime = [];
    givenA = [];
    givenP = [];
    
    for line in infile.readlines():
        field = line.strip().split(",")
        givenTime.append(float(field[0]))
        givenA.append(float(field[1]))
        givenP.append(float(field[2]))
#
    plt.figure()
    plt.plot(givenTime,givenP)
    plt.title('given P')
    plt.figure()
    plt.plot(givenTime,givenA)
    plt.title('given A')
    plt.figure()
    
    data = {'time': givenTime, 'A' : givenA, 'P' : givenP}
    graph = pd.DataFrame(data, columns=['time', 'A', 'P'])
    outfile = open("quorumOutfile.csv", "w")     
    graph.to_csv(outfile)
#    
    #### data fit attempt ##### (not sure if do just like midterm?) look at me look at me look at me
    bRange = np.arange(1,100,10) #chose beta range <100
    eRange = np.arange(1E-10,1E-8,1E-11) #just chose small epsilon range
    rssB = []
    rssE = []
    
    for b in bRange:    # the hunt for the perfect beta
        reactThree = totalReaction(5,0,10**(-9),3,b,3,5*10**(-10))
        reactThreeP =[]
        reactThreeAI = []
        for i in range(100):
            reactThreeP.append(reactThree.P)
            reactThreeAI.append(reactThree.AI)
            reactThree.update(.1)
            
        rssB.append(rss(givenP,reactThreeP))
        
        
    bIndex = rssB.index(min(rssB))
    bFav = bRange[bIndex]
    print("B Fave = ",bFav)
    
    
     
    for e in eRange:    # the hunt for the perfect epsilon
        reactFour = totalReaction(5,0,10**(-9),3,bFav,3,e)
        reactFourP =[]
        reactFourAI = []
        for i in range(100):
            reactFourP.append(reactFour.P)
            reactFourAI.append(reactFour.AI)
            reactFour.update(.1)
            
        rssE.append(rss(givenP,reactFourP))
        
        
    eIndex = rssE.index(min(rssE))
    eFav = eRange[eIndex]
    print("E Fave = ",eFav)
    
    
    reactFix = totalReaction(5,0,10**(-9),3,bFav,3,e)
    reactFixP = []
    reactFixAI = []

    for i in range(100):
        reactFixP.append(reactFix.P)
        reactFixAI.append(reactFix.AI)
        reactFix.update(.1)

    plt.plot(t,reactFixP)
    #plt.plot(P)
    plt.title('Corrected Concentration of P')
    plt.figure()
    #plt.plot(r1AI)
    plt.plot(t,reactFixAI)
    plt.title('Corrected Concentration of AI')
    plt.figure()


#    infile.close();
main();