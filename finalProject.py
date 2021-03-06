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
    def __init__(self, P, AI, k, n, beta, eta):
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        
        self.P = P
        self.AI = 0
        
    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.P = self.P + time*(self.beta*((self.AI**self.n)/(self.k**self.n+self.AI**self.n))-self.eta*self.P)
        
    
        
class aReaction: #class that has properties for a reaction with constant P
    def __init__(self, P, AI, epsilon, alpha): #initializing function
        self.epsilon = epsilon
        self.alpha = alpha
        
        self.P = P
        self.AI = AI

    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.AI = self.AI + time*(self.epsilon*self.P-self.alpha*self.AI)
        #self.P = self.P-10 #we had a bit of a disagreement about what part 3 was asking, whether it was a constant P or an independently decreasing concentration of P. Uncommented code is with constant P, uncomment this line for independent decrease.
        

        
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
        
        #time-varying alpha, part 4
        self.time = self.time + time
        if self.time < 4:
            self.alpha = 0.01
        else:
            self.alpha = 0.1



#        
def rss(list1,list2): 
    rssError = 0
    for i in range(len(list1)):
        rssError += (list1[i] - list2[i])**2
    return rssError




def main():
    print("Final Project 3, by Emily Burnette, Nick Garza, and Julia Costacurta")
#below is for part 1 of the prompt; finding a P graph without any AI feedback
#should be decreasing since the first term in the equation goes to 0 when AI = 0, which is what's asked here.
    r1 =pReaction(10, 0,1*10**(-9), 3,10,3)
    P=[]
    
    for i in range (101):
       P.append(r1.P)
       r1.update(.1)
    t = np.arange(0., 10.1, 0.1)
    
    plt.plot(t,P)
    plt.title('Part 1 - Just P Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [P] (M) ")
    plt.figure()

    
#below is for part 2 of the prompt, finding P and AI values with an epsilon of 5e-10 and alpha of .1. The independent concentration of P is commented out above so it doesn't mess with other stuff
    reactAI = aReaction(5,0,3,5*10**(-10)) 
    reactAIP = []
    reactAIAI = []

    for i in range(101):
        reactAIP.append(reactAI.P)
        reactAIAI.append(reactAI.AI)
        reactAI.update(.1)
    t = np.arange(0., 10.1, 0.1)
    
    plt.plot(t,reactAIP)
    plt.title('Part 2 - Constant P, P Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [P] (M) ")
    plt.figure()
    
    plt.plot(t,reactAIAI)
    plt.title('Part 2 - Constant P, AI Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [A]] (M) ")
    plt.figure()
    

# Graphing part 3
    reactLow = totalReaction(5,0,10**(-9),3,10,3,5*10**(-10)) #low initial P
    reactLowP = []
    reactLowAI = []

    for i in range(101):
        reactLowP.append(reactLow.P)
        reactLowAI.append(reactLow.AI)
        reactLow.update(.1)
    t = np.arange(0., 10.1, 0.1)
    
    
    reactHigh = totalReaction(100,0,10**(-9),3,10,3,5*10**(-10)) #high initial P
    reactHighP = []
    reactHighAI = []

    for i in range(101):
        reactHighP.append(reactHigh.P)
        reactHighAI.append(reactHigh.AI)
        reactHigh.update(.1)
    t = np.arange(0., 10.1, 0.1)
    
    #low P
    plt.plot(t,reactLowP)
    plt.title('Part 3 - Low P, P Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration (P) (M) ")
    plt.figure()
    
    #high P
    plt.plot(t,reactHighP)
    plt.title('Part 3 - High P, P Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [P] (M) ")
    plt.figure()
    
    #low P AI graph
    plt.plot(t,reactLowAI)
    plt.title('Part 3 - Low P, AI Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [A] (M)")
    plt.figure()
    
    #high P AI Graph
    plt.plot(t,reactHighAI)
    plt.title('Part 3 - High P, AI Graph')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [A] (M) ")
    
#part 5 of the prompt, finding best fits of epsilon and beta to match to the given graphs
    fileName = 'quorum.csv'
    infile = open(fileName, 'r')

    infile = open('quorum.csv', 'r')

    quorum_csv = csv.reader(infile)
    next(quorum_csv) # skips first line to get rid of the headings
    
    #values taken from the CSV file
    givenTime = [];
    givenA = [];
    givenP = [];
    
    
    for line in infile.readlines():
        field = line.strip().split(",")
        givenTime.append(float(field[0]))
        givenA.append(float(field[1]))
        givenP.append(float(field[2]))


#plotting given AI and P values        
    #plt.figure()
    #plt.plot(givenTime,givenP)
    #plt.title('given P')
    #plt.xlabel("Time (seconds)")
    #plt.ylabel("Concentration (P) ")
    #plt.figure()
    #plt.plot(givenTime,givenA)
    #plt.title('given A')
    #plt.xlabel("Time (seconds)")
    #plt.ylabel("Concentration (A) ")
    
    data = {'time': givenTime, 'A' : givenA, 'P' : givenP}
    graph = pd.DataFrame(data, columns=['time', 'A', 'P'])
    outfile = open("quorumOutfile.csv", "w")     
    graph.to_csv(outfile)
    

    infile.close();



    
# Finding best Epsilon value
    best2 = rss(reactLowAI,givenA)
    for i in np.arange(1*10**(-11),1*10**(-9),1*10**(-12)):
        reacti = totalReaction(5,0,10**(-9),3,10,3,i)
        A = []
        for j in range(101):
            A.append(reacti.AI)
            reacti.update(0.1)
        if rss(A,givenA)< best2:
            best2 = rss(A,givenA)
            bestEpsilon = i
    print("The best epsilon is", bestEpsilon)
    
#Finding best Beta value
    best = rss(reactLowP,givenP)
    for i in np.arange(0,20,0.1):
        reacti = totalReaction(5,0,10**(-9),3,i,3,bestEpsilon)
        P = []
        for j in range(101):
            P.append(reacti.P)
            reacti.update(0.1)
        if rss(P,givenP)<best:
            best = rss(P,givenP)
            bestBeta = i
    print("The best beta is", bestBeta)
    
    
 #simulating using best Beta and Epsilon values
    reactTotal = totalReaction(5,0,10**(-9),3,bestBeta,3,bestEpsilon)
    reactTotalP = []
    reactTotalAI = []
    for i in range(101):
        reactTotalP.append(reactTotal.P)
        reactTotalAI.append(reactTotal.AI)
        reactTotal.update(.1)
    
        

#Graph comparing given and optimized P values
    plt.figure()
    plt.plot(t, reactTotalP, 'b--', t, givenP, 'r')
    plt.title('Part 5 - Given and Optimized P')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [P] (M) ")
    blue_patch = mpatches.Patch(color='blue', label='Optimized P')
    red_patch = mpatches.Patch(color='red', label='Given P')
    plt.legend(handles=[blue_patch, red_patch])
    
    
#Graph comparing given and optimized AI values    
    plt.figure()
    plt.plot(t, reactTotalAI, 'g--', t, givenA, 'r')
    plt.title('Part 5 - Given and Optimized A')
    plt.xlabel("Time (seconds)")
    plt.ylabel("Concentration [A] (M) ")
    green_patch = mpatches.Patch(color='green', label='Optimized A')
    red_patch = mpatches.Patch(color='red', label='Given A')
    plt.legend(handles=[green_patch, red_patch])
main();

