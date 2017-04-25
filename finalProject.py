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