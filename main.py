import json
import pandas as pd
import numpy as np


def retrieve_manifest(manifest_location):
    """ """
    import urllib.request
    urllib.request.urlretrieve('https://www.bungie.net' + manifest_location, 'manifest\\manifest.zip')


def extract_manifest():
    from zipfile import ZipFile
    with ZipFile('manifest\\manifest.zip', 'r') as zipObj:
        zipObj.infolist()[0].filename = 'manifest.sqlite'
        zipObj.extract(zipObj.infolist()[0], path='manifest')


def check_manifest_updates():
    import requests
    with open('api_key.txt', "r") as file:
        api_key = file.read()
    file.close()
    manifest_version = open('manifest\\manifest_version.txt', "r+")
    HEADERS = {"X-API-Key": api_key}
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/", headers=HEADERS)
    manifest_location = r.json()['Response']['mobileWorldContentPaths']['en']
    if manifest_version.read() != manifest_location.split('/')[-1][18:-8]:
        manifest_version.seek(0)
        manifest_version.write(manifest_location.split('/')[-1][18:-8])
        retrieve_manifest(manifest_location)
        extract_manifest()
    manifest_version.close()


def connect_db():
    import dbclass
    db = dbclass.Database('manifest\\manifest.sqlite')
    return db


def retrieve_inventory_items_table(db):
    inventory_items = db.fetch("DestinyInventoryItemDefinition")
    inventory_items = [[entry[0], json.loads(entry[1])] for entry in inventory_items]
    return inventory_items


def create_dataframe(inventory_items):
    inventory_df = pd.json_normalize([entry[1] for entry in inventory_items])
    inventory_df.index = [entry[0] for entry in inventory_items]
    return inventory_df


def reduce_dataframe(inventory_df):
    inventory_df = inventory_df.explode('quality.versions')
    inventory_df = pd.concat([inventory_df.drop(['quality.versions'], axis=1),
                              inventory_df['quality.versions'].apply(pd.Series)], axis=1)
    inventory_df = inventory_df[inventory_df['powerCapHash'] == 2759499571]
    inventory_df = inventory_df.drop_duplicates(subset=['displayProperties.name'])
    inventory_df = inventory_df.drop(inventory_df.std()[(inventory_df.std() == 0)].index, axis=1)
    for column in inventory_df.columns:
        try:
            inventory_df[column] = inventory_df[column].apply(lambda y: np.nan if len(y) == 0 else y)
            if len(set(inventory_df[column])) == 1:
                inventory_df = inventory_df.drop([column], axis=1)
        except TypeError:
            pass
    inventory_df = inventory_df.dropna(axis='columns', how='all')
    return inventory_df


def create_csv(inventory_df):
    inventory_df['flavorText'] = inventory_df['flavorText'].replace(r'\n', ' ', regex=True)
    inventory_df.to_csv('manifest\\dataframe.csv', index=True)


def main():
    check_manifest_updates()
    db = connect_db()
    inventory_items = retrieve_inventory_items_table(db)
    inventory_df = create_dataframe(inventory_items)
    inventory_df = reduce_dataframe(inventory_df)
    create_csv(inventory_df)


if __name__ == '__main__':
    main()
