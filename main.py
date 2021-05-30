import json
import os

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
    headers = {"X-API-Key": api_key}
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/", headers=headers)
    manifest_location = r.json()['Response']['mobileWorldContentPaths']['en']
    return (True, manifest_location) if manifest_version.read() != manifest_location.split('/')[-1][18:-8] else (False,
                                                                                                                 0)


def connect_db():
    import dbclass
    db = dbclass.Database('manifest\\manifest.sqlite')
    return db


def retrieve_table(db, table_name):
    table_list = db.fetch(table_name)
    table_list = [[entry[0], json.loads(entry[1])] for entry in table_list]
    return table_list


def create_dataframe(table_list):
    table_df = pd.json_normalize([entry[1] for entry in table_list])
    table_df.index = [entry[0] for entry in table_list]
    return table_df


def reduce_dataframe(inventory_df):
    def reduce_rows(inventory_df):
        inventory_df = inventory_df[inventory_df['itemType'] == 3]
        inventory_df = inventory_df[inventory_df['inventory.tierTypeName'] == 'Legendary']
        inventory_df = inventory_df.explode('quality.versions')
        inventory_df = pd.concat([inventory_df.drop(['quality.versions'], axis=1),
                                  inventory_df['quality.versions'].apply(pd.Series)], axis=1)
        inventory_df = inventory_df[inventory_df['powerCapHash'] == 2759499571]
        inventory_df = inventory_df.drop_duplicates(subset=['displayProperties.name'])
        return inventory_df

    def reduce_cols(inventory_df):
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

    inventory_df = reduce_rows(inventory_df)
    inventory_df = reduce_cols(inventory_df)
    return inventory_df


def create_csv(inventory_df):
    inventory_df['flavorText'] = inventory_df['flavorText'].replace(r'\n', ' ', regex=True)
    inventory_df.to_csv('manifest\\dataframe.csv', index=True)


def create_from_csv():
    return pd.read_csv('manifest\\dataframe.csv', index_col=0)


def select_needed_columns(inventory_df):
    refined_df = inventory_df[
        ['itemTypeDisplayName', 'displayProperties.name', 'defaultDamageType', 'equippingBlock.equipmentSlotTypeHash',
         'equippingBlock.ammoType', 'sockets.socketEntries']].copy()
    return refined_df


def refine_socket_entries(refined_df):
    import ast
    refined_df[['sockets.socketEntries.{}'.format(x) for x in
                range(len(ast.literal_eval(refined_df.iloc[1]['sockets.socketEntries'])))]] = pd.DataFrame(
        refined_df['sockets.socketEntries'].apply(lambda x: ast.literal_eval(x)).values.tolist(),
        index=refined_df.index)
    refined_df['sockets.socketEntries.0.singleInitialItemHash'] = pd.DataFrame(
        refined_df['sockets.socketEntries.0'].apply(lambda x: x['singleInitialItemHash']), index=refined_df.index)
    refined_df[['sockets.socketEntries.{}.randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = pd.DataFrame(
        refined_df[['sockets.socketEntries.{}'.format(x) for x in range(1, 5)]].apply(
            lambda x: x.apply(lambda y: y['randomizedPlugSetHash'] if 'randomizedPlugSetHash' in y else np.nan)),
        index=refined_df.index)
    refined_df = refined_df.drop(
        ['sockets.socketEntries'] + ['sockets.socketEntries.{}'.format(x) for x in range(0, 10)], axis=1)
    return refined_df


def main():
    update_needed, location = check_manifest_updates()
    if update_needed:
        manifest_version = open('manifest\\manifest_version.txt', "r+")
        manifest_version.seek(0)
        manifest_version.write(location.split('/')[-1][18:-8])
        retrieve_manifest(location)
    if not os.path.exists('manifest\\manifest.sqlite') or update_needed:
        extract_manifest()
    if not os.path.exists('manifest\\dataframe.csv') or update_needed:
        db = connect_db()
        inventory_df = create_dataframe(retrieve_table(db, "DestinyInventoryItemDefinition"))
        inventory_df = reduce_dataframe(inventory_df)
        create_csv(inventory_df)
    inventory_df = create_from_csv()
    refined_df = select_needed_columns(inventory_df)
    refined_df = refine_socket_entries(refined_df)
    refined_df.to_csv('manifest\\refined_dataframe.csv', index=True)


if __name__ == '__main__':
    main()
