# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 18:35:24 2019

@author: user
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

airgen['op'] = op*1000 #in milliWatts
airgen['wp'] = wp
airgen['cp'] = cp*1000000 #in micros

print('Complete Dataframe')
print(airgen)

#combinatorial variables
#num vs power -> hold gra vel
#gra vs power -> hold num vel
#vel vs power -> hold gra num

k=0     
i=0          


class Parameter:
        name=''
        title=''
        val =[]
        
        def __init__(self, name,title,val):
            self.name = name
            self.title = title
            self.val = val
            
vel = Parameter('vel','Vviento [m/s]',[4,5,6])
ang = Parameter('ang','Angulo [°]',[30,15])
asp = Parameter('asp','Num.Aspas',[2,3,4])
cp = Parameter('cp','Cp [E-6]',[])
wp = Parameter('wp','Pviento',[])
op = Parameter('op','Psalida [mW]',[])      
       
parameterList = [vel,ang,asp]
powerList = [op,cp]

# [0]=x, [1]=y, [2]=hold
    
paramHold = ang
paramX = asp
paramY = vel
for pq in powerList:
    for pH in paramHold.val:                
        print('-------'+'fig:'+str(k)+'-------')
        fig=plt.figure(k,figsize=(9,6))
        #fig=plt.figure(k)
        print('Hold '+ paramHold.name + ':'+str(pH))
        print('X:' + paramX.name)
        print('Y:' + paramY.name)
        print('Z:' + pq.name)
        print('\n')
        df = airgen[(airgen[paramHold.name]==pH)]
        
        plt.title(paramX.title + ' y ' + paramY.title +' ' + 'vs' + ' ' + pq.title + ' ' + 'para' + ' ' + paramHold.title + ':' + str(pH),fontsize = 'x-large')
        plt.xlabel(paramX.title,fontsize = 'x-large')
        plt.ylabel(paramY.title,fontsize = 'x-large')
        plt.scatter(df[paramX.name].values, df[paramY.name].values, s=pH*100,c=df[pq.name].values,cmap=plt.cm.get_cmap('plasma'), vmin=1, vmax=150 )
        cb=plt.colorbar()
        cb.set_label(pq.title,fontsize = 'x-large')
    k+=1
        
        
        
print('-------END OF FIGURES-------')      
print('Figures:'+str(k))    
print('Permutations:'+str(i))
print('\n')

for f in range(k):
    plt.figure(f)
    title=plt.gca().get_title().replace(':',' ')
    title=title.replace('Vviento [m/s]','Vviento')
    title=title.replace('Angulo [°]','Angulo')
    title=title.replace('Cp [E-6]','Cp')
    title=title.replace('Psalida [mW]','Psalida')
    plt.savefig('map '+title+'.png')
    print(title+' saved')
    