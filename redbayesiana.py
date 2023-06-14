import numpy as np
import pandas as pd
import math
import time
from itertools import combinations
import pyAgrum as gum
#import pyAgrum.lib.notebook as gnb
inicio=time.time()

data=pd.read_csv('discretizadairis.csv')
print(data)
print(data.dtypes)
lendata=len(data)
names=data.columns.values 
#names=np.delete(nombres,-1) #eliminar esta linea y cambiar nombres a names si se utiliza la clase
print(names)
natributos=len(names)
print(natributos)
print()

bn=gum.BayesNet()
for name in names: #agrega cada atributo a la red bayesiana y especifica el numero de valores que toma ese atributo
    tamaño=len(list(set(list(data[name]))))
    name=bn.add(gum.LabelizedVariable(name,name+'1',tamaño))

print(bn)
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

combinaciones=[]
atributos=[]
for combinacion in combinaciones2:
    i=mutual_info(combinacion[0],combinacion[1])
    t=2*lendata*i
    if t >= 3.841:
        print("Conecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
        bn.addArc(combinacion[0],combinacion[1])
        combinaciones.append(combinacion)
        atributos.append(combinacion[0])
        atributos.append(combinacion[1])

print(bn)

atributos=list(set(atributos))

combinaciones3=[] #combinaciones de 2 atributos con un condicional
combinacioneseliminadas=[]
atributos2=[]
for combinacion in combinaciones:
    for atributo in atributos:
        if not (atributo in combinacion):
            i=conditional_mutual_info(combinacion[0],combinacion[1],atributo)
            t=2*lendata*i
            if t < 5.991:
                print("Desconecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
                if bn.existsArc(combinacion[0],combinacion[1]):
                    bn.eraseArc(combinacion[0],combinacion[1])
                combinacioneseliminadas.append(combinacion)
            elif combinacion in combinacioneseliminadas: #si adelante sale que tiene que ir conectada la vuelve a conectar
                print("Conecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
                if not bn.existsArc(combinacion[0],combinacion[1]):
                    bn.addArc(combinacion[0],combinacion[1])
                combinaciones3.append(combinacion)
                atributos2.append(combinacion[0])
                atributos2.append(combinacion[1])
            else: # si no hay que desconectar o reconectar solo lo agrega a la lista
                combinaciones3.append(combinacion)
                atributos2.append(combinacion[0])
                atributos2.append(combinacion[1])

combinaciones3=list(set(combinaciones3))
atributos2=list(set(atributos2))

combinaciones4=list(combinations(atributos2,2)) #combinaciones de 2 atributos con dos condicionales
combinacioneseliminadas=[]
for combinacion in combinaciones3:
    for combi in combinaciones4:
        if not (combi[0] in combinacion) and not (combi[1] in combinacion):
            i=conditional_mutual_info2(combinacion[0],combinacion[1],combi[0],combi[1])
            t=2*lendata*i
            if t < 7.815:
                print("Desconecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
                if bn.existsArc(combinacion[0],combinacion[1]):
                    bn.eraseArc(combinacion[0],combinacion[1])
                combinacioneseliminadas.append(combinacion)
            elif combinacion in combinacioneseliminadas: #si adelante sale que tiene que ir conectada la vuelve a conectar
                print("Conecta el atributo ", combinacion[0], " con el atributo ", combinacion[1], ".")
                if not bn.existsArc(combinacion[0],combinacion[1]):
                    bn.addArc(combinacion[0],combinacion[1])
                
            #else: # si no hay que desconectar o reconectar solo lo agrega a la lista
#import pyAgrum.lib.notebook
#bn

print("\nEl tiempo de ejecución es:")
fin=time.time()
print(fin-inicio)