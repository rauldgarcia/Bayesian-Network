import numpy as np
import pandas as pd
import math
import time
from itertools import combinations

inicio=time.time()

alpha={1 : 3.841,
       2 : 5.991,
       3 : 7.815,
       4 : 9.488,
       5 : 11.070,
       6 : 12.592,
       7 : 14.067,
       8 : 15.507,
       9 : 16.919,
       10 : 18.307,
       11 : 19.675,
       12 : 21.026,
       13 : 22.362,
       14 : 23.685,
       15 : 24.996,
       16 : 26.296,
       17 : 27.587,
       18 : 28.869,
       19 : 30.144,
       20 : 31.410,
       21 : 32.671,
       22 : 33.924,
       23 : 35.172,
       24 : 36.415,
       25 : 37.652,
       26 : 38.885,
       27 : 40.113,
       28 : 41.337,
       29 : 42.557,
       30 : 43.773,
       40 : 55.758,
       50 : 67.505,
       60 : 79.082,
       70 : 90.531,
       80 : 101.879,
       90 : 113.145,
       100 : 124.342}

data=pd.read_csv('discretizadaCAIMiris.csv')
print(data)
print(data.dtypes)
lendata=len(data)
names=data.columns.values 
print(names)
natributos=len(names)
print()

def mutual_info(a,b):
    va=list(set(list(data[a])))
    vb=list(set(list(data[b])))
    i=0
    for x in va:
        for y in vb:
                countxy=((data[a]==x) & (data[b]==y)).sum()
                countx=(data[a]==x).sum()
                county=(data[b]==y).sum()
                pxy=countxy/lendata
                px=countx/lendata
                py=county/lendata    
                if pxy>0:
                    aux=pxy/(px*py)
                    xy=pxy*math.log(aux)
                    i+=xy
    return i

def conditional_mutual_info(a,b,c):
    va=list(set(list(data[a])))
    vb=list(set(list(data[b])))
    vc=list(set(list(data[c])))
    i=0
    for x in va:
        for y in vb:
            for z in vc:
                countxyz=((data[a]==x) & (data[b]==y) & (data[c]==z)).sum()
                countz=(data[c]==z).sum()
                countx=((data[a]==x) & (data[c]==z)).sum()
                county=((data[b]==y) & (data[c]==z)).sum()
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
    va=list(set(list(data[a])))
    vb=list(set(list(data[b])))
    vc=list(set(list(data[c])))
    vd=list(set(list(data[d])))
    i=0
    for x in va:
        for y in vb:
            for z in vc:
                for w in vd:
                    countxyzw=((data[a]==x) & (data[b]==y) & (data[c]==z) & (data[d]==w)).sum()
                    countz=((data[c]==z) & (data[d]==w)).sum()
                    countx=((data[a]==x) & (data[c]==z) & (data[d]==w)).sum()
                    county=((data[b]==x) & (data[c]==z) & (data[d]==w)).sum()
                    pxyz=countxyzw/lendata
                    pz=countz/lendata 
                    pxz=countx/lendata
                    pyz=county/lendata    
                    if pxyz>0 and pz>0 and pxz>0 and pyz>0:
                        aux=(pxyz)/(((pxz*pyz)/pz))
                        xyz=pxyz*math.log(aux)
                        i+=xyz
                
    return i

combinaciones2=list(combinations(names,2)) #combinacion de dos atributos

print("Total de combinaciones:")
print(len(combinaciones2))
print("Total de atributos:")
print(natributos)
combinaciones=[]
atributos=[]
print("\nCalculando información mutua")
for combinacion in combinaciones2:
    i=mutual_info(combinacion[0],combinacion[1])
    t=2*lendata*i
    df=(len(list(set(list(data[combinacion[0]]))))-1)*(len(list(set(list(data[combinacion[1]]))))-1)
    if df<=30:
        sl=alpha[df]
    elif df>30 and df <=40:
        sl=alpha[30]
    elif df>40 and df <=50:
        sl=alpha[40]
    elif df>50 and df <=60:
        sl=alpha[50]
    elif df>60 and df <=70:
        sl=alpha[60]
    elif df>70 and df <=80:
        sl=alpha[70]
    elif df>80 and df <=90:
        sl=alpha[80]
    elif df>90 and df <=100:
        sl=alpha[90]
    else:
        sl=alpha[100]    
    if t >= sl:
        combinaciones.append(combinacion)
        atributos.append(combinacion[0])
        atributos.append(combinacion[1])

