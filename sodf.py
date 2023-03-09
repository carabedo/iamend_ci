import os
import pandas as pd
import csv
import plotly.express as px


def read(file, separador):
    # lee archivo csv del solatron
    # se puede definir el separador
    z=list()
    with open(file, 'r') as csvfile:
        spam = csv.reader(csvfile, delimiter=separador)
        #lineas del header
        next(spam)
        next(spam)
        next(spam)
        next(spam)

        for row in spam:
            z.append(row)
    df=pd.DataFrame(z)
    df=df.iloc[:,[0,1,4,12,13]]
    df.columns=['indice','repeticion','f','real','imag']
    return df

class DataFrameCI(pd.DataFrame):
    # construyo esta clase para extender la funcionalidad 
    # del dataframe de pandas, le agrego la posibilidad
    # de graficar las 11 mediciones que se realizan sobre 
    # cada muestra
    def __init__(self,filename,bobina,*args, **kwargs):
        super().__init__(*args, **kwargs)
        # solo me deja agregar atributos que no sean listas.
        self.filename=filename
        self.l0=bobina['L0']
    def impx(self):
        self['idznorm']=self['Impedance Imaginary (Ohms)']/(self['2*pi*f']*self.l0)
        self['Sweep Number']=self['Sweep Number'].astype(float).astype(int)
        return px.line(self, x='Frequency (Hz)',y='idznorm',color='Sweep Number',log_x=True)

def load(path,bobina,separador=';'):
    """ carga archivos en la carpeta actual, todos deben pertenecer a un mismo experimento, mismas frecuencias y misma cantidad de repeticiones, se le puede asginar la direccion en disco de la carpeta a la variable path (tener cuidado con los //), si path=0 abre una ventana de windows para elegirla manualmente
    --------------------------------------------------------------------------------------
    devuelve una lista: 
        data[0] lista de los datos de cada archivo, cada indice es una matriz con los datos crudos de cada archivo
        
        data[1] lista con los nombres de los archivos        
    """    
    
    folder_path = path
    filepaths=[]
    for (dirpath, dirnames, filenames) in os.walk(folder_path):
        filenames.sort()
        for i,j in enumerate(filenames):
            filepaths.extend([dirpath + '/'+j])
        break
    data=list()
    for k,filepath in enumerate(filepaths):
        if ('info' not in filepath) & ('csv' in filepath):
            df=read(filepath,separador)
            dfci=DataFrameCI(filename=filenames[k],bobina=bobina)
            data.append(dfci) 
    return data  

def corrnorm(df):
    """ corrige y normaliza los datos, toma como input el vector de frecuencias, la info de la bobina y los datos
        devuelve una lista de arrays, cada array es la impedancia compleja corregida y normalizada para cada frecuencia, parte real y parte imaginaria
        para recuperar la parte real  (.real) e imaginaria (.imag)
    """
    pass
