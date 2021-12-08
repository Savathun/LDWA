import sqlite3
import numpy as np
import pandas
import sqlalchemy
import time
import urllib.error
import urllib.request
import os
import lists_sets_dicts as data


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch(self, table):
        self.cur.execute("SELECT * FROM " + table)
        return self.cur.fetchall()


def generate_sql_database():
    engine = sqlalchemy.create_engine('sqlite:///../android/app/src/main/assets/weapons_database.sqlite', echo=False)
    weapons_df = pandas.read_pickle('dataframes/weapons_dataframe.pkl')
    weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']] = pandas.DataFrame(
        weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']].apply(
            lambda x: x.apply(lambda y: str(str(y).strip('[]{}')))), index=weapons_df.index)
    weapons_df.to_sql('weapons', con=engine, if_exists="replace")
    pandas.read_pickle('dataframes/perk_dataframe.pkl').to_sql('perks', con=engine, if_exists="replace")
    pandas.DataFrame.from_dict({'locale': ['en-US']}).to_sql('android_metadata', con=engine, if_exists="replace")


def create_image_archive():
    def download_image(db_path, local_dir):
        local_path = local_dir + db_path[25:].replace('/', '_').lower()
        try:
            if not (path == np.nan or os.path.exists(local_path)):
                urllib.request.urlretrieve('https://www.bungie.net' + db_path, local_path)
        except TypeError:
            return
        except urllib.error.HTTPError:
            time.sleep(150)
            urllib.request.urlretrieve('https://www.bungie.net' + db_path, local_path)

    weapons_df = pandas.read_pickle('dataframes/weapons_dataframe.pkl')
    perk_df = pandas.read_pickle('dataframes/perk_dataframe.pkl')
    for col in ['Icon', 'Screenshot', 'AmmoIcon', 'ElementIcon']:
        for path in weapons_df[col].values.tolist():
            if col == 'Screenshot':
                download_image(path, '../android/app/src/main/res/drawable/')
            else:
                download_image(path, '../android/app/src/main/res/mipmap-xxhdpi/')
    for perk in data.generate_set_of_available_traits(weapons_df):
        path = perk_df.loc[perk_df['displayProperties_name'] == perk]['displayProperties_icon'].values[0]
        download_image(path, '../android/app/src/main/res/mipmap-xxhdpi/')

