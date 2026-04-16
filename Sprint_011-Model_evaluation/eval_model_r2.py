import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
import re
import statistics
from scipy.stats import spearmanr

#Load MAE, R2 and MAPE for each sensor
df_poa1=pd.read_excel("list_mae.xlsx",sheet_name="POA1")
df_poa2=pd.read_excel("list_mae.xlsx",sheet_name="POA2")
df_rear1=pd.read_excel("list_mae.xlsx",sheet_name="Rear1")
df_rear2=pd.read_excel("list_mae.xlsx",sheet_name="Rear2")
df_rear3=pd.read_excel("list_mae.xlsx",sheet_name="Rear3")

#This function creates a dictionary with each metric
def div_metrics(df1):
    dictionary={"MAE_ind":df1.iloc[3:19,2:10].reset_index(drop=True),"MAE_INT":df1.iloc[20:36,2:10].reset_index(drop=True),
                "R2_ind":df1.iloc[3:19,13:21].reset_index(drop=True),"R2_INT":df1.iloc[20:36,13:21].reset_index(drop=True),
                "MAPE_ind":df1.iloc[3:19,24:32].reset_index(drop=True),"MAPE_INT":df1.iloc[20:36,24:32].reset_index(drop=True)}
    dictionary["MAE_ind"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]
    dictionary["MAE_INT"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]
    dictionary["R2_ind"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]
    dictionary["R2_INT"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]
    dictionary["MAPE_ind"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]
    dictionary["MAPE_INT"].columns=["n","LSTM","GRU","BiLSTM","BiGRU","TCN","CNN-LSTM","CNN-GRU"]

    for metric1 in dictionary.keys():
        
        for n_col in range(1,8):

            for n_row in range(0,16):
                #It is important to convert np.float64 and nan values
                if isinstance(dictionary[metric1].iloc[n_row,n_col], str):
                    
                    x = re.sub(r'np\.float64\(', '', dictionary[metric1].iloc[n_row,n_col])
                    # # Remove parenthesis
                    x = x.replace(')', '')
                if isinstance(x,str):
                    x = re.sub(r'\bnan\b', 'None', x)
                #ast.literal_eval() converts string to list
                dictionary[metric1].iloc[n_row,n_col]=ast.literal_eval(x)


    return dictionary

#Apply function to all sensors
poa1_metrics=div_metrics(df_poa1)
poa2_metrics=div_metrics(df_poa2)
rear1_metrics=div_metrics(df_rear1)
rear2_metrics=div_metrics(df_rear2)
rear3_metrics=div_metrics(df_rear3)

#Verify the elements' type
print(type(poa2_metrics["MAPE_INT"].iloc[2,2]))
print(type(rear1_metrics["R2_INT"].iloc[4,0]))
num_elements=len(poa1_metrics["MAE_ind"].iloc[0,1])
print(num_elements)

##set1 1 LSTM, GRU, BiLSTM, BiGRU
#This function creates a list of all the R2 values ​​for a given day and finds the medium (median) value.
def create_set1(sensor_metric):
    df_R2_ind=sensor_metric["R2_ind"]
    df_R2_INT=sensor_metric["R2_INT"]
    end_list=[]

    for n_element in range(0,num_elements):
        daily_list=[]
        for n_col in range(1,5):
        
            for n_row in range(0,16):
                n_day_ind=df_R2_ind.iloc[n_row,n_col][n_element]
                n_day_INT=df_R2_INT.iloc[n_row,n_col][n_element]
                daily_list.append(n_day_ind)
                daily_list.append(n_day_INT)
        medium_value=statistics.median(daily_list)
        end_list.append(medium_value)
    #enumerate basically allows us to keep track of the day number
    end_tuple=enumerate(end_list)
    #Finally we use sorted to order the numbers from lowest to highest
    ordered_tuple=sorted(end_tuple,key=lambda x: x[1],reverse=False)
    
    return end_list, ordered_tuple

medium_POA1_set1, tuple_POA1_set1=create_set1(poa1_metrics)
medium_POA2_set1, tuple_POA2_set1=create_set1(poa2_metrics)
medium_Rear1_set1, tuple_Rear1_set1=create_set1(rear1_metrics)
medium_Rear2_set1, tuple_Rear2_set1=create_set1(rear2_metrics)
medium_Rear3_set1, tuple_Rear3_set1=create_set1(rear3_metrics)

