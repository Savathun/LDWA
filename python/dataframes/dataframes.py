import json
import python.lists_sets_dicts as data

import pandas
import requests


def generate_pickle(db, name, columns):
    table_list = [[entry[0], json.loads(entry[1])] for entry in db.fetch('Destiny' + name + 'Definition')]
    table_df = pandas.json_normalize([entry[1] for entry in table_list], sep='_')
    table_df.index = [entry[0] for entry in table_list]
    table_df[columns].to_pickle('dataframes/{}_dataframe.pkl'.format(name))


def generate_perk_pickle():
    inventory_df = pandas.read_pickle('dataframes/InventoryItem_dataframe.pkl')
    inventory_df[
        inventory_df['itemCategoryHashes'].apply(lambda x: 610365472 in x if type(x) is list else False)][
        ['hash', 'displayProperties_name', 'displayProperties_icon']].to_pickle('dataframes/perk_dataframe.pkl')


def generate_weapons_pickle():
    def reduce_inventory_to_weapons(inventory_df):
        def refine_socket_entries(inventory_df):
            inventory_df[['sockets_socketEntries_{}'.format(x) for x in
                          range(len(inventory_df.iloc[1]['sockets_socketEntries']))]] = pandas.DataFrame(
                inventory_df['sockets_socketEntries'].values.tolist(),
                index=inventory_df.index)
            inventory_df['sockets_socketEntries_0_singleInitialItemHash'] = pandas.DataFrame(
                inventory_df['sockets_socketEntries_0'].apply(lambda x: x['singleInitialItemHash']),
                index=inventory_df.index)
            inventory_df[
                ['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = pandas.DataFrame(
                inventory_df[['sockets_socketEntries_{}'.format(x) for x in range(1, 5)]].apply(
                    lambda x: x.apply(lambda y: y['randomizedPlugSetHash'] if 'randomizedPlugSetHash' in y else
                    y['reusablePlugSetHash'])),
                index=inventory_df.index)
            return inventory_df.drop(
                ['sockets_socketEntries'] + ['sockets_socketEntries_{}'.format(x) for x in range(0, 10)], axis=1)

        inventory_df = inventory_df[(inventory_df['itemType'] == 3) &
                                    (inventory_df['inventory_tierTypeName'] == 'Legendary')].explode('quality_versions')
        inventory_df = pandas.concat([inventory_df.drop(['quality_versions'], axis=1),
                                      inventory_df['quality_versions'].apply(pandas.Series)], axis=1)
        return refine_socket_entries(
            inventory_df[inventory_df['powerCapHash'] == 2759499571].drop_duplicates(subset=['displayProperties_name'])[
                ['itemTypeDisplayName', 'displayProperties_name', 'displayProperties_icon', 'screenshot',
                 'defaultDamageTypeHash',
                 'equippingBlock_equipmentSlotTypeHash', 'equippingBlock_ammoType', 'sockets_socketEntries']])

    def generate_weapon_synergy_column(weapons_df):
        weapons_df['Synergy'] = weapons_df.apply(
            lambda row: {(perk_1, perk_2)
                         for combo in data.synergistic_combos
                         for cat in combo
                         for perk_1 in row.perk_column_3 if perk_1 in data.categories[cat]
                         for perk_2 in row.perk_column_4
                         for cat_2 in ([x for x in list(combo) if x != cat] if len(combo) > 1
                                       else [cat]) if perk_2 in data.categories[cat_2]}, axis=1)
        weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']] = pandas.DataFrame(
            weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']].apply(
                lambda x: x.apply(lambda y: str(str(y).strip('[]{}')))), index=weapons_df.index)
        return weapons_df

    inventory_df = pandas.read_pickle('dataframes/InventoryItem_dataframe.pkl')
    perk_df = pandas.read_pickle('dataframes/perk_dataframe.pkl')
    plug_sets_df = pandas.read_pickle('dataframes/PlugSet_dataframe.pkl')
    damage_type_df = pandas.read_pickle('dataframes/DamageType_dataframe.pkl')
    slot_df = pandas.read_pickle('dataframes/EquipmentSlot_dataframe.pkl')
    presentation_node_df = pandas.read_pickle('dataframes/PresentationNode_dataframe.pkl')
    ammo_type_list = [item['identifier'] for item in
                      requests.get("https://github.com/Bungie-net/api/raw/master/openapi.json").json()[
                          'components']['schemas']['Destiny.DestinyAmmunitionType']['x-enum-values']]
    weapons_df = reduce_inventory_to_weapons(inventory_df)
    weapons_df['defaultDamageTypeHashIcon'] = pandas.DataFrame(
        weapons_df['defaultDamageTypeHash'].apply(
            lambda x: damage_type_df.loc[damage_type_df['hash'] == x]['displayProperties_icon'].values[0]),
        index=weapons_df.index)
    weapons_df['defaultDamageTypeHash'] = pandas.DataFrame(
        weapons_df['defaultDamageTypeHash'].apply(
            lambda x: damage_type_df.loc[damage_type_df['hash'] == x]['displayProperties_name'].values[0]),
        index=weapons_df.index)

    weapons_df['equippingBlock_equipmentSlotTypeHash'] = pandas.DataFrame(
        weapons_df['equippingBlock_equipmentSlotTypeHash'].apply(
            lambda x: slot_df.loc[slot_df['hash'] == x]['displayProperties_name'].values[0].split(' ')[0]),
        index=weapons_df.index)
    weapons_df['equippingBlock_ammoTypeIcon'] = pandas.DataFrame(
        weapons_df['equippingBlock_ammoType'].apply(
            lambda x:
            presentation_node_df.loc[presentation_node_df['displayProperties_name'] == ammo_type_list[int(x)]][
                'displayProperties_icon'].values[0],
            lambda x: ammo_type_list[int(x)]),
        index=weapons_df.index)
    weapons_df['equippingBlock_ammoType'] = pandas.DataFrame(
        weapons_df['equippingBlock_ammoType'].apply(
            lambda x: ammo_type_list[int(x)]),
        index=weapons_df.index)
    weapons_df['sockets_socketEntries_0_singleInitialItemHash'] = pandas.DataFrame(
        weapons_df['sockets_socketEntries_0_singleInitialItemHash'].apply(
            lambda x: perk_df.loc[perk_df['hash'] == x]['displayProperties_name'].values[0]),
        index=weapons_df.index)
    weapons_df[['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]] = pandas.DataFrame(
        weapons_df[['sockets_socketEntries_{}_randomizedPlugSetHash'.format(x) for x in range(1, 5)]].apply(
            lambda x: x.apply(
                lambda y: set([
                    perk_df.loc[perk_df['hash'] == z['plugItemHash']]['displayProperties_name'].values[0] for z
                    in plug_sets_df.loc[plug_sets_df['hash'] == y]['reusablePlugItems'].values[0] if
                    z['currentlyCanRoll']]))),
        index=weapons_df.index)
    weapons_df.columns = data.renamed_weapons_df_columns
    weapons_df = weapons_df[data.reordered_weapons_df_columns]
    weapons_df['Synergy'] = weapons_df.apply(
        lambda row: {(perk_1, perk_2)
                     for combo in data.synergistic_combos
                     for cat in combo
                     for perk_1 in row.perk_column_3 if perk_1 in data.categories[cat]
                     for perk_2 in row.perk_column_4
                     for cat_2 in ([x for x in list(combo) if x != cat] if len(combo) > 1
                                   else [cat]) if perk_2 in data.categories[cat_2]}, axis=1)
    weapons_df.to_pickle('dataframes/weapons_dataframe.pkl')