atributos=list(set(atributos))
print("Combinaciones:")
print(len(combinaciones))
print("Atributos:")
print(len(atributos))
print("\nCalculando información mutua condicional")

combinaciones3=[] #combinaciones de 2 atributos con un condicional
atributos2=[]
for combinacion in combinaciones:
    contsi=1
    contno=0

    if names[-1] in combinacion:
        combinaciones3.append(combinacion)
        atributos2.append(combinacion[0])
        atributos2.append(combinacion[1])

    else:
        for atributo in atributos:
            if not (atributo in combinacion):
                i=conditional_mutual_info(combinacion[0],combinacion[1],atributo)
                t=2*lendata*i
                df=(len(list(set(list(data[combinacion[0]]))))-1)*(len(list(set(list(data[combinacion[1]]))))-1)*(len(list(set(list(data[atributo])))))
                if df<=30:
                    sl=alpha[df]
                elif df>30 and df <=40:
                    sl=alpha[30]
                elif df>40 and df <=50:
                    sl=alpha[40]
                elif df>50 and df <=60:
                    sl=alpha[50]
                elif df>60 and df <=70:
                    sl=alpha[60]
                elif df>70 and df <=80:
                    sl=alpha[70]
                elif df>80 and df <=90:
                    sl=alpha[80]
                elif df>90 and df <=100:
                    sl=alpha[90]
                else:
                    sl=alpha[100] 

                if t >= sl:
                    contsi+=1
                else:
                    contno+=1

        if contsi>=contno:
            combinaciones3.append(combinacion)
            atributos2.append(combinacion[0])
            atributos2.append(combinacion[1])

atributos2=list(set(atributos2))
print("Combinaciones:")
print(len(combinaciones3))
print("Atributos:")
print(len(atributos2))
print("\nCalculando información mutua condicional con dos atributos")

combinaciones4=list(combinations(atributos2,2)) #combinaciones de 2 atributos con dos condicionales
combinaciones5=[]
atributosfin=[]
for combinacion in combinaciones3:
    contsi=1
    contno=0
    if names[-1] in combinacion:
        combinaciones5.append(combinacion)
        atributosfin.append(combinacion[0])
        atributosfin.append(combinacion[1])

    else:
        for combi in combinaciones4:
            if not (combi[0] in combinacion) and not (combi[1] in combinacion):
                i=conditional_mutual_info2(combinacion[0],combinacion[1],combi[0],combi[1])
                t=2*lendata*i

                df=(len(list(set(list(data[combinacion[0]]))))-1)*(len(list(set(list(data[combinacion[1]]))))-1)*(len(list(set(list(data[combi[0]])))))*(len(list(set(list(data[combi[1]])))))
                if df<=30:
                    sl=alpha[df]
                elif df>30 and df <=40:
                    sl=alpha[30]
                elif df>40 and df <=50:
                    sl=alpha[40]
                elif df>50 and df <=60:
                    sl=alpha[50]
                elif df>60 and df <=70:
                    sl=alpha[60]
                elif df>70 and df <=80:
                    sl=alpha[70]
                elif df>80 and df <=90:
                    sl=alpha[80]
                elif df>90 and df <=100:
                    sl=alpha[90]
                else:
                    sl=alpha[100]    

                if t >= sl:
                    contsi+=1
                else:
                    contno+=1

        if contsi>=contno:
            combinaciones5.append(combinacion)
            atributosfin.append(combinacion[0])
            atributosfin.append(combinacion[1])

print("Combinaciones:")
print(len(combinaciones5))
print("Atributos:")
print(len(list(set(atributosfin))))
for combinacion in combinaciones5:
    print("Conecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")

print("\nEl tiempo de ejecución es:")
fin=time.time()
print(fin-inicio)