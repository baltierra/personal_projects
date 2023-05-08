#Import pandas to manipulate data
import pandas as pd

#Open file with results for 2022 PDT test
data_1 = pd.read_csv('A_INSCRITOS_PUNTAJES_PDT_2022_PUB_MRUN.csv', sep = ';')

#Keep only the columns we are interested in
data_1_cleaned = data_1[['MRUN', 'COD_SEXO','CODIGO_ENS', 'DEPENDENCIA', 'CODIGO_COMUNA_EGRESO',
                   'NOMBRE_COMUNA_EGRESO', 'ANYO_DE_EGRESO', 'PROMEDIO_NOTAS',
                   'PTJE_NEM', 'PORC_SUP_NOTAS', 'PTJE_RANKING', 'CLEC_ACTUAL',
                   'MATE_ACTUAL', 'HCSO_ACTUAL', 'CIEN_ACTUAL', 'PROM_CM_ACTUAL']]
#Only keep those students graduated the year before of the test
data_1_cleaned = data_1_cleaned[data_1_cleaned.ANYO_DE_EGRESO == 2021]
del data_1

#Now open academic performance of students at highschool data
data_2 = pd.read_csv('20220302_Rendimiento_2021_20220131_WEB.csv', sep = ';')
#Keep only the columns we are interested in
data_2_cleaned = data_2[['MRUN', 'RURAL_RBD', 'PROM_GRAL', 'ASISTENCIA']]
#Delete already used data frame
del data_2

#Match academic performance data with PDT results by MRUN using a join
new_data = data_1_cleaned.join(data_2_cleaned, on = 'MRUN', how = 'left', lsuffix = '_left', rsuffix = '_right')
#Delete already used data frames
del data_1_cleaned
del data_2_cleaned
#Drop the repeated column because of the join 
new_data = new_data.drop(['MRUN_right'], axis=1)

#Now open students economic situation data
data_3 = pd.read_csv('B_SOCIOECONOMICO_DOMICILIO_PDT_2022_PUB_MRUN.csv', sep = ';')
#Keep only the columns we are interested in
data_3_cleaned = data_3[['MRUN', 'INGRESO_PERCAPITA_GRUPO_FA', 'EDUCACION_MADRE',
                         'EDUCACION_PADRE', 'HOGAR_CONEXION_INTERNET']]
#Delete already used data frame
del data_3

#Match students economic data with existing data by MRUN using a join
final_data = new_data.join(data_3_cleaned, on = 'MRUN_left', how = 'left', lsuffix = '_left', rsuffix = '_right')
#Delete already used data frames
del data_3_cleaned
del new_data
#Drop the repeated column because of the join and rename the MRUN column
final_data = final_data.drop(['MRUN'], axis=1)
final_data.rename(columns = {'MRUN_left':'MRUN'}, inplace = True)

#Check result
print(list(final_data.columns))
print(final_data.shape)

#Export data frame as csv
final_data.to_csv('pdt_2022_data.csv')
del final_data