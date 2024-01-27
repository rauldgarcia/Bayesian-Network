Aprendizaje Automático 

Proyecto Final 

Redes Bayesianas

Raúl Daniel García Ramón

rauld.garcia95@gmail.com

# Introducción
Las redes bayesianas son representaciones de la dependencia entre variables mediante grafos dirigidos acíclicos, donde cada nada nodo representa un atributo, el cual puede ser categórico o continuo, mientras que las flechas sirven para conectar pares de nodos entre sí, de manera que si hay una flecha que va del nodo X al Y se dice que X es padre de Y. Cada nodo tiene asociada una probabilidad que cuantifica el efecto de los padres en el nodo.

Para obtener la red bayesiana se requiere tener la base de datos correspondiente, con la cual se calculara la información mutua entre cada par de atributos $X$ y $Y$ con la fórmula, para posteriormente obtener el valor de $T$ con la ecuación, donde $N$ es el número de ejemplos que incluye la base de datos. A continuación se calcula el número de grados de libertad del par de atributos con la fórmula y con ese valor $df$ obtener el valor de $\chi^{2}$ de tablas para $\alpha=0.05$. Después, se revisa si $T\geq\chi^{2}$ y en caso de que así sea, se dice que son dependientes y se agrega una flecha entre estos atributos, mientras que si no es el caso, se dice que son independientes y no se agrega la flecha entre los nodos.

$H(X:Y)=I(X,Y)=\sum_{XY}P(X,Y)Log\frac{P(X,Y)}{P(X)P(Y)}$

$T=2NI$

$df=(Cat(X)-1)*(Cat(Y)-1)*\prod_{i=1}^{n}Cat(Zi)$

Posteriormente, se repite lo anterior, pero con la información mutua condicional, la cual se calcula con la fórmula, para cada par de atributos, condicionándolo con un tercer atributo diferente $Z$, en caso de obtener que $T\geq\chi^{2}$ si no había flecha entre los atributos $X$ y $Y$ se agrega esta, si ya había se mantiene la flecha, y en caso de que no se cumpla $T\geq\chi^{2}$, si había una flecha entre los atributos $X$ y $Y$ esta se elimina.

$H(X:Y|Z)=I(X,Y|Z)=\sum_{XYZ}P(X,Y,Z)Log\frac{P(X,Y|Z)}{P(X|Z)P(Y|Z)}$

Finalmente, se va repitiendo lo anterior, pero agregando otra variable $W$ a la información mutua condicional, como se ve en la fórmula

$H(X:Y|Z,W)=I(X,Y|Z,W)=\sum_{XYZW}P(X,Y,Z,W)Log\frac{P(X,Y|Z,W)}{P(X|Z,W)P(Y|Z,W)}$


# Heurística propuesta

Para implementar la obtención de la red bayesiana se propone utilizar la siguiente heurística, la cual consiste en:

1. Calcular la información mutua con la fórmula para todas las combinaciones posibles de dos atributos, y guardar en una lista $L1$ únicamente aquellas que hayan generado una conexión entre par de atributos, además de guardar una lista $L2$ los atributos que sí hayan generado conexión. De manera que si un atributo no genera conexión ya no será contemplado más adelante.

1. Calcular la información mutua condicional con la fórmula únicamente para las combinaciones guardadas en la lista $L1$. Los atributos a condicionar cada combinación serán los que estén en la lista $L2$ (solamente no condicionaran los atributos que estén en la combinación). De manera que se calculara la información mutua condicional para cada combinación en $L1$ con cada uno de los atributos de $L2$, después de cada cálculo se revisara si $T\geq\chi^{2}$ si es el caso se votará para que la conexión se mantenga, si no es el caso se votará para que la conexión no se mantenga. Después de calcular la información mutua condicional de la combinación con cada elemento de la lista $L2$ se verá quien gano la votación, en caso de ganar que se mantenga la conexión o si hay empate la combinación se guarda en la lista $L3$ y sus atributos en la lista $L4$. (Las combinaciones que sean entre algún atributo y el target se guardaran en automático sin pasar por votación)

1. Se repetirá lo mismo del paso anterior, pero con la fórmula, condicionando con todas las combinaciones posibles de los elementos de la lista $L4$.

1. Finalmente, se generará la red con las conexiones que se hayan guardado al final del paso anterior.


A continuación se muestra un ejemplo con la base de datos Iris: 

* Primero se tiene la lista de los atributos, en este caso son los siguientes cinco:

'SepalLengthCm' 'SepalWidthCm' 'PetalLengthCm' 'PetalWidthCm' 'Species'

* Con esta lista se obtienen las 10 combinaciones siguientes:

('SepalLengthCm', 'SepalWidthCm'), ('SepalLengthCm', 'PetalLengthCm'), ('SepalLengthCm', 'PetalWidthCm'), ('SepalLengthCm', 'Species'), ('SepalWidthCm', 'PetalLengthCm'), ('SepalWidthCm', 'PetalWidthCm'), ('SepalWidthCm', 'Species'), ('PetalLengthCm', 'PetalWidthCm'), ('PetalLengthCm', 'Species'), ('PetalWidthCm', 'Species')

