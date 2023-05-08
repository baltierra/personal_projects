from django.core.management.base import BaseCommand
import sqlite3
import pandas as pd

class Command(BaseCommand):
    help = 'Populates Sqlite3 Data Base'

    def handle(self, *args, **kwargs):
        self.stdout.write("This will populate the Data Base")
        
        # conn = sqlite3.connect('db.sqlite3')
        # c = conn.cursor()

        # # load the data into a Pandas DataFrame
        # users = pd.read_csv('weights_career_demre.csv')
        # # write the data to a sqlite table
        # users.to_sql('app_sim_weightedcareer', conn, if_exists='append', index = False)

        # print(c.execute('''SELECT * FROM app_sim_weightedcareer''').fetchall())
        # c.close()