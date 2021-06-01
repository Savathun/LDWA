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


def retrieve_table(db, table_name):
    table_list = db.fetch(table_name)
    table_list = [[entry[0], json.loads(entry[1])] for entry in table_list]
    return table_list


def create_dataframe(table_list):
    table_df = pd.json_normalize([entry[1] for entry in table_list])
    table_df.index = [entry[0] for entry in table_list]
    return table_df


def reduce_dataframe(inventory_df):
    inventory_df = inventory_df[inventory_df['itemType'] == 3]
    inventory_df = inventory_df[inventory_df['inventory.tierTypeName'] == 'Legendary']
    inventory_df = inventory_df.explode('quality.versions')
    inventory_df = pd.concat([inventory_df.drop(['quality.versions'], axis=1),
                              inventory_df['quality.versions'].apply(pd.Series)], axis=1)
    inventory_df = inventory_df[inventory_df['powerCapHash'] == 2759499571]
    inventory_df = inventory_df.drop_duplicates(subset=['displayProperties.name'])
    return inventory_df


def select_needed_columns(inventory_df):
    refined_df = inventory_df[
        ['itemTypeDisplayName', 'displayProperties.name', 'defaultDamageTypeHash',
         'equippingBlock.equipmentSlotTypeHash',
         'equippingBlock.ammoType', 'sockets.socketEntries']].copy()
    return refined_df


def refine_socket_entries(refined_df):
    refined_df[['sockets.socketEntries.{}'.format(x) for x in
                range(len(refined_df.iloc[1]['sockets.socketEntries']))]] = pd.DataFrame(
        refined_df['sockets.socketEntries'].values.tolist(),
        index=refined_df.index)
    refined_df['sockets.socketEntries.0.singleInitialItemHash'] = pd.DataFrame(
        refined_df['sockets.socketEntries.0'].apply(lambda x: x['singleInitialItemHash']), index=refined_df.index)
    refined_df[['sockets.socketEntries.{}.randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = pd.DataFrame(
        refined_df[['sockets.socketEntries.{}'.format(x) for x in range(1, 5)]].apply(
            lambda x: x.apply(lambda y: y['randomizedPlugSetHash'] if 'randomizedPlugSetHash' in y else 0)),
        index=refined_df.index)
    refined_df = refined_df.drop(
        ['sockets.socketEntries'] + ['sockets.socketEntries.{}'.format(x) for x in range(0, 10)], axis=1)
    return refined_df


def convert_hashes(weapons_df, perk_df, plug_sets_df, damage_type_df, slot_df):
    weapons_df['defaultDamageTypeHash'] = pd.DataFrame(
        weapons_df['defaultDamageTypeHash'].apply(
            lambda x: damage_type_df.loc[damage_type_df['hash'] == x]['displayProperties.name'].values[0]),
        index=weapons_df.index)
    weapons_df['equippingBlock.equipmentSlotTypeHash'] = pd.DataFrame(
        weapons_df['equippingBlock.equipmentSlotTypeHash'].apply(
            lambda x: slot_df.loc[slot_df['hash'] == x]['displayProperties.name'].values[0].split(' ')[0]),
        index=weapons_df.index)
    ammo_type_list = ['None', 'Primary', 'Special', 'Heavy', 'Unknown']
    weapons_df['equippingBlock.ammoType'] = pd.DataFrame(
        weapons_df['equippingBlock.ammoType'].apply(lambda x: ammo_type_list[int(x)]), index=weapons_df.index)
    weapons_df['sockets.socketEntries.0.singleInitialItemHash'] = pd.DataFrame(
        weapons_df['sockets.socketEntries.0.singleInitialItemHash'].apply(
            lambda x: perk_df.loc[perk_df['hash'] == x]['displayProperties.name'].values[0]),
        index=weapons_df.index)
    weapons_df[
        ['sockets.socketEntries.{}.randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = pd.DataFrame(
        weapons_df[
            ['sockets.socketEntries.{}.randomizedPlugSetHash'.format(x) for x in range(1, 5)]].apply(
            lambda x: x.apply(
                lambda y: [
                    perk_df.loc[perk_df['hash'] == z['plugItemHash']]['displayProperties.name'].values[0] for z
                    in plug_sets_df.loc[plug_sets_df['hash'] == y]['reusablePlugItems'].values[0] if
                    z['currentlyCanRoll']] if y != 0 else ['Static'])),
        index=weapons_df.index)
    return weapons_df


def main():
    update_needed, location = check_manifest_updates()
    if update_needed:
        manifest_version = open('manifest\\manifest_version.txt', "r+")
        manifest_version.seek(0)
        manifest_version.write(location.split('/')[-1][18:-8])
        retrieve_manifest(location)
    if not os.path.exists('manifest\\manifest.sqlite') or update_needed:
        extract_manifest()
    if not os.path.exists('manifest\\weapons_dataframe.csv') or update_needed:
        import dbclass
        db = dbclass.Database('manifest\\manifest.sqlite')
        inventory_df = create_dataframe(retrieve_table(db, "DestinyInventoryItemDefinition"))
        perk_df = \
            inventory_df[
                inventory_df['itemCategoryHashes'].apply(lambda x: 610365472 in x if type(x) is list else False)][
                ['hash', 'displayProperties.name']]
        perk_df.to_csv('manifest\\perk_dataframe.csv', index=True)
        damage_type_df = create_dataframe(retrieve_table(db, "DestinyDamageTypeDefinition"))[
            ['hash', 'displayProperties.name']]
        damage_type_df.to_csv('manifest\\damage_type_dataframe.csv', index=True)
        slot_df = create_dataframe(retrieve_table(db, "DestinyEquipmentSlotDefinition"))[
            ['hash', 'displayProperties.name']]
        slot_df.to_csv('manifest\\slot_dataframe.csv', index=True)
        plug_sets_df = create_dataframe(retrieve_table(db, "DestinyPlugSetDefinition"))[['hash', 'reusablePlugItems']]
        plug_sets_df.to_csv('manifest\\plug_sets_dataframe.csv', index=True)
        weapons_df = reduce_dataframe(inventory_df)
        weapons_df = select_needed_columns(weapons_df)
        weapons_df = refine_socket_entries(weapons_df)
        weapons_df = convert_hashes(weapons_df, perk_df, plug_sets_df, damage_type_df, slot_df)
        weapons_df.to_csv('manifest\\weapons_dataframe.csv', index=True)

    # weapons_df = pd.read_csv('manifest\\weapons_dataframe.csv', index_col=0)
    # perk_df = pd.read_csv('manifest\\perk_dataframe.csv', index_col=0)
    # plug_sets_df = pd.read_csv('manifest\\plug_sets_dataframe.csv', index_col=0)
    # slot_df = pd.read_csv('manifest\\slot_dataframe.csv', index_col=0)
    # damage_type_df = pd.read_csv('manifest\\damage_type_dataframe.csv', index_col=0)


if __name__ == '__main__':
    main()