* A cada combinación de la lista se obtiene su información mutua con la fórmula, se calcula $T$ con la fórmula y se calcula sus grados de libertad con la fórmula para obtener su valor $\chi^{2}$ y si $T\geq\chi^{2}$ se agrega esa combinación a la lista $L1$ y se guardan sus atributos en la lista $L2$

* Al finalizar los cálculos para este ejemplo se obtiene la lista $L1$ siguiente, en la cual las 10 combinaciones generaron conexión, por lo tanto, las 10 se guardan

('SepalLengthCm', 'SepalWidthCm'), ('SepalLengthCm', 'PetalLengthCm'), ('SepalLengthCm', 'PetalWidthCm'), ('SepalLengthCm', 'Species'), ('SepalWidthCm', 'PetalLengthCm'), ('SepalWidthCm', 'PetalWidthCm'), ('SepalWidthCm', 'Species'), ('PetalLengthCm', 'PetalWidthCm'), ('PetalLengthCm', 'Species'), ('PetalWidthCm', 'Species') 

* Mientras que la lista $L2$ se queda con los mismos 5 atributos

'SepalWidthCm', 'PetalWidthCm', 'PetalLengthCm', 'Species', 'SepalLengthCm'

* Posteriormente, para cada combinación en la lista $L1$ se calcula su información mutua condicional con la fórmula, condicionando con cada elemento de la lista $L2$ que no esté en la combinación que se está evaluando, de manera que la primera combinación de $L1$ ('SepalLengthCm', 'SepalWidthCm') será condiciona por 'PetalWidthCm', 'PetalLengthCm', 'Species' y si $T\geq\chi^{2}$ se votará para que se mantenga la combinación, en caso contrario se votará para que se elimine la combinación.

En el caso del ejemplo ('SepalLengthCm', 'SepalWidthCm') se obtiene la siguiente votación:

* Desconecta el atributo  SepalLengthCm  con el atributo  SepalWidthCm. 
* Desconecta el atributo  SepalLengthCm  con el atributo  SepalWidthCm. 
* Desconecta el atributo  SepalLengthCm  con el atributo  SepalWidthCm. 

Por lo que esa combinación no se guarda en la lista $L3$ ni sus atributos en la lista $L4$

Sin embargo, para la combinación ('SepalLengthCm', 'PetalLengthCm') se obtiene la siguiente votación: 

* Desconecta el atributo  SepalLengthCm  con el atributo  PetalLengthCm. 
* Conecta el atributo  SepalLengthCm  con el atributo  PetalLengthCm. 
* Conecta el atributo  SepalLengthCm  con el atributo  PetalLengthCm. 

En este caso la votación la gana que se mantenga la conexión, por lo que se agrega la combinación a la lista $L3$ y sus atributos a la lista $L4$ (en caso de haber empate se guarda la combinación).

En el caso de las combinaciones que incluyan al target, en esta base de datos llamada 'Species', esta combinación se guardara sin pasar por votación. Al finalizar este proceso para cada combinación se obtiene la lista $L3$ siguiente:

('SepalLengthCm', 'PetalLengthCm'), ('SepalLengthCm', 'PetalWidthCm'), ('SepalLengthCm', 'Species'), ('SepalWidthCm', 'PetalLengthCm'), ('SepalWidthCm', 'PetalWidthCm'), ('SepalWidthCm', 'Species'), ('PetalLengthCm', 'PetalWidthCm'), ('PetalLengthCm', 'Species'), ('PetalWidthCm', 'Species')

Se puede notar que ahora la lista es de 9 combinaciones, ya que la combinación ('SepalLengthCm', 'SepalWidthCm') se eliminó después de la votación. Mientras que la lista $L4$ queda de la siguiente manera: 

'SepalLengthCm', 'SepalWidthCm', 'PetalWidthCm', 'PetalLengthCm', 'Species'

* A continuación, para cada combinación de la lista $L3$ se calculará su información mutua condicional con dos atributos condicionando con la fórmula, donde los dos atributos a condicionar serán tomados la lista $L4$ siempre y cuando los atributos no estén en la combinación, por ejemplo para la primera combinación de la lista $L3$ ('SepalLengthCm', 'PetalLengthCm') esta se condicionará con las combinaciones  ('SepalWidthCm', 'Species'), ('SepalWidthCm', 'PetalWidthCm'), ('Species', 'PetalWidthCm'). Y de igual manera que en el paso anterior se votara si se mantiene o no la combinación, y en el caso de las combinaciones que incluyen al target, estas se volverán a guardar sin pasar por la votación.

Al final las combinaciones que queden conectadas serán las que generen la red bayesiana, en el ejemplo de Iris queda de la siguiente manera:

