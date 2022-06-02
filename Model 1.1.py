# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:19:49 2022

@author: lucas
"""

from pulp import *
import Inlezen

region = 'Twente'
if region == 'Twente':    
    file = #Choose your own filename of the Twente database
    p = 3
    total = 623050
    reachable = 620395
elif region == 'Drenthe':
    file = #Choose your own filename of the Drenthe database
    p = 5
    total = 489610
    reachable = 476670
t = Inlezen.DISTANCE(file, region)
postals, d = Inlezen.DEMAND(file)

k = Inlezen.K(file, region)
I = postals
J = postals.copy()

#create LP-problem
Ambu = LpProblem("Ambu", LpMinimize)

#introduce y, c, u variable
y = LpVariable.dicts("Ambulance locations", J, cat='Binary')
c = LpVariable.dicts("C", I, cat='Binary')
u = LpVariable.dicts("Uber", (I,J), cat='Binary')

#add objective function
Ambu += lpSum([u[i][j]*d[i]*t[j][i] for j in J for i in I]), "Number of people reached"

#constraint number of locations
Ambu += lpSum([y[j] for j in J]) == p

#constraint number of people reached
Ambu += lpSum([c[i]*d[i] for i in I]) >= reachable

#constraint
for i in I:
    Ambu += lpSum([u[i][j] for j in J]) == 1

for i in I:
    for j in J:
        Ambu += u[i][j] <= y[j]

#constraint
for i in I:
    Ambu += c[i] - lpSum([y[j]*k[j][i] for j in J]) <= 0

Ambu.solve(CPLEX_CMD())

reached = 0
for i in I:
    reached += value(c[i])*d[i]
print(region)
print("Status: ", LpStatus[Ambu.status])
print("Total time: ", value(Ambu.objective)/total)
print("Population reached: ", reached)

#Maximum time needed
for j in J:
    if value(y[j]) == 1:
        print(j)
maxt = 0
maxi = 0
maxj = 0
for i in I:
    for j in J:
        if value(u[i][j])*t[j][i] > maxt:
            maxt = value(u[i][j])*t[j][i]
            maxi = i
            maxj = j
print(maxt,maxi,maxj)

#Dictionary used for the expansion
n = dict()
for j in J:
    if value(y[j]) == 1:
        som = 0
        for i in I:
            if value(u[i][j]) == 1:
                som += d[i]
        n[j] = som
print(n)