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

class reaction: #class that has properties for a single reaction
    def __init__(self, k, n, beta, eta, epsilon, alpha): #initializing function
        self.k = k
        self.n = n
        self.beta = beta
        self.eta = eta
        self.epsilon = epsilon
        self.alpha = alpha
        
        self.P = 0
        self.AI = 0

    def setConc(self,P,AI):
        self.P = P
        self.AI = AI
  
    def update(self, time): #function to update concentrations of chemicals for a time interval (time)
        self.P = self.P + time*beta((self.AI**self.n)/(self.k**n+self.AI**n))
        self.AI = self.AI + time*(self.epsilon*self.P-self.alpha*self.AI)


def main():
    
    fileName = input("Input file name: ")
    infile = open(fileName, 'r')
    quorum_csv = csv.reader(infile)
    next(quorum_csv) # skips first line to get rid of the headings
    print(quorum_csv)
    
    #values taken from the CSV file
    givenTime = [];
    givenA = [];
    givenP = [];
    
    for line in infile.readlines():
        field = line.strip().split(",")
        givenTime.append(float(field[0]))
        givenA.append(float(field[1]))
        givenP.append(float(field[2]))

    data = {'time': givenTime, 'A' : givenA, 'P' : givenP}
    graph = pd.DataFrame(data, columns=['time', 'A', 'P'])
    outfile = open("quorumOutfile.csv", "w")     
    graph.to_csv(outfile)
    
    infile.close();
main();
