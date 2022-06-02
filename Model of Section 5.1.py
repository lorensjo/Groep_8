# -*- coding: utf-8 -*-
"""
Created on Tue May 31 13:25:12 2022

@author: lucas
"""

from pulp import *
import Inlezen

region = 'Drenthe'

if region == 'Twente':
    filename = #Choose your own filename of the Twente database
    p = 9
    A = 31
    population = 623050
    H = [7443,7462,7496,7514,7544,7557,7596,7608,7609]
    dmd = [50455,50975,43235,120790,57780,117355,48815,70325,63320]
    n = dict()
    for i, h in enumerate(H):
        n[h] = dmd[i]
elif region == 'Drenthe':
    filename = #Choose your own filename of the Drenthe database
    p = 16
    A = 59
    population = 489610
    H = [7741,7812,7823,7891,7908,7914,7941,7984,9301,9401,9407,9411,9462,9471,9571,9761]
    dmd = [21290,48235,42410,32180,36790,32885,45970,20175,29295,41055,42575,21220,24460,23155,14300,13615]
    n = dict()
    for i, h in enumerate(H):
        n[h] = dmd[i]

#create LP-problem
Ambu = LpProblem("Ambu", LpMaximize)

#introduce y, c, u variable
a = LpVariable.dicts("Ambulance locations", H, 1, cat='Integer')
S = LpVariable("People per ambulance", cat='Continuous')

#add objective function
Ambu += S, "Minimum of people per ambulance"

#constraint sum ambulances
Ambu += lpSum([a[h] for h in H]) == A

#constraint maximum
for h in H:
    Ambu += S*n[h] <= a[h]

Ambu.solve(CPLEX_CMD())

print(region)
print("Status: ", LpStatus[Ambu.status])
print("Max number of people per amublance: ", 1/value(Ambu.objective))

for h in H:
    print(h, n[h], value(a[h]))
