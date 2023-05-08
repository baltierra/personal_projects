import pandas as pd
import json

df = pd.read_csv('clean_data_total.csv', sep = ',')

years = set(df.Year.unique())
# years.remove(1990)
# years.remove(1991)
# years.remove(1992)
# years.remove(1993)
# years.remove(1994)
# years.remove(1995)
# years.remove(1996)
years.remove(2020)
# print(years)
# print(len(years))
countries = set(df.Country.unique())
countries.remove('United States')
# countries.remove('Israel')
# print(countries)
# print(len(countries))
gases = set(df.Pollutant.unique())
gases.remove('Greenhouse gases')
# print(gases)
# print(len(gases))

# print(len(df.loc[(df['Year'] == 1990) & 
#              (df['Country'] == 'Latvia') & 
#              (df['Pollutant'] == 'Sulphur hexafluoride'), 
#              'Value']))

data = {"name" : "Years", "children" : []}

for y, year in enumerate(years):
    data["children"].append({"name" : str(year),
                             "children" : [],
                             "color" : "#1f77b4",
                             "opacity" : 0.75})
    for c, country in enumerate(countries):
        data["children"][y]["children"].append({"name" : str(country),
                                                "children" : [],
                                                "color" : "#1f77b4",
                                                "opacity" : 0.50})
        for gas in gases:
            value = 0
            if len(df.loc[(df['Year'] == year) & 
                      (df['Country'] == country) & 
                      (df['Pollutant'] == gas), 'Value']) > 0:
                value = df.loc[(df['Year'] == int(year)) & 
                        (df['Country'] == country) & 
                        (df['Pollutant'] == gas), 
                        'Value'].item()
            data["children"][y]["children"][c]['children'].append({"name" : str(gas),
                                                        "value" : value,
                                                        "color" : "#1f77b4",
                                                        "opacity" : 0.25})

with open("GHG_data_all.json", "w") as write_file:
    json.dump(data, write_file, indent=4)   
# with open("GHG_data_all-USA.json", "w") as write_file:
#     json.dump(data, write_file, indent=4)
    
# data_1 = data_1[data_1.POLL == 'GHG']
# print(data_1)

# data_1.to_csv('totalGHG.csv', index=False)
# df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y").dt.month_name()

# deaths_by_month = df[['Date']]
# deaths_by_month['Deaths'] = ''
# total_deaths_by_month = deaths_by_month.groupby('Date').agg({"Deaths":["count"]})
# print(total_deaths_by_month)
# total_deaths_by_month.to_csv('total_deaths_by_month.csv')


# deaths_by_gender = df[['Gender']]
# deaths_by_gender['Deaths'] = ''
# total_deaths_by_gender = deaths_by_gender.groupby('Gender').agg({"Deaths":["count"]})
# total_deaths_by_gender.to_csv('total_deaths_by_gender.csv')


# deaths_by_race = df[['Race']]
# deaths_by_race['Deaths'] = ''
# total_deaths_by_race = deaths_by_race.groupby('Race').agg({"Deaths":["count"]})
# total_deaths_by_race.to_csv('total_deaths_by_race.csv')


# deaths_by_mental = df[['Mental_illness']]
# deaths_by_mental['Deaths'] = 1
# total_deaths_by_mental = deaths_by_mental.groupby('Mental_illness').agg({"Deaths":["count"]})
# total_deaths_by_mental.to_csv('total_deaths_by_mental.csv')


# deaths_by_manner = df[['Manner_of_death']]
# deaths_by_manner['Deaths'] = 1
# total_deaths_by_manner = deaths_by_manner.groupby('Manner_of_death').agg({"Deaths":["count"]})
# total_deaths_by_manner.to_csv('total_deaths_by_manner.csv')


# deaths_by_race_month = df[['Date','Race']]
# deaths_by_race_month['Deaths'] = ''
# total_deaths_by_race_month = deaths_by_race_month.groupby(['Date','Race']).agg({"Deaths":["count"]})
# total_deaths_by_race_month = total_deaths_by_race_month.reset_index()
# print(total_deaths_by_race_month)
# total_deaths_by_race_month.to_csv('test.csv', index=False)
# data = total_deaths_by_race_month.to_json(orient='records')


