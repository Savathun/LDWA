class Database:
    def __init__(self, db):
        from sqlite3 import connect
        self.conn = connect(db)
        self.cur = self.conn.cursor()

    def fetch(self, table):
        self.cur.execute("SELECT * FROM " + table)
        return self.cur.fetchall()


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
    from requests import get
    manifest_location = get("https://www.bungie.net/platform/Destiny2/Manifest/",
                            headers={"X-API-Key": open('api_key.txt', "r").read()}).json()['Response'][
        'mobileWorldContentPaths']['en']
    return (True, manifest_location) if open('manifest\\manifest_version.txt',
                                             "r+").read() != manifest_location.split('/')[-1][18:-8] else (False, 0)


def generate_pickle(db, name, columns):
    from pandas import json_normalize
    from json import loads
    table_list = [[entry[0], loads(entry[1])] for entry in db.fetch('Destiny' + name + "Definition")]
    table_df = json_normalize([entry[1] for entry in table_list], sep='_')
    table_df.index = [entry[0] for entry in table_list]
    table_df[columns].to_pickle('manifest\\{}_dataframe.pkl'.format(name))


def generate_weapons_dataframe(inventory_df, perk_df, plug_sets_df, damage_type_df, slot_df):
    def reduce_inventory_to_weapons(inventory_df):
        def refine_socket_entries(inventory_df):
            inventory_df[['sockets_socketEntries_{}'.format(x) for x in
                          range(len(inventory_df.iloc[1]['sockets_socketEntries']))]] = DataFrame(
                inventory_df['sockets_socketEntries'].values.tolist(),
                index=inventory_df.index)
            inventory_df['sockets_socketEntries_0_singleInitialItemHash'] = DataFrame(
                inventory_df['sockets_socketEntries_0'].apply(lambda x: x['singleInitialItemHash']),
                index=inventory_df.index)
            inventory_df[['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = DataFrame(
                inventory_df[['sockets_socketEntries_{}'.format(x) for x in range(1, 5)]].apply(
                    lambda x: x.apply(lambda y: y['randomizedPlugSetHash'] if 'randomizedPlugSetHash' in y else 0)),
                index=inventory_df.index)
            return inventory_df.drop(
                ['sockets_socketEntries'] + ['sockets_socketEntries_{}'.format(x) for x in range(0, 10)], axis=1)

        from pandas import concat, Series
        inventory_df = inventory_df[(inventory_df['itemType'] == 3) &
                                    (inventory_df['inventory_tierTypeName'] == 'Legendary')].explode('quality_versions')
        inventory_df = concat([inventory_df.drop(['quality_versions'], axis=1),
                               inventory_df['quality_versions'].apply(Series)], axis=1)
        return refine_socket_entries(
            inventory_df[inventory_df['powerCapHash'] == 2759499571].drop_duplicates(subset=['displayProperties_name'])[
                ['itemTypeDisplayName', 'displayProperties_name', 'defaultDamageTypeHash',
                 'equippingBlock_equipmentSlotTypeHash', 'equippingBlock_ammoType', 'sockets_socketEntries']])

    from pandas import DataFrame
    ammo_type_list = ['None', 'Primary', 'Special', 'Heavy', 'Unknown']
    weapons_df = reduce_inventory_to_weapons(inventory_df)
    weapons_df['defaultDamageTypeHash'] = DataFrame(
        weapons_df['defaultDamageTypeHash'].apply(
            lambda x: damage_type_df.loc[damage_type_df['hash'] == x]['displayProperties_name'].values[0]),
        index=weapons_df.index)
    weapons_df['equippingBlock_equipmentSlotTypeHash'] = DataFrame(
        weapons_df['equippingBlock_equipmentSlotTypeHash'].apply(
            lambda x: slot_df.loc[slot_df['hash'] == x]['displayProperties_name'].values[0].split(' ')[0]),
        index=weapons_df.index)
    weapons_df['equippingBlock_ammoType'] = DataFrame(
        weapons_df['equippingBlock_ammoType'].apply(
            lambda x: ammo_type_list[int(x)]),
        index=weapons_df.index)
    weapons_df['sockets_socketEntries_0_singleInitialItemHash'] = DataFrame(
        weapons_df['sockets_socketEntries_0_singleInitialItemHash'].apply(
            lambda x: perk_df.loc[perk_df['hash'] == x]['displayProperties_name'].values[0]),
        index=weapons_df.index)
    weapons_df[['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = DataFrame(
        weapons_df[['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]].apply(
            lambda x: x.apply(
                lambda y: [
                    perk_df.loc[perk_df['hash'] == z['plugItemHash']]['displayProperties_name'].values[0] for z
                    in plug_sets_df.loc[plug_sets_df['hash'] == y]['reusablePlugItems'].values[0] if
                    z['currentlyCanRoll']] if y != 0 else ['Static'])),
        index=weapons_df.index)
    return weapons_df


def main():
    update_needed, location = check_manifest_updates()
    if update_needed:
        open('manifest\\manifest_version.txt', "r+").write(location.split('/')[-1][18:-8])
        retrieve_manifest(location)
    from os.path import exists
    if not exists('manifest\\manifest.sqlite') or update_needed:
        extract_manifest()
    db = None
    for name, columns in zip(['InventoryItem', 'DamageType', 'EquipmentSlot', 'PlugSet'],
                             [['hash', 'itemCategoryHashes', 'itemTypeDisplayName', 'displayProperties_name',
                               'itemType', 'equippingBlock_equipmentSlotTypeHash', 'inventory_tierTypeName',
                               'quality_versions', 'equippingBlock_ammoType', 'sockets_socketEntries',
                               'defaultDamageTypeHash'], ['hash', 'displayProperties_name'],
                              ['hash', 'displayProperties_name'], ['hash', 'reusablePlugItems']]):
        if not exists('manifest\\{}_dataframe.pkl'.format(name)) or update_needed:
            db = Database('manifest\\manifest.sqlite') if not None else db
            generate_pickle(db, name, columns)
    if not exists('manifest\\weapons_dataframe.pkl') or update_needed:
        from pandas import read_pickle
        inventory_df = read_pickle('manifest\\InventoryItem_dataframe.pkl')
        if not exists('manifest\\perk_dataframe.pkl') or update_needed:
            inventory_df[
                inventory_df['itemCategoryHashes'].apply(lambda x: 610365472 in x if type(x) is list else False)][
                ['hash', 'displayProperties_name']].to_pickle('manifest\\perk_dataframe.pkl')
        if not exists('manifest\\weapons_dataframe.pkl') or update_needed:
            generate_weapons_dataframe(inventory_df,
                                       read_pickle('manifest\\perk_dataframe.pkl'),
                                       read_pickle('manifest\\PlugSet_dataframe.pkl'),
                                       read_pickle('manifest\\DamageType_dataframe.pkl'),
                                       read_pickle('manifest\\EquipmentSlot_dataframe.pkl')
                                       ).to_pickle('manifest\\weapons_dataframe.pkl')
    from pandas import read_pickle
    weapons_df = read_pickle('manifest\\weapons_dataframe.pkl')
    weapons_df.columns = ['Type', 'Name', 'Element', 'Slot', 'Ammo', 'Archetype',
                          'perk_column_1', 'perk_column_2', 'perk_column_3', 'perk_column_4']


if __name__ == '__main__':
    main()
