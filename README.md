# ItacaReader

ItacaReader és un script senzill que es pot utilitzar per a passar els llistats d'incidències d'Itaca del format:
![image](https://user-images.githubusercontent.com/91680464/135536933-46e7c8de-a6dd-4b89-99eb-bd27533dcefa.png)
a un arxiu csv que es pot obrir amb excel amb el format típic del quadern de professor:
![image](https://user-images.githubusercontent.com/91680464/135536973-d6da02c3-21f9-48a5-83d4-73c1b554cd2c.png)

És un script de Python, per la qual cosa cal tindre instal·lat python per a executar-lo i les llibreries camelot, pandas i datetime (es poden instal·lar amb pip, per exemple).

L'script cerca a totes les carpetes del directori on es troba el llistat de l'alumnat i el llistat d'incidències, que han d'estar junts dins de la mateixa carpeta:

![image](https://user-images.githubusercontent.com/91680464/135537591-a86e18ed-3bda-4c96-8b79-39cc95986aec.png)
![image](https://user-images.githubusercontent.com/91680464/135537741-e58e8f0f-6929-4ba3-a0b8-eb89daefdac7.png)

El nom de la carpeta determina el nom del csv creat (ja que se li posa el mateix nom), mentre que el nom dels documents amb els llistats de l'alumnat i d'incidències pot ser qualsevol.

Per a obtindre el llistat de l'alumnat cal generar en Itaca l'informe que es diu "Llisat de qualificacions", i, per a obtindre el llistat d'incidències, cal obtindre en Itaca el document homònim sel·leccionant la data d'inici i de fi, el grup i la matèria. És important no marcar cap dels quadradets d'ordenar i filtrar que hi ha baix d'on es tria la matèria.

Una volta fet açò, quan l'script s'execute, es generarà un csv dins de la carpeta amb tota la informació que té el llistat d'incidències d'Itaca i ens permet analitzar millor les dades:

![image](https://user-images.githubusercontent.com/91680464/135538482-3559e91d-33c7-4b58-a02a-07dd8c45084b.png)
