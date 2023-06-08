import numpy as np
import pandas as pd
import math
import time
inicio=time.time()

data=pd.read_csv('prueba.csv')
print(data)
print(data.dtypes)
lendata=len(data)
names=data.columns.values
print(names)
natributos=len(names)
print(natributos)
print()

def mutual_info(a,b):
    va=list(set(list(data[names[a]])))
    vb=list(set(list(data[names[b]])))

    i=0
    for x in va:
        for y in vb:
                countxy=0
                countx=0
                county=0
                
                for ejemplo in range(lendata):
                    if (data[names[a]][ejemplo]==x) and (data[names[b]][ejemplo]==y):
                        countxy+=1
                    if data[names[a]][ejemplo]==x:
                        countx+=1
                    if data[names[b]][ejemplo]==y:
                        county+=1  

                pxy=countxy/lendata
                px=countx/lendata
                py=county/lendata    
                
                if pxy>0:
                    aux=pxy/(px*py)
                    xy=pxy*math.log(aux)
                    i+=xy

    return i

def conditional_mutual_info(a,b,c):
    va=list(set(list(data[names[a]])))
    vb=list(set(list(data[names[b]])))
    vc=list(set(list(data[names[c]])))
    i=0
    for x in va:
        for y in vb:
            for z in vc:
                countxyz=0
                countx=0
                county=0
                countz=0
                for ejemplo in range(lendata):
                    if (data[names[a]][ejemplo]==x) and (data[names[b]][ejemplo]==y) and (data[names[c]][ejemplo]==z):
                        countxyz+=1
                    if data[names[c]][ejemplo]==z:
                        countz+=1
                    if (data[names[a]][ejemplo]==x) and (data[names[c]][ejemplo]==z):
                        countx+=1
                    if (data[names[b]][ejemplo]==y) and (data[names[c]][ejemplo]==z):
                        county+=1  

                pxyz=countxyz/lendata
                pz=countz/lendata 
                pxz=countx/lendata
                pyz=county/lendata    
                
                if pxyz>0:
                    aux=(pxyz/pz)/((pxz/pz)*(pyz/pz))
                    xyz=pxyz*math.log(aux)
                    i+=xyz

    return i

print(mutual_info(0,1))
print(mutual_info(0,2))
print(mutual_info(1,2))

print()
print(conditional_mutual_info(0,1,2))
print(conditional_mutual_info(0,2,1))
print(conditional_mutual_info(1,2,0))

print("El tiempo de ejecución es:")
fin=time.time()
print(fin-inicio)