#zip(*) allows us to get a list where list[0] is the hardest day and list[127] is the easiest
POA1_set1,days1=zip(*tuple_POA1_set1)
POA2_set1,days2=zip(*tuple_POA2_set1)
Rear1_set1,days3=zip(*tuple_Rear1_set1)
Rear2_set1,days4=zip(*tuple_Rear2_set1)
Rear3_set1,days5=zip(*tuple_Rear3_set1)
#print(medium_POA1_set1)

##set2  TCN, CNN_LSTM, CNN_GRU
#This function creates a list of all the R2 values ​​for a given day and finds the medium (median) value.
def create_set2(sensor_metric):
    df_R2_ind=sensor_metric["R2_ind"]
    df_R2_INT=sensor_metric["R2_INT"]
    end_list=[]

    for n_element in range(0,num_elements):
        daily_list=[]
        for n_col in range(5,8):
            
            for n_row in range(0,16):
                n_day_ind=df_R2_ind.iloc[n_row,n_col][n_element]
                n_day_INT=df_R2_INT.iloc[n_row,n_col][n_element]
                daily_list.append(n_day_ind)
                daily_list.append(n_day_INT)
        medium_value=statistics.median(daily_list)
        end_list.append(medium_value)
    #enumerate basically allows us to keep track of the day number
    end_tuple=enumerate(end_list)
    #Finally we use sorted to order the numbers from lowest to highest
    ordered_tuple=sorted(end_tuple,key=lambda x: x[1],reverse=False)
    
    return end_list, ordered_tuple

medium_POA1_set2, tuple_POA1_set2=create_set2(poa1_metrics)
medium_POA2_set2, tuple_POA2_set2=create_set2(poa2_metrics)
medium_Rear1_set2, tuple_Rear1_set2=create_set2(rear1_metrics)
medium_Rear2_set2, tuple_Rear2_set2=create_set2(rear2_metrics)
medium_Rear3_set2, tuple_Rear3_set2=create_set2(rear3_metrics)

#zip(*) allows us to get a list where list[0] is the hardest day and list[127] is the easiest
POA1_set2,days1=zip(*tuple_POA1_set2)
POA2_set2,days2=zip(*tuple_POA2_set2)
Rear1_set2,days3=zip(*tuple_Rear1_set2)
Rear2_set2,days4=zip(*tuple_Rear2_set2)
Rear3_set2,days5=zip(*tuple_Rear3_set2)
#print(medium_POA1_set1)

##set3  CNN_LSTM_CNN_GRU
#This function creates a list of all the R2 values ​​for a given day and finds the medium (median) value.
def create_set3(sensor_metric):
    df_R2_ind=sensor_metric["R2_ind"]
    df_R2_INT=sensor_metric["R2_INT"]
    end_list=[]

    for n_element in range(0,num_elements):
        daily_list=[]
        for n_col in range(6,8):
            
            for n_row in range(0,16):
                n_day_ind=df_R2_ind.iloc[n_row,n_col][n_element]
                n_day_INT=df_R2_INT.iloc[n_row,n_col][n_element]
                daily_list.append(n_day_ind)
                daily_list.append(n_day_INT)
        medium_value=statistics.median(daily_list)
        end_list.append(medium_value)
    #enumerate basically allows us to keep track of the day number
    end_tuple=enumerate(end_list)
    #Finally we use sorted to order the numbers from lowest to highest
    ordered_tuple=sorted(end_tuple,key=lambda x: x[1],reverse=False)
    
    return end_list, ordered_tuple

medium_POA1_set3, tuple_POA1_set3=create_set3(poa1_metrics)
medium_POA2_set3, tuple_POA2_set3=create_set3(poa2_metrics)
medium_Rear1_set3, tuple_Rear1_set3=create_set3(rear1_metrics)
medium_Rear2_set3, tuple_Rear2_set3=create_set3(rear2_metrics)
medium_Rear3_set3, tuple_Rear3_set3=create_set3(rear3_metrics)

#zip(*) allows us to get a list where list[0] is the hardest day and list[127] is the easiest
POA1_set3,days1=zip(*tuple_POA1_set3)
POA2_set3,days2=zip(*tuple_POA2_set3)
Rear1_set3,days3=zip(*tuple_Rear1_set3)
Rear2_set3,days4=zip(*tuple_Rear2_set3)
Rear3_set3,days5=zip(*tuple_Rear3_set3)
#print(medium_POA1_set1)

