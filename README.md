# iamend_ci

Libreria para la estimacion de la permeabilidad relativa efectiva usando mediciones de impedancia de una bobina sobre materiales conductores ferromagneticos. Contiene submodulos para la importancion de mediciones realizadas con `Solartron 1260A`, grafico de impedancias y correciones de efectos no ideales en los contactos.

### implementacion del modelo teorico de dood,deeds

`iamend_ci.theo.zo()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_1.png)

`iamend_ci.theo.dzD()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_2.png)

`iamend_ci.theo.jhf()`

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_3.png)

con:

![img](https://raw.githubusercontent.com/carabedo/iamend_ci/master/imgs/0_4.png)




### carga  y correccion datos



```python


import iamend_ci as ci


# Generamos un objeto de la clase experimento
# esta carpeta tiene que tener los archivos csv de las mediciones 
# y un archivo info.csv 

exp1=ci.exp('carpeta con mediciones')
``` 
Una vez creado el objeto exp, tenemos los sigueintes metodos y atributos:

 ```python
 exp1.bobina : Nombre de la bobina
 exp1.coil : Array con valores de la bobina
 exp1.data : Lista con el array de los datos.
 exp1.espesores : Lista de espesores.
 exp1.f : Lista de frecuencias.
 exp1.files : Lista de nombres de archivos.
 exp1.fitmues() : Metodo para ajustar permeabilidades.
 exp1.fitpatron() : Metodo para ajustar z1eff usando las mediciones sobre el patron.
 exp1.im(n) : Metodo para plotear la parte imaginaria de la medicion n.
 exp1.info : Dataframe con los nombres de los archivos, conductividades, espesores.
 exp1.normcorr() : Metodo para normalizar y corregir los datos.
 exp1.path : Ruta de la carpeta donde estan los archivos del experimento.
 exp1.re(n) :  Metodo para plotear la parte imaginaria de la medicion n.
 exp1.sigmas : Lista de sigmas.
 exp1.w : Lista de frecuencias * 2*np.pi.
 ``` 


### grafico datos

```python
# ploteo de la parte imaginaria de la impedancia corregida (n= id medicion )
exp.im(0)
```

![](/imgs/1.png)

### ajuste permeabilidad

#### parametros geometricos efectivos

```phyton
exp1.fitpatron()
```
Luego de realizar el ajuste sobre el patron, el z1 efectivo esta en el atributo:

```phyton
exp1.z1eff
```

#### permeabilidad relativa efectiva

```phyton
exp1.fitmues()
```

Luego de realizar el ajuste de las permeabilidades, los mues estan en el atributo:

```phyton
exp1.mues
```





