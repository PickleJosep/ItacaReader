# ItacaReader v1.1
# Fet per Josep Gallego

import os
import camelot
from datetime import datetime
import pandas as pd

def process_folder(grupo):
    #Se obtienen los pdfs que haya dentro de la carpeta
    alguna_incidencia = False
    pdfs = [os.path.join(grupo, f) for f in os.listdir(grupo) if os.path.isfile(os.path.join(grupo, f)) and f.endswith('.pdf')]
    listas_pdf = []
    incidencias_pdf = []
    
    #Se identifica cuáles son los PDFS que tienen las listas de alumnos y cuáles las incidencias
    for pdf in pdfs:
        layout, dim = camelot.utils.get_page_layout(pdf)
        if dim[0] < dim[1]:
            listas_pdf.append(pdf)
        else:
            incidencias_pdf.append(pdf)
    
    #Si no encuentra algún documento en la carpeta, sale
    if len(listas_pdf) < 1:
        print('  - ERROR: Document amb el llistat de l\'alumnat no trobat')
        return
    
    if len(incidencias_pdf) < 1:
        print('  - ERROR: Document amb les incidències de l\'alumnat no trobat')
        return
    
    #Se obtiene el listado con todo el alumnado de la clase (nombre y curso)
    listado = {}
    for lista in listas_pdf:
        try:
            lectura = camelot.read_pdf(lista, flavor = 'stream', table_areas=['10, 650, 400, 10'], columns=['45, 90, 300, 325'], split_text=True, strip_text='\n')[0].df
            alumni = lectura[2][lectura[4] != '']
            clase = lectura[4][lectura[4] != '']
            for alum, clas in zip(alumni, clase):
                listado[alum] = {'curs': clas, 'inci': []}
        except:
            print('  - ERROR: No s\'ha pogut llegir correctament el document ' + lista)
    print('  - Classe amb ' + str(len(listado)) + ' alumnes')
    
    # Aquí se procesa cada hoja de incidencias y se juntan todas
    lecturas = pd.DataFrame()
    for incidencia in incidencias_pdf:   
        try:
            #Se lee el pdf y se condensa toda la información en la variable lectura
            lectura = camelot.read_pdf(incidencia, flavor = 'stream', row_tol=10, pages = '1-end', table_areas=['10, 440, 817, 80'], columns=['206, 242, 290, 332, 374, 485, 614'])
            concatenado = pd.concat([elem.df for elem in lectura], ignore_index = True)
            afig = []
            for index, row in concatenado.iterrows():
                if not ('Grup' in str(row) or 'Pàgina' in str(row) or 'Data' in str(row) or '(amonestació' in str(row) or 'Fecha' in str(row) or 'Página' in str(row)):
                    afig.append(index)
            lecturas = pd.concat([lecturas, concatenado.iloc[afig, :]], ignore_index = True)
            print('  - Llegides ' + str(len(lecturas)) + ' incidències en ' + os.path.basename(incidencia) + '\n')
            alguna_incidencia = True
        except:
            print('  - ADVERTÈNCIA: No s\'ha pogut llegir correctament el document ' + incidencia + ' o no s\'han trobat incidències.')
    lecturas = lecturas.replace('\n', ' ', regex=True)
    
    #Se obtienen todas las fechas para las que hay incidencias
    fechas_dict = {}
    fechas = []
    if alguna_incidencia:
        fechas = [fecha for fecha in lecturas[2]]
        fechas = list(dict.fromkeys(fechas))
        fechas.sort(key = lambda date: datetime.strptime(date, '%d/%m/%Y'))
        for i, elem in enumerate(fechas):
            fechas_dict[elem] = i
    
        #Se rellena el listado de alumnados con las incidencias
        for key in listado:
            listado[key]['inci'] = [[] for i in range(len(fechas_dict))]
        df = lecturas.iloc[:, 0]
        indices = df[df != ''].index
        for i, elem in enumerate(indices):
            j = 0
            if i < len(indices) - 1:
                while(elem + j < indices[i+1]):
                    listado[lecturas.iloc[elem, 0]]['inci'][fechas_dict[lecturas.iloc[elem + j, 2]]].append({lecturas.iloc[elem + j, 1]: lecturas.iloc[elem + j, 5]})
                    j += 1
            else:
                while(elem + j < len(df)):
                    listado[lecturas.iloc[elem, 0]]['inci'][fechas_dict[lecturas.iloc[elem + j, 2]]].append({lecturas.iloc[elem + j, 1]: lecturas.iloc[elem + j, 5]})
                    j += 1
        
    header = ['Cognoms', 'Nom', 'Curs'] + fechas
    with open(os.path.join(grupo, os.path.basename(grupo) + '.csv'), 'w') as f:
        for elem in header:
            f.write(elem + ';')
        f.write('\n')

        for key in listado:
            spl = key.split(', ')
            f.write(spl[0] + ';' + spl[1] + ';' + listado[key]['curs'])
            for elem in listado[key]['inci']:
                f.write(';')
                if elem != []:
                    for i, incidencia in enumerate(elem):
                        for clave in incidencia:
                            if i == 0:
                                f.write(clave + ': ' + incidencia[clave])
                            else:
                                f.write(' & ' + clave + ': ' + incidencia[clave])
            f.write('\n')

d = '.'
grupos = [os.path.join(d, o) for o in os.listdir(d) if (os.path.isdir(os.path.join(d,o)) and o[0] != '.' and o[0] != '_')]

for grupo in grupos:
    print('Processant ' + os.path.basename(grupo) + ':')
    process_folder(grupo)

print('Processament finalitzat!\n\n')