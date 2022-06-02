# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:19:49 2022

@author: lucas
"""

from pulp import *
import Inlezen

region = 'Drenthe'
if region == 'Twente':    
    file = #Choose your own filename of the Twente database
    p = 3
    total = 623050
elif region == 'Drenthe':
    file = #Choose your own filename of the Drenthe database
    p = 5
    total = 489610
postals, d = Inlezen.DEMAND(file)

k = Inlezen.K(file,region)
I = postals
J = postals.copy()

#create LP-problem
Ambu = LpProblem("Ambu", LpMaximize)

#introduce y variable
y = LpVariable.dicts("Ambulance locations", J, cat='Binary')
c = LpVariable.dicts("C", I, cat='Binary')

#add objective function
Ambu += lpSum([c[i]*d[i] for i in I]), "Number of people reached"

#constraint number of locations
Ambu += lpSum([y[j] for j in J]) == p
    
#constraint
for i in I:
    Ambu += c[i] - lpSum([y[j]*k[j][i] for j in J]) <= 0

Ambu.solve(CPLEX_CMD())

print(region)
print("Status: ", LpStatus[Ambu.status])
print("Number of people reached: ", value(Ambu.objective))
    
for j in J:
    if value(y[j]) == 1:
        print(j)
