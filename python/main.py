import sqlite3
import sys
import time
import pandas
import zipfile
import json
import urllib.request
import urllib.error
import requests
import os
import sqlalchemy


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def fetch(self, table):
        self.cur.execute("SELECT * FROM " + table)
        return self.cur.fetchall()


def retrieve_manifest(manifest_location):
    """ """
    urllib.request.urlretrieve('https://www.bungie.net' + manifest_location, 'manifest/manifest.zip')


def extract_manifest():
    with zipfile.ZipFile('manifest/manifest.zip', 'r') as zipObj:
        zipObj.infolist()[0].filename = 'manifest.sqlite'
        zipObj.extract(zipObj.infolist()[0], path='manifest')


def check_manifest_updates():
    manifest_location = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/",
                                     headers={"X-API-Key": open('api_key.txt', "r").read()}).json()['Response'][
        'mobileWorldContentPaths']['en']
    return (True, manifest_location) if open('manifest/manifest_version.txt',
                                             "r+").read() != manifest_location.split('/')[-1][18:-8] else (False, 0)


def generate_pickle(db, name, columns):
    table_list = [[entry[0], json.loads(entry[1])] for entry in db.fetch('Destiny' + name + 'Definition')]
    table_df = pandas.json_normalize([entry[1] for entry in table_list], sep='_')
    table_df.index = [entry[0] for entry in table_list]
    table_df[columns].to_pickle('dataframes/{}_dataframe.pkl'.format(name))


def generate_weapons_dataframe(inventory_df, perk_df, plug_sets_df, damage_type_df, slot_df, presentation_node_df):
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
    weapons_df.columns = ['Type', 'Name', 'Icon', 'Screenshot', 'Element', 'Slot', 'Ammo', 'Archetype',
                          'perk_column_1', 'perk_column_2', 'perk_column_3', 'perk_column_4', 'ElementIcon', 'AmmoIcon']
    return weapons_df[['Name', 'Type', 'Archetype', 'Icon', 'Screenshot', 'Slot', 'Element', 'ElementIcon', 'Ammo',
                       'AmmoIcon', 'perk_column_1', 'perk_column_2', 'perk_column_3', 'perk_column_4']]


def create_image_archive(weapons_df, perk_df):
    import numpy as np

    def generate_set_of_available_traits(weapons_df):
        perks = np.append(weapons_df['perk_column_1'].explode().unique(),
                          weapons_df['perk_column_2'].explode().unique())
        perks = np.append(perks, weapons_df['perk_column_3'].explode().unique())
        perks = np.append(perks, weapons_df['perk_column_4'].explode().unique())
        return sorted(set(perks))

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

    for col in ['Icon', 'Screenshot', 'AmmoIcon', 'ElementIcon']:
        for path in weapons_df[col].values.tolist():
            if col == 'Screenshot':
                download_image(path, '../android/app/src/main/res/drawable/')
            else:
                download_image(path, '../android/app/src/main/res/mipmap-xxhdpi/')
    perk_set = generate_set_of_available_traits(weapons_df)
    for perk in perk_set:
        path = perk_df.loc[perk_df['displayProperties_name'] == perk]['displayProperties_icon'].values[0]
        download_image(path, '../android/app/src/main/res/mipmap-xxhdpi/')


