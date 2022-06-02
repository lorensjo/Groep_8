# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:54:09 2022

@author: loren
"""

from pulp import *
import Inlezen

region = 'Twente'

if region == 'Twente':
    filename = #Choose your own filename of the Twente database
    p = 3
    people = 623050
elif region == 'Drenthe':
    filename = #Choose your own filename of the Drenthe database
    p = 5
    people = 489610
#Input data
J, d = Inlezen.DEMAND(filename)
I = J.copy()
t = Inlezen.DISTANCE(filename, region)
k = Inlezen.K(filename, region)
factor = 1500

#create LP problem 
Ambu = LpProblem("Ambu", LpMinimize)

#introduce y and c and u variable
y = LpVariable.dicts("Ambubool",J,cat="Binary")
c = LpVariable.dicts("c", I, cat="Binary")
u = LpVariable.dicts("u",(I,J), cat="Binary")

#add objective function
Ambu += lpSum([d[i]*u[i][j]*t[j][i] for j in J for i in I]) - factor*lpSum([c[i]*d[i] for i in I]), "tijd totaal - aantal bereikt"

# uij constraint
for i in I:
    Ambu += lpSum([u[i][j] for j in J]) == 1
    
for i in I:
    for j in J:
        Ambu += u[i][j] <= y[j] 



# max p constraint
Ambu += lpSum([y[j] for j in J]) == p

# c_i - sumthing <= 0 constraint
for i in I:
    Ambu += c[i] - lpSum([y[j]*k[j][i] for j in J]) <= 0


 
#solve problem    
Ambu.solve(CPLEX_CMD())
    
#print status
print(factor)
print("Status:", LpStatus[Ambu.status])

#print objective function value
#print("Totale tijd", value(Ambu.objective))

#print solution
som = 0
for i in I:
    som += value(c[i])*d[i]
print("Aantal bereikte mensen: " + str(som))
print("Totale tijd: " + str((value(Ambu.objective)+factortje*som)/people))
print("Ambulance locaties/postcodes:")
for j in J:
    if value(y[j]) != 0:
        print(j)

[d[i]*u[i][j]*t[j][i] for j in J for i in I]
maxi = 0
post = I[0]
for i in I:
    for j in J:
        if value(u[i][j])*t[j][i] > maxi:
            maxi = value(u[i][j])*t[j][i]
            post = i
                 
print("Langste tijd:")
print(post, maxi)