* Conecta el atributo  SepalLengthCm  con el atributo  PetalLengthCm. 
* Conecta el atributo  SepalLengthCm  con el atributo  PetalWidthCm. 
* Conecta el atributo  SepalLengthCm  con el atributo  Species. 
* Conecta el atributo  SepalWidthCm  con el atributo  PetalLengthCm. 
* Conecta el atributo  SepalWidthCm  con el atributo  PetalWidthCm. 
* Conecta el atributo  SepalWidthCm  con el atributo  Species. 
* Conecta el atributo  PetalLengthCm  con el atributo  PetalWidthCm. 
* Conecta el atributo  PetalLengthCm  con el atributo  Species. 
* Conecta el atributo  PetalWidthCm  con el atributo  Species. 

Y el grafo de esta red bayesiana se vería como se muestra en la figura:

![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.001.png)

Al correr el código con la base de datos Iris que se utilizó como ejemplo, en la terminal se muestra el siguiente resultado:

['SepalLengthCm' 'SepalWidthCm' 'PetalLengthCm' 'PetalWidthCm' 'Species']

Total de combinaciones: 10

Total de atributos: 5

Calculando información mutua

Combinaciones: 10

Atributos: 5

Calculando información mutua condicional

Combinaciones: 9

Atributos: 5

Calculando información mutua condicional con dos atributos

Combinaciones: 9

Atributos: 5

Conecta el atributo  SepalLengthCm  con el atributo  PetalLengthCm.

Conecta el atributo  SepalLengthCm  con el atributo  PetalWidthCm.

Conecta el atributo  SepalLengthCm  con el atributo  Species.

Conecta el atributo  SepalWidthCm  con el atributo  PetalLengthCm.

Conecta el atributo  SepalWidthCm  con el atributo  PetalWidthCm.

Conecta el atributo  SepalWidthCm  con el atributo  Species.

Conecta el atributo  PetalLengthCm  con el atributo  PetalWidthCm.

Conecta el atributo  PetalLengthCm  con el atributo  Species.

Conecta el atributo  PetalWidthCm  con el atributo  Species.

El tiempo de ejecución es: 1.8674638271331787


# Experimentos

Para realizar diferentes experimentos y poder ver qué resultados se obtienen al utilizar la heurística propuesta, se utilizan las siguientes diez bases de datos obtenidas del repositorio UC Irvine Machine Learning Repository \cite{uci}:

* Balance Scale
* Breast Cancer Wisconsin (Original)
* Contraceptive Method Choice 
* Ecoli
* Glass Identification
* Haberman's Survival
* Iris
* Liver Disorders
* Seeds
* Wholesale Customers


Para comparar las redes bayesianas obtenidas con la heurística propuesta se utiliza el software Waikato Environment for Knowledge Analysis, WEKA, en el cual se ingresa la base de datos y la red generada y utilizando una validación cruzada de diez se obtiene la precisión de la red bayesiana para la clasificación, además se realiza una comparación con los datos obtenidos al generar la red bayesiana con WEKA con el algoritmo de búsqueda local K2 con cada una de las bases de datos utilizadas.

# Resultados

A continuación se muestran gráficamente cada una de las redes bayesianas obtenidas tanto por el software de WEKA como con la heurística propuesta para cada una de las diez bases de datos utilizadas: 

![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.002.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.003.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.004.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.005.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.006.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.007.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.008.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.009.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.010.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.011.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.012.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.013.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.014.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.001.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.015.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.016.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.017.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.018.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.019.png)
![](Aspose.Words.851c9663-140a-45f2-8656-c14e21f5083d.020.png)


La tabla muestra la precisión obtenida tanto por el algoritmo de WEKA como con la heurística propuesta, en donde se puede apreciar que el algoritmo de WEKA obtiene mayor precisión en cinco de las diez bases de datos, mientras que con la heurística propuesta se obtiene una mayor precisión en tres y se obtiene el mismo resultado en las otras dos bases de datos. Sin embargo, se realiza la prueba estadística Wilcoxon rank-sum para ver si existe una diferencia significativa entre los valores obtenidos, con la cual se obtuvo un valor de $P=1$ por lo que no hay diferencia significativa entre los valores obtenidos.

|Bases|WEKA|Propuesta|
| - | - | - |
| Balance Scale | **72.32** | 71.04 |
| Breast Cancer Wisconsin| **94.27** | 93.99 |
| Contraceptive Method Choice | 51.73 | **52.27** |
| Ecoli | **82.44** | 79.16 |
| Glass Identification | **71.02** | 65.88 |
| Haberman's Survival | 72.87 | 72.87 |
| Iris | **93.33** | 92 |
| Liver Disorders | 57.97 | 57.97 |
| Seeds | 89.04 | **91.42** |
| Wholesale Customers | 89.54 | **91.13** |
|Media|77.45|76.77|

# Conclusión
Después de realizar los experimentos con las diferentes bases de datos, así como comparar los resultados obtenidos entre la heurística propuesta y la utilizada por WEKA, se puede concluir que en general la heurística propuesta es competente, debido a que obtiene valores similares a los de WEKA, lo cual se ve reflejado en el valor $P$ obtenido con la prueba estadística Wilcoxon rank-sum, al igual que en la media de ambos algoritmos. Finalmente, esta heurística, en algunos casos, también ayuda a encontrar aquellos atributos que no aportan información necesaria para la tarea de clasificación, por lo que podrían ser ignorados sin llegar a perder información relevante.
