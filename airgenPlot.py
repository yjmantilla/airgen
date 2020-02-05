# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 22:09:20 2019

@author: yjmantilla
"""


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations


data_url = 'data.csv'
# read data from url as pandas dataframe
airgen = pd.read_csv(data_url)

print(airgen)

#we calculate the power output
op = airgen['vol'].values**2 / airgen['res'].values

print('Power Output')
print(op)

#we calculate power input of the wind

#air density at 20 deg c (average temp in medellin) in kg/m**3
airDensity = 1.2041
rotorRadius = 0.355 # in meters
rotorArea = np.pi * rotorRadius**2
wp = 0.5 * airDensity *  rotorArea * airgen['vel'].values**3 #in watts

print('Air Power')
print(wp)

#Power Coefficients Cp
cp = op / wp
print('Power Coefficients')
print(cp)


#we add this data to the dataframe

airgen['op'] = op
airgen['wp'] = wp
airgen['cp'] = cp

print('Complete Dataframe')
print(airgen)


#num vs power -> hold gra vel
#gra vs power -> hold num vel
#vel vs power -> hold gra num

k=0   #figure counter  
i=0   #permutation counter


class Parameter:
        name=''
        title=''
        val =[]
        
        def __init__(self, name,title,val):
            self.name = name
            self.title = title
            self.val = val
            
vel = Parameter('vel','Viento',[4,5,6])
ang = Parameter('ang','Angulo',[15,30])
asp = Parameter('asp','Num.Aspas',[2,3,4])
cp = Parameter('cp','Cp',[])
wp = Parameter('wp','Pviento',[])
op = Parameter('op','Psalida',[])       
       
parameterList = [vel,ang,asp]
powerList = [op,wp,cp]

# [0]=x, [1]=curve, [2]=hold

for param in permutations(parameterList, 3):
    paramHold = param[2]
    paramCurve = param[1]
    paramX = param[0]
    i+=1
    
    for pH in paramHold.val:
        for pq in powerList:
                fig=plt.figure(k,figsize=(13,10))
                #fig=plt.figure(k)
                print('-------'+'fig:'+str(k)+'-------')
                
                
                for pC in paramCurve.val:
                    print('Hold '+ paramHold.name + ':'+str(pH))
                    print('Curve '+ paramCurve.name + ':'+str(pC))
                    print('X:' + paramX.name)
                    print('Y:' + pq.name)
                    print('\n')
                    
                    df = airgen[(airgen[paramHold.name]==pH) & (airgen[paramCurve.name] == pC)]
                    #use plt.scatter or plt.plot here
                    #plt.scatter(df[paramX.name].values,df[pq.name].values,s=1000,label=paramCurve.title+':'+str(pC))
                    plt.plot(df[paramX.name].values,df[pq.name].values,linestyle='-', marker='o',linewidth=6,markersize=24,label=paramCurve.title+':'+str(pC))
                    plt.xlabel(paramX.title,fontsize = 'xx-large')
                    plt.ylabel(pq.title,fontsize = 'xx-large')         
                    plt.title(paramX.title + ' ' + 'vs' + ' ' + pq.title + ' ' + 'para' + ' ' + paramHold.title + ':' + str(pH),fontsize = 'xx-large')
                    plt.legend(loc='best', fontsize = 'xx-large')
                k+=1
                 
            
print('-------END OF FIGURES-------')      
print('Figures:'+str(k))    
print('Permutations:'+str(i))
print('\n')

#the problem was the ':' in the title
for f in range(k):
    plt.figure(f)
    title=plt.gca().get_title().replace(':',' ')
    plt.savefig(title+'.png')
    print(title+' saved')
#max values

for pq in powerList:
    print('Max ' + pq.name)
    print(airgen.loc[airgen[pq.name].idxmax(),:])
    print('\n')
    