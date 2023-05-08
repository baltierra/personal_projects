import pandas as pd
import json

with open('/Users/fabs/Documents/_UChicago/Q4_Autumn/capp30239_DVPA/CAPP30239_FA22/week_06/homework/a3cleanedonly2015.json') as f:
    d = json.load(f)

df = pd.DataFrame(d)

df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y").dt.month_name()

deaths_by_month = df[['Date']]
deaths_by_month['Deaths'] = ''
total_deaths_by_month = deaths_by_month.groupby('Date').agg({"Deaths":["count"]})
print(total_deaths_by_month)
total_deaths_by_month.to_csv('total_deaths_by_month.csv')


deaths_by_gender = df[['Gender']]
deaths_by_gender['Deaths'] = ''
total_deaths_by_gender = deaths_by_gender.groupby('Gender').agg({"Deaths":["count"]})
total_deaths_by_gender.to_csv('total_deaths_by_gender.csv')


deaths_by_race = df[['Race']]
deaths_by_race['Deaths'] = ''
total_deaths_by_race = deaths_by_race.groupby('Race').agg({"Deaths":["count"]})
total_deaths_by_race.to_csv('total_deaths_by_race.csv')


deaths_by_mental = df[['Mental_illness']]
deaths_by_mental['Deaths'] = 1
total_deaths_by_mental = deaths_by_mental.groupby('Mental_illness').agg({"Deaths":["count"]})
total_deaths_by_mental.to_csv('total_deaths_by_mental.csv')


deaths_by_manner = df[['Manner_of_death']]
deaths_by_manner['Deaths'] = 1
total_deaths_by_manner = deaths_by_manner.groupby('Manner_of_death').agg({"Deaths":["count"]})
total_deaths_by_manner.to_csv('total_deaths_by_manner.csv')


deaths_by_race_month = df[['Date','Race']]
deaths_by_race_month['Deaths'] = ''
total_deaths_by_race_month = deaths_by_race_month.groupby(['Date','Race']).agg({"Deaths":["count"]})
total_deaths_by_race_month = total_deaths_by_race_month.reset_index()
print(total_deaths_by_race_month)
total_deaths_by_race_month.to_csv('test.csv', index=False)
data = total_deaths_by_race_month.to_json(orient='records')