##Create Q1,Q2,Q3,Q4 for set1 and set2
inter_Q1_POA1=list(set(POA1_set1[0:31]) & set(POA1_set2[0:31]))
inter_Q2_POA1=list(set(POA1_set1[31:64]) & set(POA1_set2[31:64]))
inter_Q3_POA1=list(set(POA1_set1[64:97]) & set(POA1_set2[64:97]))
inter_Q4_POA1=list(set(POA1_set1[97:]) & set(POA1_set2[97:]))

conc_Q1_POA1=len(inter_Q1_POA1)/len(POA1_set1[0:31])
conc_Q2_POA1=len(inter_Q2_POA1)/len(POA1_set1[31:64])
conc_Q3_POA1=len(inter_Q3_POA1)/len(POA1_set1[64:97])
conc_Q4_POA1=len(inter_Q4_POA1)/len(POA1_set1[97:])
print("intersection of quartile intervals of set1 and set2 for POA1")
print(inter_Q1_POA1)
print(inter_Q2_POA1)
print(inter_Q3_POA1)
print(inter_Q4_POA1)
print(f"coincidence Q1= {conc_Q1_POA1}, coincidence Q2= {conc_Q2_POA1}, coincidence Q3= {conc_Q3_POA1}, coincidence Q4= {conc_Q4_POA1}")

inter_Q1_POA2=list(set(POA2_set1[0:31]) & set(POA2_set2[0:31]))
inter_Q2_POA2=list(set(POA2_set1[31:64]) & set(POA2_set2[31:64]))
inter_Q3_POA2=list(set(POA2_set1[64:97]) & set(POA2_set2[64:97]))
inter_Q4_POA2=list(set(POA2_set1[97:]) & set(POA2_set2[97:]))

conc_Q1_POA2=len(inter_Q1_POA2)/len(POA2_set1[0:31])
conc_Q2_POA2=len(inter_Q2_POA2)/len(POA2_set1[31:64])
conc_Q3_POA2=len(inter_Q3_POA2)/len(POA2_set1[64:97])
conc_Q4_POA2=len(inter_Q4_POA2)/len(POA2_set1[97:])
print("intersection of quartile intervals of set1 and set2 for POA2")
print(inter_Q1_POA2)
print(inter_Q2_POA2)
print(inter_Q3_POA2)
print(inter_Q4_POA2)
print(f"coincidence Q1= {conc_Q1_POA2}, coincidence Q2= {conc_Q2_POA2}, coincidence Q3= {conc_Q3_POA2},  coincidence Q4= {conc_Q4_POA2}")

inter_Q1_Rear1=list(set(Rear1_set1[0:31]) & set(Rear1_set2[0:31]))
inter_Q2_Rear1=list(set(Rear1_set1[31:64]) & set(Rear1_set2[31:64]))
inter_Q3_Rear1=list(set(Rear1_set1[64:97]) & set(Rear1_set2[64:97]))
inter_Q4_Rear1=list(set(Rear1_set1[97:]) & set(Rear1_set2[97:]))

conc_Q1_Rear1=len(inter_Q1_Rear1)/len(Rear1_set1[0:31])
conc_Q2_Rear1=len(inter_Q2_Rear1)/len(Rear1_set1[31:64])
conc_Q3_Rear1=len(inter_Q3_Rear1)/len(Rear1_set1[64:97])
conc_Q4_Rear1=len(inter_Q4_Rear1)/len(Rear1_set1[97:])
print("intersection of quartile intervals of set1 and set2 for Rear1")
print(inter_Q1_Rear1)
print(inter_Q2_Rear1)
print(inter_Q3_Rear1)
print(inter_Q4_Rear1)
print(f"coincidence Q1= {conc_Q1_Rear1}, coincidence Q2= {conc_Q2_Rear1}, coincidence Q3= {conc_Q3_Rear1}, coincidence Q4= {conc_Q4_Rear1}")

inter_Q1_Rear2=list(set(Rear2_set1[0:31]) & set(Rear2_set2[0:31]))
inter_Q2_Rear2=list(set(Rear2_set1[31:64]) & set(Rear2_set2[31:64]))
inter_Q3_Rear2=list(set(Rear2_set1[64:97]) & set(Rear2_set2[64:97]))
inter_Q4_Rear2=list(set(Rear2_set1[97:]) & set(Rear2_set2[97:]))

