# -*- coding: utf-8 -*-
"""
Created on Tue May 10 11:19:49 2022

@author: lucas
"""

import Inlezen
import random as rnd

file = #Choose your own filename

postals, demand_dict = Inlezen.DEMAND(file)
distance_dict = Inlezen.DISTANCE(file, "Twente")

def OnebyOne(postcodes, demand_dict, distance_dict, p, t):
    Ambupost = list()
    Bereikt = set()
    Totalpeople = 0
    Totaltime = 0
    
    i = 0
    while i < p:
        cur = None
        cur_k = 0
        for code1 in postals:
            k = 0
            for code2 in postals:
                time = distance_dict[code1][code2]
                if time <= t and code2 not in Bereikt:
                    k += demand_dict[code2]
            if k > cur_k:
                cur = code1
                cur_k = k

        Ambupost.append(cur)
        for code2 in postals:
            if distance_dict[cur][code2] <= t:
                Bereikt.add(code2)
                
        i += 1
    for postal in postals:
        vals = []
        for post in Ambupost:
            vals.append(distance_dict[post][postal])
        mini = min(vals)
        if mini <= 900:
            Totalpeople += demand_dict[postal]
        Totaltime += demand_dict[postal] * mini
    AvgTime = Totaltime/623050
    return t, Ambupost, Totalpeople, AvgTime

p = 3
for t in range(50, 15*60):
    t, Ambupost, Totalpeople, AvgTime = OnebyOne(rnd.shuffle(postals), demand_dict, distance_dict, p, t)
    if Totalpeople >= 600000 and AvgTime <= 550:
        print(t, Ambupost, Totalpeople, AvgTime)
    
                