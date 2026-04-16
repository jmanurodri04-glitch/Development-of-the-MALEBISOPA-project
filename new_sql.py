import pandas as pd
import numpy as np
import datetime

#Load environmental data from power nasa
dfamb=pd.read_csv("D:\\data_prov\\POWER_Point.csv",skiprows=12)


#Define delta time to create a new column called 'Time'
#That new column matches perfectly with the irradiance data
delta=datetime.timedelta(minutes=15)

fecha_inicial=datetime.datetime(2021,7,1,0,0)
fecha_limite=datetime.datetime(2025,5,11,23,0)

vector_tiempo=[]
#Create 4 vectors (Temperature, specific humidity, precipitation, relative humidity)
temperaturas=dfamb['T2M']
humedad_esp=dfamb['QV2M']
precipitacion=dfamb['PRECTOTCORR']
humedad_rel=dfamb['RH2M']

temperaturasmod=[]
humedad_espmod=[]
precipitacionmod=[]
humedad_relmod=[]
#Create 2 counters since we have hourly data
contador=0
contador2=0

while 1<2:
    #Filling the vectors with the environmental data
    vector_tiempo.append(fecha_inicial)
    temperaturasmod.append(temperaturas[contador])
    humedad_espmod.append(humedad_esp[contador])
    precipitacionmod.append(precipitacion[contador])
    humedad_relmod.append(humedad_rel[contador])

    contador2=contador2+1
    if contador2==4:
        contador2=0
        contador=contador+1


    fecha_inicial=fecha_inicial+delta
    if fecha_inicial==fecha_limite:
        break

#Create a new modified data frame with the environmental data
diccionario1={'Time':vector_tiempo,'Temperatura':temperaturasmod,'humedad_esp':humedad_espmod,'precipitacion':precipitacionmod,'humedad_rel':humedad_relmod}
dataframe_mod=pd.DataFrame(diccionario1)

dataframe_mod.to_csv("D:\\data_prov\\POWER_Pointmod.csv",index=False)

#Load irradiance data from March 12 2025 to May 11 2025
env_nueva=pd.read_csv("D:\\data_prov\\ENV_2025.csv")
env_nueva=env_nueva.set_axis(['Time','Rear 1 (W/m2)','Front POA1 (W/m2)','Rear 2 (W/m2)','Front POA2 (W/m2)','Rear 3 (W/m2)'],axis='columns')
nfil_time=len(env_nueva['Time'])
#Create albedo vectors
arr_G=np.zeros((nfil_time,1))
arr_W=np.zeros((nfil_time,1))
arr_B=np.ones((nfil_time,1))
arr_S=np.zeros((nfil_time,1))

env_nueva['G']=arr_G
env_nueva['W']=arr_W
env_nueva['B']=arr_B
env_nueva['S']=arr_S

#Load irradiance data from july 2021 to March 2025
int_data=pd.read_csv("D:\\integrated_data.csv")
#Concatenate the irradiance data
general1=pd.concat([int_data,env_nueva])

#Add the environmental data 
general1['Temperatura C']=temperaturasmod[51:]
general1['Humedad_especifica g/kg']=humedad_espmod[51:]
general1['Precipitacion mm/hour']=precipitacionmod[51:]
general1['Humedad relativa %']=humedad_relmod[51:]

#Drop columns that are not useful for the project
general1=general1.drop(['Inverter AC (W)','Array DC (W)','Battery Charge (W)','Battery Discharge (W)','EV Consumption (W)',
                        'Temp mod 1 (C)','Temp mod 2 (C)','Power Mod 1 (W)','Power Mod 2 (W)','Power Mod 3 (W)','Power Mod 4 (W)',
                        'Power Mod 5 (W)','Power Mod 6 (W)','Power Mod 7 (W)','Power Mod 8 (W)','Power Mod 9 (W)','Power Mod 10 (W)',
                        'Power Mod 11 (W)','Power Mod 12 (W)','Observation'],axis=1)
#Upload the File we will use for our project
general1.to_csv("D:\\data_prov\\integrated_proyecto.csv",index=False)