def main():
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    update_needed, location = check_manifest_updates()

    if update_needed:
        open('manifest/manifest_version.txt', "r+").write(location.split('/')[-1][18:-8])
        retrieve_manifest(location)
    if not os.path.exists('manifest/manifest.sqlite') or update_needed:
        extract_manifest()
    db = Database('manifest/manifest.sqlite')
    for name, columns in zip(['InventoryItem', 'DamageType', 'EquipmentSlot', 'PlugSet', 'PresentationNode'],
                             [['hash', 'itemCategoryHashes', 'itemTypeDisplayName', 'displayProperties_name',
                               'displayProperties_icon', 'screenshot',
                               'quality_versions', 'equippingBlock_equipmentSlotTypeHash', 'inventory_tierTypeName',
                               'itemType', 'equippingBlock_ammoType', 'sockets_socketEntries', 'defaultDamageTypeHash'],
                              ['hash', 'displayProperties_name', 'displayProperties_icon'],
                              ['hash', 'displayProperties_name'],
                              ['hash', 'reusablePlugItems'],
                              ['hash', 'displayProperties_name', 'displayProperties_icon']]):
        if update_needed:
            generate_pickle(db, name, columns)
    if update_needed:
        inventory_df = pandas.read_pickle('dataframes/InventoryItem_dataframe.pkl')
        if update_needed:
            inventory_df[
                inventory_df['itemCategoryHashes'].apply(lambda x: 610365472 in x if type(x) is list else False)][
                ['hash', 'displayProperties_name', 'displayProperties_icon']].to_pickle(
                'dataframes/perk_dataframe.pkl')
        if update_needed:
            generate_weapons_dataframe(inventory_df,
                                       pandas.read_pickle('dataframes/perk_dataframe.pkl'),
                                       pandas.read_pickle('dataframes/PlugSet_dataframe.pkl'),
                                       pandas.read_pickle('dataframes/DamageType_dataframe.pkl'),
                                       pandas.read_pickle('dataframes/EquipmentSlot_dataframe.pkl'),
                                       pandas.read_pickle('dataframes/PresentationNode_dataframe.pkl')
                                       ).to_pickle('dataframes/weapons_dataframe.pkl')
    if update_needed:
        weapons_df = pandas.read_pickle('dataframes/weapons_dataframe.pkl')
        create_image_archive(pandas.read_pickle('dataframes/weapons_dataframe.pkl'),
                             pandas.read_pickle('dataframes/perk_dataframe.pkl'))
        categories = {
            'increase_weapon_damage': ['Swashbuckler', 'Adrenaline Junkie', "Assassin's Blade", 'Counterattack',
                                       'One for All',
                                       'Cluster Bomb', 'Surrounded', 'High-Impact Reserves', 'Frenzy', 'Rampage',
                                       'Reservoir Burst',
                                       'Whirlwind Blade', 'Trench Barrel', 'Timed Payload', 'Multikill Clip',
                                       'Recombination',
                                       'En Garde', 'Explosive Payload', 'Explosive Head', 'Full Court',
                                       'Shattering Blade', 'Kill Clip', 'Lasting Impression', 'Kickstart', ],
            'increase_weapon_damage_against_powerful_red_and_orange_bar': ['Redirection'],
            'increase_weapon_damage_against_yellow_bar': ['Vorpal Weapon', 'Redirection', ],
            'increase_weapon_precision_damage': ['Box Breathing', 'Firing Line', 'Headseeker', ],
            'increase_melee_damage': ['One-Two Punch', ],
            'increase_handling': ['Elemental Capacitor', 'Celerity', 'Eye of the Storm', 'Backup Plan', 'Surplus',
                                  'Killing Wind', 'Threat Detector', 'Frenzy',
                                  'Firmly Planted', 'Slideways', 'Pulse Monitor', 'Quickdraw'],
            'increase_accuracy': ['Dynamic Sway Reduction', 'Eye of the Storm', 'Opening Shot', 'Under Pressure',
                                  'Hip-Fire Grip', 'Heating Up', 'Firmly Planted', 'Tap the Trigger', ],
            'increase_stability': ['Dynamic Sway Reduction', 'Elemental Capacitor', 'Under Pressure', 'Surplus',
                                   'Hip-Fire Grip', 'Heating Up', 'Rapid Hit', 'Threat Detector',
                                   'Iron Grip', 'Firmly Planted', 'Slideshot', 'Slideways', 'Tap the Trigger', ],
            'increase_range': ['Slideshot', 'Opening Shot', 'Iron Reach', 'Killing Wind', 'Box Breathing', ],
            'increase_rpm': ['Desperado', ],
            'increase_mag_size': ['Ambitious Assassin', 'Bottomless Grief', 'Clown Cartridge', 'Overflow',
                                  'Reconstruction', ],
            'increase_reload_speed': ['Celerity', 'Dual Loader', 'Elemental Capacitor', 'Feeding Frenzy',
                                      'Surplus', 'Threat Detector', 'Firefly', 'Frenzy', 'Outlaw',
                                      'Rapid Hit', 'Sneak Bow', 'Impulse Amplifier',
                                      # 'Underdog',
                                      ],
            'increase_reserves': ['Field Prep', ],
            'increase_stow_speed': ['Field Prep', ],
            'increase_draw_speed': ['Field Prep', 'Quickdraw'],
            'increase_mobility': ['Killing Wind', ],
            'increase_speed': ["Assassin's Blade", ],
            'increase_precision_hit_targeting_while_hip_firing': ['Hip-Fire Grip'],
            'increase_movement_while_ads_speed': ['Elemental Capacitor', 'Moving Target', ],
            'increase_zoom': ['Rangefinder', ],
            'increase_velocity': ['Rangefinder', 'Impulse Amplifier', ],
            'increase_blast_radius': ['Danger Zone', ],
            'increase_ads_speed': ['Tunnel Vision', 'Snapshot Sights'],
            'increase_target_acquisition': ['Iron Gaze', 'Moving Target', 'Celerity', 'Tunnel Vision', ],
            'increase_bow_hold_time': ['Sneak Bow'],

            'regen_class_energy': ['Energy Transfer', 'Wellspring', ],
            'regen_grenade_energy': ['Demolitionist', 'Wellspring', ],
            'regen_super_energy': ['Thresh', ],
            'regen_melee_energy': ['Wellspring', ],

            'regen_health': ['Unrelenting'],
            'regen_ammo': ['Mulligan', "Fourth Time's the Charm", 'Triple Tap', 'Tireless Blade', 'Relentless Strikes'],

            'inflict_damage_debuff': ['Flash Counter', ],
            'inflict_kinetic_damage_debuff': ['Disruption Break', ],
            'inflict_disorient_debuff': ['Shield Disorient', 'Flash Counter', ],

            'reduce_screen_shake': ['Zen Moment', ],
            'reduce_vertical_recoil': ['Elemental Capacitor', 'Heating Up', ],
            'reduce_flinch': ['No Distractions', 'Celerity', ],
            'reduce_bow_draw_time': ['Cornered', "Archer's Tempo", ],
            'reduce_fusion_charge_time': ['Cornered', 'Backup Plan', 'Kickstart', ],

            'reduce_range': ['Iron Gaze'],
            'reduce_stability': ['Iron Reach'],
            'reduce_reload_speed': ['Iron Grip'],

            'track_targets': ['Tracking Module'],
            'create_aoe_damage_instance': ['Firefly', 'Dragonfly', 'Cluster Bomb', 'Timed Payload',
                                           'Chain Reaction', 'Reservoir Burst', 'Explosive Payload', 'Explosive Head'],
            'reload_weapon': ['Demolitionist', 'Auto-Loading Holster', 'Reconstruction', 'Grave Robber', 'Slideshot',
                              'Slideways', 'Rewind Rounds', 'Subsistence', 'Bottomless Grief', 'Overflow',
                              'Pulse Monitor', ],
            'reload_stowed_weapons': ['Sympathetic Arsenal', ],
            'make_weapon_full_auto': ['Full Auto Trigger System', ],
            'gain_special_ammo': ['Lead from Gold', ],
            'prevent_radar_pings_from_shooting': ['Sneak Bow'],
            'change_weapon_element': ['Osmosis', ],
            'passive': ['Celerity', 'Bottomless Grief', 'Cluster Bomb', 'Explosive Head', 'Explosive Payload',
                        'Lasting Impression', 'Timed Payload', 'Dual Loader', 'Elemental Capacitor', 'Backup Plan',
                        'Full Auto Trigger System', 'Hip-Fire Grip', 'Impulse Amplifier', 'Rangefinder',
                        'Iron Gaze', 'Iron Grip', 'Iron Reach', 'Reconstruction', 'Snapshot Sights', 'Vorpal Weapon', ],
            # passive is defined as something that is either a flat boost with no action required to activate it,
            # or a buff that buffs the action required to activate it,
            # i.e. dual loader buffs reload speed, and also is activated by reloading.

            'on_kill_with_melee': ['Swashbuckler', 'Grave Robber', ],
            'on_kill_with_grenade': ['Adrenaline Junkie', ],

            'on_kill_with_weapon': ["Assassin's Blade", 'Chain Reaction', 'Thresh', 'Wellspring', 'Reservoir Burst',
                                    'Killing Wind', 'Swashbuckler',
                                    'Demolitionist', 'Feeding Frenzy', 'Heating Up', 'Subsistence', 'Rampage', ],
            'on_kill_with_elemental_weapon': ['Recombination'],
            'on_precision_kill_with_weapon': ['Firefly', 'Dragonfly', 'Outlaw', ],
            'on_every_other_kill_with_weapon': ['Tireless Blade'],
            'on_kill_with_weapon_when_last_alive': ['Bottomless Grief', ],
            'on_major_kill_or_multikills_with_weapon': ['Unrelenting', ],

            'on_shield_break': ['Disruption Break', 'Genesis'],
            'on_shield_break_when_energy_matched': ['Shield Disorient'],

            'on_slide': ['Slideshot', 'Slideways', 'Kickstart', ],
            'on_slide_after_sprint_for_time': ['Kickstart', ],

            'on_block_any_attack': ['Energy Transfer'],
            'on_block_any_attack_right_after_guarding': ['Counterattack', ],
            'on_block_melee_attack_right_after_guarding': ['Flash Counter', ],

            'on_reload': ['Clown Cartridge'],
            'on_reload_after_kill': ['Ambitious Assassin', 'Tunnel Vision', 'Multikill Clip', 'Kill Clip',
                                     # 'Sympathetic Arsenal',
                                     ],
            'on_reload_after_precision_kill': ['Desperado', ],

            'while_ads': ['Rangefinder', 'Tracking Module'],
            'while_moving_while_ads': ['Moving Target', ],

            'on_special_ammo_pickup': ['Overflow'],
            'on_heavy_ammo_pickup': ['Lead from Gold', 'Overflow'],

            'on_hit_with_weapon': ['Whirlwind Blade', 'Zen Moment', ],
            'on_weak_enemy_hit_with_weapon': ['Redirection'],
            'on_hit_to_body_with_weapon': ['Headseeker', ],

            'on_hit_to_head_with_weapon': ["Archer's Tempo", 'Rapid Hit', ],
            'on_multiple_hits_to_head_with_weapon': ["Fourth Time's the Charm", 'Triple Tap', ],

            'on_matched_energy_shield_hit': ['Genesis'],
            'on_three_consecutive_light_hits': ['Relentless Strikes'],
            'on_hitting_all_pellets': ['One-Two Punch', ],
            'on_empty_mag_after_multiple_hits': ['Rewind Rounds'],

            'on_melee_hit': ['Trench Barrel', ],
            'while_full_mag': ['Reservoir Burst'],
            'while_crouched': ['Firmly Planted', 'Field Prep', 'Sneak Bow', ],
            'while_low_health': ['Eye of the Storm', 'Underdog', 'Pulse Monitor', ],
            'while_near_multiple_allies': ['Firing Line'],
            'while_charged_abilities': ['Surplus'],
            'while_surrounded_by_enemies': ['Surrounded', 'Cornered', 'Threat Detector', 'Danger Zone', ],
            'on_last_alive': ['Celerity', ],
            'on_being_in_combat_for_some_time': ['Frenzy', ],
            'on_low_mag': ['High-Impact Reserves', 'Under Pressure', ],
            'on_heavy_on_last_ammo': ['Shattering Blade'],
            'on_draw': ['En Garde', 'Backup Plan', 'Quickdraw'],
            'on_stow_after_timer': ['Auto-Loading Holster', ],
            'on_initial_trigger_pull': ['Tap the Trigger'],
            'on_ads_after_timer': ['No Distractions', 'Box Breathing', ],
            'on_first_shot_after_timer': ['Opening Shot'],
            'on_missing_shot': ['Mulligan'],
            'on_longer_projectile_travel_distance': ['Full Court'],
            'on_damage_on_three_targets': ['One for All'],
            'on_sustained_fire': ['Dynamic Sway Reduction', ],
            'on_grenade_usage': ['Osmosis', 'Demolitionist'],

        }
        synergistic_combos = [
            {'increase_weapon_damage'}, {'on_reload_after_kill'}, {'on_slide'}, {'on_kill_with_weapon'},
            {'increase_reload_speed', 'on_reload_after_kill'}, {'while_surrounded_by_enemies'},
            {'on_shield_break'},
            {'inflict_damage_debuff', 'inflict_kinetic_damage_debuff', 'increase_weapon_damage',
             'inflict_disorient_debuff'},
            {'regen_class_energy', 'regen_melee_energy', 'regen_grenade_energy', 'regen_super_energy'},
            {'on_low_mag'},
            {'on_kill_with_grenade', 'regen_grenade_energy', },
            {'on_reload_after_precision_kill', 'increase_reload_speed'},
            {'on_kill_with_melee', 'regen_melee_energy', 'on_melee_hit', 'increase_melee_damage'},
        ]

        weapons_df['Synergy'] = weapons_df.apply(
            lambda row: {(perk_1, perk_2)
                         for combo in synergistic_combos
                         for cat in combo
                         for perk_1 in row.perk_column_3 if perk_1 in categories[cat]
                         for perk_2 in row.perk_column_4
                         for cat_2 in ([x for x in list(combo) if x != cat] if len(combo) > 1
                                       else [cat]) if perk_2 in categories[cat_2]}, axis=1)
        weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']] = pandas.DataFrame(
            weapons_df[['perk_column_{}'.format(x + 1) for x in range(4)] + ['Synergy']].apply(
                lambda x: x.apply(lambda y: str(str(y).strip('[]{}')))), index=weapons_df.index)
        engine = sqlalchemy.create_engine('sqlite:///../android/app/src/main/assets/weapons_database.sqlite',
                                          echo=False)
        weapons_df.to_sql('weapons', con=engine, if_exists="replace")
        pandas.read_pickle('dataframes/perk_dataframe.pkl').to_sql('perks', con=engine, if_exists="replace")
        pandas.DataFrame.from_dict({'locale': ['en-US']}).to_sql('android_metadata', con=engine, if_exists="replace")


if __name__ == '__main__':
    main()