conc_Q1_Rear2=len(inter_Q1_Rear2)/len(Rear2_set1[0:31])
conc_Q2_Rear2=len(inter_Q2_Rear2)/len(Rear2_set1[31:64])
conc_Q3_Rear2=len(inter_Q3_Rear2)/len(Rear2_set1[64:97])
conc_Q4_Rear2=len(inter_Q4_Rear2)/len(Rear2_set1[97:])
print("intersection of quartile intervals of set1 and set2 for Rear2")
print(inter_Q1_Rear2)
print(inter_Q2_Rear2)
print(inter_Q3_Rear2)
print(f"coincidence Q1= {conc_Q1_Rear2}, coincidence Q2= {conc_Q2_Rear2}, coincidence Q3= {conc_Q3_Rear2}, coincidence Q4= {conc_Q4_Rear2}")

inter_Q1_Rear3=list(set(Rear3_set1[0:31]) & set(Rear3_set2[0:31]))
inter_Q2_Rear3=list(set(Rear3_set1[31:64]) & set(Rear3_set2[31:64]))
inter_Q3_Rear3=list(set(Rear3_set1[64:97]) & set(Rear3_set2[64:97]))
inter_Q4_Rear3=list(set(Rear3_set1[97:]) & set(Rear3_set2[97:]))

conc_Q1_Rear3=len(inter_Q1_Rear3)/len(Rear3_set1[0:31])
conc_Q2_Rear3=len(inter_Q2_Rear3)/len(Rear3_set1[31:64])
conc_Q3_Rear3=len(inter_Q3_Rear3)/len(Rear3_set1[64:97])
conc_Q4_Rear3=len(inter_Q4_Rear3)/len(Rear3_set1[97:])
print("intersection of quartile intervals of set1 and set2 for Rear3")
print(inter_Q1_Rear3)
print(inter_Q2_Rear3)
print(inter_Q3_Rear3)
print(f"coincidence Q1= {conc_Q1_Rear3}, coincidence Q2= {conc_Q2_Rear3}, coincidence Q3= {conc_Q3_Rear3}, coincidence Q4= {conc_Q4_Rear3}")


##Create Q1,Q2,Q3,Q4 for set1 and set3
inter_Q1_POA1=list(set(POA1_set1[0:31]) & set(POA1_set3[0:31]))
inter_Q2_POA1=list(set(POA1_set1[31:64]) & set(POA1_set3[31:64]))
inter_Q3_POA1=list(set(POA1_set1[64:97]) & set(POA1_set3[64:97]))
inter_Q4_POA1=list(set(POA1_set1[97:]) & set(POA1_set3[97:]))

conc_Q1_POA1=len(inter_Q1_POA1)/len(POA1_set1[0:31])
conc_Q2_POA1=len(inter_Q2_POA1)/len(POA1_set1[31:64])
conc_Q3_POA1=len(inter_Q3_POA1)/len(POA1_set1[64:97])
conc_Q4_POA1=len(inter_Q4_POA1)/len(POA1_set1[97:])
print("intersection of quartile intervals of set1 and set3 for POA1")
print(inter_Q1_POA1)
print(inter_Q2_POA1)
print(inter_Q3_POA1)
print(inter_Q4_POA1)
print(f"coincidence Q1= {conc_Q1_POA1}, coincidence Q2= {conc_Q2_POA1}, coincidence Q3= {conc_Q3_POA1}, coincidence Q4= {conc_Q4_POA1}")

inter_Q1_POA2=list(set(POA2_set1[0:31]) & set(POA2_set3[0:31]))
inter_Q2_POA2=list(set(POA2_set1[31:64]) & set(POA2_set3[31:64]))
inter_Q3_POA2=list(set(POA2_set1[64:97]) & set(POA2_set3[64:97]))
inter_Q4_POA2=list(set(POA2_set1[97:]) & set(POA2_set3[97:]))

