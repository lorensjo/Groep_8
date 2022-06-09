"""
This file, "Inlezen.py" was used to read all data from the Twente and Drenthe databases and convert the data to a demand[postcode] dictionary, 
a distance[postcode1][postcode2] dictionary for travel times and a binary k_ji dictionary which is 0 or 1 depending whether postal code i is reachable within 900 seconds from ambulance location j.
"""
import pandas as pd

def DEMAND(file):
    data = pd.read_excel(file, sheet_name=2)
    #post = pd.DataFrame(df, columns= ['Postal codes'])
    
    postcodes = data["Postal codes"]
    demands = data["Demand"]
    
    L = len(postcodes)
    
    # Maak dictionary voor demand
    demand_dict = dict()
    for index in range(L):
        demand_dict[postcodes[index]] = demands[index]
    
    return postcodes, demand_dict

def DISTANCE(file, region):
    if region == 'Twente':
        data = pd.read_excel(file, sheet_name=1, header=1, usecols='A:DQ') 
    elif region == 'Drenthe':
        data = pd.read_excel(file, sheet_name=1, header=1, usecols='A:IV')
    
    bases = data["j"]
    L = len(bases)
            
    # Make distances dictionary from base j to postal code i
    distance_dict = dict()
    for j in range(L):  # All bases
        base = bases[j]
        d = dict()
        for i in range(L):
            nummer = bases[i]
            afstand = data[nummer][j]
            if i == j:
                afstand = 0     
            d[nummer] = afstand
        distance_dict[base] = d
        
    return distance_dict

def K(file, region):
    if region == 'Twente':
        data = pd.read_excel(file, sheet_name=1, header=1, usecols='A:DQ') 
    elif region == 'Drenthe':
        data = pd.read_excel(file, sheet_name=1, header=1, usecols='A:IV')
    bound = 900
    
    bases = data["j"]
    L = len(bases)
            
    # Make distances dictionary from base j to postal code i
    k = dict()
    for j in range(L):  # All bases
        base = bases[j]
        kbinnen = dict()
        for i in range(L):
            nummer = bases[i]
            afstand = data[nummer][j]
            if i == j:
                afstand = 0
                
            if afstand <= bound:
                kbinnen[nummer] = 1
            else:
                kbinnen[nummer] = 0
        k[base] = kbinnen
    return k

        
    
