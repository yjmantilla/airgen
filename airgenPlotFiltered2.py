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
airDensity = 0.975
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
            
vel = Parameter('vel','Vviento [m/s]',[4,5,6])
ang = Parameter('ang','Angulo [°]',[15,30])
asp = Parameter('asp','Num.Aspas',[2,3,4])
cp = Parameter('cp','Cp [E-6]',[])
wp = Parameter('wp','Pviento',[])
op = Parameter('op','Psalida [mW]',[])       
       
parameterList = [vel,ang,asp]
powerList = [op,cp]

# [0]=x, [1]=curve, [2]=hold

paramHold = ang
paramX = asp
paramCurve = vel

for pq in powerList:    
    for pH in paramHold.val:
    
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
                plt.plot(df[paramX.name].values,df[pq.name].values,linestyle='-', marker='o',linewidth=6,markersize=24,label=paramCurve.title+':'+str(pC)+' '+paramHold.title+':'+str(pH))
                plt.xlabel(paramX.title,fontsize = 'xx-large')
                plt.ylabel(pq.title,fontsize = 'xx-large')         
                plt.title(paramX.title + ' y '+ paramHold.title + ' ' + 'vs' + ' ' + pq.title,fontsize = 'xx-large')
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
    title=title.replace('Vviento [m/s]','Vviento')
    title=title.replace('Angulo [°]','Angulo')
    title=title.replace('Cp [E-6]','Cp')
    title=title.replace('Psalida [mW]','Psalida')
    plt.savefig('plot '+title+'.png')
    print('plot '+title+' saved')
#max values

for pq in powerList:
    print('Max ' + pq.name)
    print(airgen.loc[airgen[pq.name].idxmax(),:])
    print('\n')
    