conc_Q1_POA2=len(inter_Q1_POA2)/len(POA2_set1[0:31])
conc_Q2_POA2=len(inter_Q2_POA2)/len(POA2_set1[31:64])
conc_Q3_POA2=len(inter_Q3_POA2)/len(POA2_set1[64:97])
conc_Q4_POA2=len(inter_Q4_POA2)/len(POA2_set1[97:])
print("intersection of quartile intervals of set1 and set3 for POA2")
print(inter_Q1_POA2)
print(inter_Q2_POA2)
print(inter_Q3_POA2)
print(inter_Q4_POA2)
print(f"coincidence Q1= {conc_Q1_POA2}, coincidence Q2= {conc_Q2_POA2}, coincidence Q3= {conc_Q3_POA2},  coincidence Q4= {conc_Q4_POA2}")

inter_Q1_Rear1=list(set(Rear1_set1[0:31]) & set(Rear1_set3[0:31]))
inter_Q2_Rear1=list(set(Rear1_set1[31:64]) & set(Rear1_set3[31:64]))
inter_Q3_Rear1=list(set(Rear1_set1[64:97]) & set(Rear1_set3[64:97]))
inter_Q4_Rear1=list(set(Rear1_set1[97:]) & set(Rear1_set3[97:]))

conc_Q1_Rear1=len(inter_Q1_Rear1)/len(Rear1_set1[0:31])
conc_Q2_Rear1=len(inter_Q2_Rear1)/len(Rear1_set1[31:64])
conc_Q3_Rear1=len(inter_Q3_Rear1)/len(Rear1_set1[64:97])
conc_Q4_Rear1=len(inter_Q4_Rear1)/len(Rear1_set1[97:])
print("intersection of quartile intervals of set1 and set3 for Rear1")
print(inter_Q1_Rear1)
print(inter_Q2_Rear1)
print(inter_Q3_Rear1)
print(inter_Q4_Rear1)
print(f"coincidence Q1= {conc_Q1_Rear1}, coincidence Q2= {conc_Q2_Rear1}, coincidence Q3= {conc_Q3_Rear1}, coincidence Q4= {conc_Q4_Rear1}")

inter_Q1_Rear2=list(set(Rear2_set1[0:31]) & set(Rear2_set3[0:31]))
inter_Q2_Rear2=list(set(Rear2_set1[31:64]) & set(Rear2_set3[31:64]))
inter_Q3_Rear2=list(set(Rear2_set1[64:97]) & set(Rear2_set3[64:97]))
inter_Q4_Rear2=list(set(Rear2_set1[97:]) & set(Rear2_set3[97:]))

conc_Q1_Rear2=len(inter_Q1_Rear2)/len(Rear2_set1[0:31])
conc_Q2_Rear2=len(inter_Q2_Rear2)/len(Rear2_set1[31:64])
conc_Q3_Rear2=len(inter_Q3_Rear2)/len(Rear2_set1[64:97])
conc_Q4_Rear2=len(inter_Q4_Rear2)/len(Rear2_set1[97:])
print("intersection of quartile intervals of set1 and set3 for Rear2")
print(inter_Q1_Rear2)
print(inter_Q2_Rear2)
print(inter_Q3_Rear2)
print(f"coincidence Q1= {conc_Q1_Rear2}, coincidence Q2= {conc_Q2_Rear2}, coincidence Q3= {conc_Q3_Rear2}, coincidence Q4= {conc_Q4_Rear2}")

inter_Q1_Rear3=list(set(Rear3_set1[0:31]) & set(Rear3_set3[0:31]))
inter_Q2_Rear3=list(set(Rear3_set1[31:64]) & set(Rear3_set3[31:64]))
inter_Q3_Rear3=list(set(Rear3_set1[64:97]) & set(Rear3_set3[64:97]))
inter_Q4_Rear3=list(set(Rear3_set1[97:]) & set(Rear3_set3[97:]))

conc_Q1_Rear3=len(inter_Q1_Rear3)/len(Rear3_set1[0:31])
conc_Q2_Rear3=len(inter_Q2_Rear3)/len(Rear3_set1[31:64])
conc_Q3_Rear3=len(inter_Q3_Rear3)/len(Rear3_set1[64:97])
conc_Q4_Rear3=len(inter_Q4_Rear3)/len(Rear3_set1[97:])
print("intersection of quartile intervals of set1 and set3 for Rear3")
print(inter_Q1_Rear3)
print(inter_Q2_Rear3)
print(inter_Q3_Rear3)
print(f"coincidence Q1= {conc_Q1_Rear3}, coincidence Q2= {conc_Q2_Rear3}, coincidence Q3= {conc_Q3_Rear3}, coincidence Q4= {conc_Q4_Rear3}")

