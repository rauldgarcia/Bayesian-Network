import numpy as np
import pandas as pd
import math
import time
from itertools import combinations
from sklearn.metrics import mutual_info_score
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

"""def mutual_info(a,b):
    va=list(set(list(data[a])))
    vb=list(set(list(data[b])))
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
    return i"""

def conditional_mutual_info(a,b,c):
    va=list(set(list(data[a])))
    vb=list(set(list(data[b])))
    vc=list(set(list(data[c])))
    i=0
    for x in va:
        for y in vb:
            for z in vc:
                countxyz=0
                countx=0
                county=0
                countz=0
                for ejemplo in range(lendata):
                    if (data[a][ejemplo]==x) and (data[b][ejemplo]==y) and (data[c][ejemplo]==z):
                        countxyz+=1
                    if data[c][ejemplo]==z:
                        countz+=1
                    if (data[a][ejemplo]==x) and (data[c][ejemplo]==z):
                        countx+=1
                    if (data[b][ejemplo]==y) and (data[c][ejemplo]==z):
                        county+=1  

                pxyz=countxyz/lendata
                pz=countz/lendata 
                pxz=countx/lendata
                pyz=county/lendata    
                
                if pxyz>0 and pz>0 and pxz>0 and pyz>0:
                    aux=(pxyz)/(((pxz*pyz)/pz))
                    xyz=pxyz*math.log(aux)
                    i+=xyz

    return i

def conditional_mutual_info2(a,b,c,d):
    va=list(set(list(data[names[a]])))
    vb=list(set(list(data[names[b]])))
    vc=list(set(list(data[names[c]])))
    vd=list(set(list(data[names[d]])))
    i=0
    for x in va:
        for y in vb:
            for z in vc:
                for w in vd:
                
                    countxyzw=0
                    countx=0
                    county=0
                    countz=0
                    for ejemplo in range(lendata):
                        if (data[names[a]][ejemplo]==x) and (data[names[b]][ejemplo]==y) and (data[names[c]][ejemplo]==z) and (data[names[d]][ejemplo]==w):
                            countxyzw+=1
                        if data[names[c]][ejemplo] and data[names[d]][ejemplo]==z:
                            countz+=1
                        if (data[names[a]][ejemplo]==x) and (data[names[c]][ejemplo] and data[names[d]][ejemplo]==z):
                            countx+=1
                        if (data[names[b]][ejemplo]==y) and (data[names[c]][ejemplo]==z) and data[names[d]][ejemplo]:
                            county+=1  

                    pxyz=countxyzw/lendata
                    pz=countz/lendata 
                    pxz=countx/lendata
                    pyz=county/lendata    
                    
                    if pxyz>0 and pz>0 and pxz>0 and pyz>0:
                        aux=(pxyz)/(((pxz*pyz)/pz))
                        xyz=pxyz*math.log(aux)
                        i+=xyz
                
    return i

#print(mutual_info(0,1))
#print(mutual_info_score(data[names[0]],data[names[1]]))

combinaciones2=list(combinations(names,2)) #combinacion de dos atributos

combinaciones=[]
atributos=[]
for combinacion in combinaciones2:
    i=mutual_info_score(data[combinacion[0]],data[combinacion[1]])
    t=2*lendata*i
    if t >= 3.841:
        print("Conecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
        combinaciones.append(combinacion)
        atributos.append(combinacion[0])
        atributos.append(combinacion[1])

#print(combinaciones)
atributos=list(set(atributos))
#print(atributos)

for combinacion in combinaciones:
    for atributo in atributos:
        if not (atributo in combinacion):
            i=conditional_mutual_info(combinacion[0],combinacion[1],atributo)
            t=2*lendata*i
            if t < 5.991:
                print("Desconecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")


"""print()
print(conditional_mutual_info(0,1,2))
#print(conditional_mutual_info(0,1,3))
print(conditional_mutual_info(0,2,1))
#print(conditional_mutual_info(0,2,3))
#print(conditional_mutual_info(0,3,1))
#print(conditional_mutual_info(0,3,2))
print(conditional_mutual_info(1,2,0))
#print(conditional_mutual_info(1,2,3))
#print(conditional_mutual_info(1,3,0))
#print(conditional_mutual_info(1,3,2))
#print(conditional_mutual_info(2,3,0))
#print(conditional_mutual_info(2,3,1))"""

"""print()
print(conditional_mutual_info2(0,1,2,3))
print(conditional_mutual_info2(0,2,1,3))
print(conditional_mutual_info2(0,3,1,2))
print(conditional_mutual_info2(1,2,0,3))
print(conditional_mutual_info2(1,3,0,2))
print(conditional_mutual_info2(2,3,0,1))"""

print("\nEl tiempo de ejecución es:")
fin=time.time()
print(fin-inicio)