#Import pandas to manipulate data
import pandas as pd

#Open file with results for 2022 PDT test
data_1 = pd.read_csv('pdt_2022_data.csv', sep = ',')

#Keeping only the columns without massive missing data
data_1_cleaned = data_1[['MRUN', 'COD_SEXO','CODIGO_ENS', 'DEPENDENCIA', 'CODIGO_COMUNA_EGRESO',
                   'NOMBRE_COMUNA_EGRESO', 'ANYO_DE_EGRESO', 'PROMEDIO_NOTAS',
                   'PTJE_NEM', 'PORC_SUP_NOTAS', 'PTJE_RANKING', 'CLEC_ACTUAL',
                   'MATE_ACTUAL', 'HCSO_ACTUAL', 'CIEN_ACTUAL', 'PROM_CM_ACTUAL', 'RURAL_RBD']]
del data_1

#Dropping all the records without PROMEDIO_NOTAS and PTJE_NEM
data_1_cleaned = data_1_cleaned[data_1_cleaned.PROMEDIO_NOTAS != 0]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PROMEDIO_NOTAS != "0"]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PROMEDIO_NOTAS != ""]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PROMEDIO_NOTAS != " "]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PTJE_NEM != 0]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PTJE_NEM != "0"]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PTJE_NEM != ""]
data_1_cleaned = data_1_cleaned[data_1_cleaned.PTJE_NEM != " "]

#Dropping all the records without CODIGO_ENS
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != ""]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != " "]

#Droping all records where CODIGO_ENS is for adults education
data_1_cleaned = data_1_cleaned.astype({'CODIGO_ENS' : 'int'})
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 360]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 361]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 362]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 363]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 460]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 461]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 463]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 560]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 561]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 563]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 660]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 661]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 663]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 760]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 761]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 763]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 860]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 863]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CODIGO_ENS != 963]

#Dropping all the records without scores in CLEC_ACTUAL and MATE_ACTUAL
data_1_cleaned = data_1_cleaned[data_1_cleaned.CLEC_ACTUAL != 0]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CLEC_ACTUAL != "0"]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CLEC_ACTUAL != ""]
data_1_cleaned = data_1_cleaned[data_1_cleaned.CLEC_ACTUAL != " "]
data_1_cleaned = data_1_cleaned[data_1_cleaned.MATE_ACTUAL != 0]
data_1_cleaned = data_1_cleaned[data_1_cleaned.MATE_ACTUAL != "0"]
data_1_cleaned = data_1_cleaned[data_1_cleaned.MATE_ACTUAL != ""]
data_1_cleaned = data_1_cleaned[data_1_cleaned.MATE_ACTUAL != " "]

#Make sure all the numeric columns are floats or integers
#First replace decimal symbols from comas to dots
data_1_cleaned['PROMEDIO_NOTAS'] = data_1_cleaned['PROMEDIO_NOTAS'].str.replace(',' , '.')
data_1_cleaned['PROM_CM_ACTUAL'] = data_1_cleaned['PROM_CM_ACTUAL'].str.replace(',' , '.')
#Cast to float
data_1_cleaned = data_1_cleaned.astype({'PROMEDIO_NOTAS' : 'float',
                                        'PROM_CM_ACTUAL' : 'float'})
#Cast to integer
data_1_cleaned = data_1_cleaned.astype({'PTJE_NEM' : 'int',
                                        'PORC_SUP_NOTAS' : 'int',
                                        'PTJE_RANKING' : 'int',
                                        'CLEC_ACTUAL' : 'int',
                                        'MATE_ACTUAL' : 'int',
                                        'HCSO_ACTUAL' : 'int',
                                        'CIEN_ACTUAL' : 'int'})


#Now we make some data binary for the sake of linear regression
#CODIGO_ENS --> 0:T-P y 1:H-C
data_1_cleaned.loc[data_1_cleaned["CODIGO_ENS"] != 310, "CODIGO_ENS"] = 0
data_1_cleaned.loc[data_1_cleaned["CODIGO_ENS"] == 310, "CODIGO_ENS"] = 1

#DEPENDENCIA --> 1:Particular Pagado 0: all the rest
data_1_cleaned = data_1_cleaned.astype({'DEPENDENCIA' : 'int'})
data_1_cleaned.loc[data_1_cleaned["DEPENDENCIA"] != 4, "DEPENDENCIA"] = 0
data_1_cleaned.loc[data_1_cleaned["DEPENDENCIA"] == 4, "DEPENDENCIA"] = 1

#Check
print(list(data_1_cleaned))
print(data_1_cleaned.shape)

data_1_cleaned.to_csv('pdt_2022_data_refined.csv')
del data_1_cleaned