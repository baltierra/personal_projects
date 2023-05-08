import pandas as pd 
data_1 = pd.read_csv('[Original]weights_career_demre.csv', sep = ',')
data_2 = pd.read_csv('base_cris_3.csv', sep = ',')

#print(data_2)

sim_2022_weighted_careers = data_1.merge(data_2, on='unique_code', how='right')
sim_2022_weighted_careers.fillna(0, inplace=True)
sim_2022_weighted_careers['demre_code'] = sim_2022_weighted_careers['demre_code'].astype(int)

#print(sim_2022_weighted_careers)

sim_2022_weighted_careers['ingreso_directo'] = sim_2022_weighted_careers['ingreso_directo'].astype(int)
sim_2022_weighted_careers = sim_2022_weighted_careers[(sim_2022_weighted_careers[['tipoies',
                                                                                  'region',
                                                                                  'nombreies',
                                                                                  'nombrecarrera']] != 0).all(axis=1)]

print(sim_2022_weighted_careers)
sim_2022_weighted_careers.to_csv('all_sim_2022_weighted_careers.csv', index=False)