##Organize all the information
#2 files (LSTM, GRU, BILSTM, BIGRU - TCN,CNNLSTM,CNNGRU) and 5 sheets (POA1,POA2,Rear1,Rear2,Rear3) a

#File 1
def create_df_end_gropu1(sensor1,tupla_sensor):
    Q1_set=tupla_sensor[0:31] #More difficult
    Q2_set=tupla_sensor[31:64]
    Q3_set=tupla_sensor[64:97]
    Q4_set=tupla_sensor[97:] #Easiest

    list_model=[]
    model_type=[]
    list_scaler=[]
    list_var=[]
    list_train=[]
    list_quartiles=[]
    list_mae=[]
    list_r2=[]
    list_mape=[]

    for metrics2 in sensor1.keys():

        if metrics2[-3:]=="ind":
            tipo="Individual"
        else:
            tipo="Integrated"

        current_df=sensor1[metrics2]

        for n_col in range(1,5):
            col_names_dic={1:"LSTM",2:"GRU",3:"BiLSTM",4:"BiGRU"}

            for n_row in range(0,16):
                if n_row in [0,1,2,3]:
                    scaler_type="Robust"
                    retrainig="No"
                elif n_row in [4,5,6,7]:
                    scaler_type="Robust"
                    retrainig="Yes"
                elif n_row in [8,9,10,11]:
                    scaler_type="MinMax"
                    retrainig="No"
                else:
                    scaler_type="MinMax"
                    retrainig="Yes"
                elemento_x=current_df.iloc[n_row,n_col]
                try:
                    Q_100=statistics.mean(elemento_x)
                except:
                    Q_100=None
                try:
                    Q_75=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if i not in Q1_set)
                except:
                    Q_75=None
                try:
                    Q_50=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if (i not in (Q1_set+Q2_set)))
                except:
                    Q_50=None
                try:
                    Q_25=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if (i not in (Q1_set+Q2_set+Q3_set)))
                except:
                    Q_25=None

                if metrics2[0:3]=="MAE":
                    for m in range(0,4):
                        list_model.append(col_names_dic[n_col])
                        model_type.append(tipo)
                        list_scaler.append(scaler_type)
                        list_var.append(current_df.iloc[n_row,0])
                        list_train.append(retrainig)
                    list_quartiles.append("Q100%")
                    list_mae.append(Q_100)
                    list_quartiles.append("Q75%")
                    list_mae.append(Q_75)
                    list_quartiles.append("Q50%")
                    list_mae.append(Q_50)
                    list_quartiles.append("Q25%")
                    list_mae.append(Q_25)
                elif metrics2[0:3]=="R2_":
                    list_r2.append(Q_100)
                    list_r2.append(Q_75)
                    list_r2.append(Q_50)
                    list_r2.append(Q_25)
                else:
                    list_mape.append(Q_100)
                    list_mape.append(Q_75)
                    list_mape.append(Q_50)
                    list_mape.append(Q_25)
    #The columns of the results table are: Model, Type, Scaler, Var, Retraining, Quartile, MAE, R2, MAPE
    dic_dat={"Model":list_model,"Type":model_type,"Scaler":list_scaler,"Var":list_var,"Retraining":list_train,
             "Quartile":list_quartiles,"MAE":list_mae,"R2":list_r2,"MAPE":list_mape}
    df_completed=pd.DataFrame(data=dic_dat)
    return df_completed

df_poa1_group1=create_df_end_gropu1(poa1_metrics,POA1_set1)
df_poa2_group1=create_df_end_gropu1(poa2_metrics,POA2_set1)
df_rear1_group1=create_df_end_gropu1(rear1_metrics,Rear1_set1)
df_rear2_group1=create_df_end_gropu1(rear2_metrics,Rear2_set1)
df_rear3_group1=create_df_end_gropu1(rear3_metrics,Rear3_set1)

with pd.ExcelWriter("Tesis_Results_group1B.xlsx") as writer:
    df_poa1_group1.to_excel(writer,sheet_name="POA1", index=False)
    df_poa2_group1.to_excel(writer,sheet_name="POA2", index=False)
    df_rear1_group1.to_excel(writer,sheet_name="Rear1", index=False)
    df_rear2_group1.to_excel(writer,sheet_name="Rear2", index=False)
    df_rear3_group1.to_excel(writer,sheet_name="Rear3", index=False)
print("File 1 created")


#File 2
def create_df_end_gropu2(sensor1,tupla_sensor):
    Q1_set=tupla_sensor[0:31] #More difficult
    Q2_set=tupla_sensor[31:64]
    Q3_set=tupla_sensor[64:97]
    Q4_set=tupla_sensor[97:] #Easiest

    list_model=[]
    model_type=[]
    list_scaler=[]
    list_var=[]
    list_train=[]
    list_quartiles=[]
    list_mae=[]
    list_r2=[]
    list_mape=[]

    for metrics2 in sensor1.keys():

        if metrics2[-3:]=="ind":
            tipo="Individual"
        else:
            tipo="Integrated"

        current_df=sensor1[metrics2]

        for n_col in range(5,8):
            col_names_dic={5:"TCN",6:"CNN_LSTM",7:"CNN_GRU"}

            for n_row in range(0,16):
                if n_row in [0,1,2,3]:
                    scaler_type="Robust"
                    retrainig="No"
                elif n_row in [4,5,6,7]:
                    scaler_type="Robust"
                    retrainig="Yes"
                elif n_row in [8,9,10,11]:
                    scaler_type="MinMax"
                    retrainig="No"
                else:
                    scaler_type="MinMax"
                    retrainig="Yes"
                elemento_x=current_df.iloc[n_row,n_col]
                try:
                    Q_100=statistics.mean(elemento_x)
                except:
                    Q_100=None
                try:
                    Q_75=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if i not in Q1_set)
                except:
                    Q_75=None
                try:
                    Q_50=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if (i not in (Q1_set+Q2_set)))
                except:
                    Q_50=None
                try:
                    Q_25=statistics.mean(elemento_x[i] for i in range(len(elemento_x)) if (i not in (Q1_set+Q2_set+Q3_set)))
                except:
                    Q_25=None

                if metrics2[0:3]=="MAE":
                    for m in range(0,4):
                        list_model.append(col_names_dic[n_col])
                        model_type.append(tipo)
                        list_scaler.append(scaler_type)
                        list_var.append(current_df.iloc[n_row,0])
                        list_train.append(retrainig)
                    list_quartiles.append("Q100%")
                    list_mae.append(Q_100)
                    list_quartiles.append("Q75%")
                    list_mae.append(Q_75)
                    list_quartiles.append("Q50%")
                    list_mae.append(Q_50)
                    list_quartiles.append("Q25%")
                    list_mae.append(Q_25)
                elif metrics2[0:3]=="R2_":
                    list_r2.append(Q_100)
                    list_r2.append(Q_75)
                    list_r2.append(Q_50)
                    list_r2.append(Q_25)
                else:
                    list_mape.append(Q_100)
                    list_mape.append(Q_75)
                    list_mape.append(Q_50)
                    list_mape.append(Q_25)
    #The columns of the results table are: Model, Type, Scaler, Var, Retraining, Quartile, MAE, R2, MAPE
    dic_dat={"Model":list_model,"Type":model_type,"Scaler":list_scaler,"Var":list_var,"Retraining":list_train,
             "Quartile":list_quartiles,"MAE":list_mae,"R2":list_r2,"MAPE":list_mape}
    df_completed=pd.DataFrame(data=dic_dat)
    return df_completed

df_poa1_group2=create_df_end_gropu2(poa1_metrics,POA1_set2)
df_poa2_group2=create_df_end_gropu2(poa2_metrics,POA2_set2)
df_rear1_group2=create_df_end_gropu2(rear1_metrics,Rear1_set2)
df_rear2_group2=create_df_end_gropu2(rear2_metrics,Rear2_set2)
df_rear3_group2=create_df_end_gropu2(rear3_metrics,Rear3_set2)

with pd.ExcelWriter("Tesis_results_group2B.xlsx") as writer2:
    df_poa1_group2.to_excel(writer2,sheet_name="POA1", index=False)
    df_poa2_group2.to_excel(writer2,sheet_name="POA2", index=False)
    df_rear1_group2.to_excel(writer2,sheet_name="Rear1", index=False)
    df_rear2_group2.to_excel(writer2,sheet_name="Rear2", index=False)
    df_rear3_group2.to_excel(writer2,sheet_name="Rear3", index=False)

print("File 2 created")