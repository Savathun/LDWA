
name_column_zip = zip(['InventoryItem', 'DamageType', 'EquipmentSlot', 'PlugSet', 'PresentationNode'],
                             [['hash', 'itemCategoryHashes', 'itemTypeDisplayName', 'displayProperties_name',
                               'displayProperties_icon', 'screenshot',
                               'quality_versions', 'equippingBlock_equipmentSlotTypeHash', 'inventory_tierTypeName',
                               'itemType', 'equippingBlock_ammoType', 'sockets_socketEntries', 'defaultDamageTypeHash'],
                              ['hash', 'displayProperties_name', 'displayProperties_icon'],
                              ['hash', 'displayProperties_name'],
                              ['hash', 'reusablePlugItems'],
                              ['hash', 'displayProperties_name', 'displayProperties_icon']])

renamed_weapons_df_columns = ['Type', 'Name', 'Icon', 'Screenshot', 'Element', 'Slot', 'Ammo', 'Archetype',
                              'perk_column_1', 'perk_column_2', 'perk_column_3', 'perk_column_4', 'ElementIcon', 'AmmoIcon']
reordered_weapons_df_columns = ['Name', 'Type', 'Archetype', 'Icon', 'Screenshot', 'Slot', 'Element', 'ElementIcon',
                                'Ammo', 'AmmoIcon', 'perk_column_1', 'perk_column_2', 'perk_column_3', 'perk_column_4']
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


def generate_set_of_available_traits(weapons_df):
    import numpy as np
    perks = np.append(weapons_df['perk_column_1'].explode().unique(),
                      weapons_df['perk_column_2'].explode().unique())
    perks = np.append(perks, weapons_df['perk_column_3'].explode().unique())
    perks = np.append(perks, weapons_df['perk_column_4'].explode().unique())
    return sorted(set(perks))


# Rest of file is currently unused but may find use at a later date
# ==================================================================================================================
categorized_effects = {
    'increase_damage': {
        'increase_weapon_damage': {
            'increase_weapon_damage': ['Swashbuckler', 'Adrenaline Junkie', "Assassin's Blade", 'Counterattack',
                                       'Cluster Bomb', 'Surrounded', 'High-Impact Reserves', 'Frenzy', 'Rampage',
                                       'Reservoir Burst', 'Recombination', 'One for All',
                                       'Whirlwind Blade', 'Trench Barrel', 'Timed Payload', 'Multikill Clip',
                                       'En Garde', 'Explosive Payload', 'Explosive Head', 'Full Court',
                                       'Shattering Blade', 'Kill Clip', 'Lasting Impression', 'Kickstart', ],
            'increase_weapon_damage_against_powerful_red_and_orange_bar': ['Redirection'],
            'increase_weapon_damage_against_yellow_bar': ['Vorpal Weapon', 'Redirection', ],
            'increase_weapon_precision_damage': ['Box Breathing', 'Firing Line', 'Headseeker', ],
        },
        'increase_melee_damage': ['One-Two Punch', ],
    },
    'increase_stat': {
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
                                  'Rapid Hit', 'Sneak Bow', 'Impulse Amplifier', 'Underdog', ],
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
    },
    'reduce_negative_stat': {
        'reduce_screen_shake': ['Zen Moment', ],
        'reduce_vertical_recoil': ['Elemental Capacitor', 'Heating Up', ],
        'reduce_flinch': ['No Distractions', 'Celerity', ],
        'reduce_bow_draw_time': ['Cornered', "Archer's Tempo", ],
        'reduce_fusion_charge_time': ['Cornered', 'Backup Plan', 'Kickstart', ],
    },
    'reduce_positive_stat': {
        'reduce_range': ['Iron Gaze'],
        'reduce_stability': ['Iron Reach'],
        'reduce_reload_speed': ['Iron Grip'],
    },
    'regen': {
        'regen_energy': {
            'regen_class_energy': ['Energy Transfer', 'Wellspring', ],
            'regen_grenade_energy': ['Demolitionist', 'Wellspring', ],
            'regen_super_energy': ['Thresh', ],
            'regen_melee_energy': ['Wellspring', ],
        },
        'regen_health': ['Unrelenting'],
        'regen_ammo': ['Mulligan', "Fourth Time's the Charm", 'Triple Tap', 'Tireless Blade', 'Relentless Strikes', ],
    },
    'inflict_debuff': {
        'inflict_damage_debuff': {
            'inflict_damage_debuff': ['Flash Counter', ],
            'inflict_kinetic_damage_debuff': ['Disruption Break', ],
        },
        'inflict_disorient_debuff': ['Shield Disorient', 'Flash Counter', ],
    },
    'track_targets': ['Tracking Module'],
    'create_aoe_damage_instance': ['Firefly', 'Dragonfly', 'Cluster Bomb', 'Timed Payload',
                                   'Chain Reaction', 'Reservoir Burst', 'Explosive Payload', 'Explosive Head', ],
    'reload_weapon': ['Demolitionist', 'Auto-Loading Holster', 'Reconstruction', 'Grave Robber', 'Slideshot',
                      'Slideways', 'Rewind Rounds', 'Subsistence', 'Bottomless Grief', 'Overflow', 'Pulse Monitor', ],
    'reload_stowed_weapons': ['Sympathetic Arsenal', ],
    'make_weapon_full_auto': ['Full Auto Trigger System', ],
    'gain_special_ammo': ['Lead from Gold', ],
    'prevent_radar_pings_from_shooting': ['Sneak Bow'],
    'change_weapon_element': ['Osmosis', ],

}
categorized_triggers = {
    'passive': ['Celerity', 'Bottomless Grief', 'Cluster Bomb', 'Explosive Head', 'Explosive Payload',
                'Lasting Impression', 'Timed Payload', 'Dual Loader', 'Elemental Capacitor', 'Backup Plan',
                'Full Auto Trigger System', 'Hip-Fire Grip', 'Impulse Amplifier', 'Rangefinder',
                'Iron Gaze', 'Iron Grip', 'Iron Reach', 'Reconstruction', 'Snapshot Sights', 'Vorpal Weapon', ],
    # passive is defined as something that is either a flat boost with no action required to activate it, or a buff that
    # buffs the action required to activate it, i.e. dual loader buffs reload speed, and also is activated by reloading
    'on_kill': {
        'on_kill_with_melee': ['Swashbuckler', 'Grave Robber', ],
        'on_kill_with_grenade': ['Adrenaline Junkie', ],
        'on_kill_with_weapon': {
            'on_kill_with_weapon': ["Assassin's Blade", 'Chain Reaction', 'Thresh', 'Wellspring', 'Reservoir Burst',
                                    'Killing Wind', 'Swashbuckler',
                                    'Demolitionist', 'Feeding Frenzy', 'Heating Up', 'Subsistence', 'Rampage', ],
            'on_kill_with_elemental_weapon': ['Recombination'],
            'on_precision_kill_with_weapon': ['Firefly', 'Dragonfly', 'Outlaw', ],
            'on_every_other_kill_with_weapon': ['Tireless Blade'],
            'on_kill_with_weapon_when_last_alive': ['Bottomless Grief', ],
            'on_major_kill_or_multikills_with_weapon': ['Unrelenting', ],
        },
    },
    'on_shield_break': {
        'on_shield_break': ['Disruption Break', 'Genesis'],
        'on_shield_break_when_energy_matched': ['Shield Disorient'],
    },
    'on_slide': {
        'on_slide': ['Slideshot', 'Slideways', 'Kickstart', ],
        'on_slide_after_sprint_for_time': ['Kickstart', ],
    },
    'on_block_any_attack': {
        'on_block_any_attack': ['Energy Transfer'],
        'on_block_any_attack_right_after_guarding': {
            'on_block_any_attack_right_after_guarding': ['Counterattack', ],
            'on_block_melee_attack_right_after_guarding': ['Flash Counter', ],
        },
    },
    'on_reload': {
        'on_reload': ['Clown Cartridge'],
        'on_reload_after_kill': {
            'on_reload_after_kill': ['Ambitious Assassin', 'Tunnel Vision', 'Multikill Clip', 'Kill Clip',
                                     'Sympathetic Arsenal', ],
            'on_reload_after_precision_kill': ['Desperado', ],
        }
    },
    'while_ads': {
        'while_ads': ['Rangefinder', 'Tracking Module'],
        'while_moving_while_ads': ['Moving Target', ],
    },
    'on_ammo_pickup': {
        'on_special_ammo_pickup': ['Overflow'],
        'on_heavy_ammo_pickup': ['Lead from Gold', 'Overflow'],
    },
    'on_hit': {
        'on_hit_with_weapon': {
            'on_hit_with_weapon': ['Whirlwind Blade', 'Zen Moment', ],
            'on_weak_enemy_hit_with_weapon': ['Redirection'],
            'on_hit_to_body_with_weapon': ['Headseeker', ],
            'on_hit_to_head_with_weapon': {
                'on_hit_to_head_with_weapon': ["Archer's Tempo", 'Rapid Hit', ],
                'on_multiple_hits_to_head_with_weapon': ["Fourth Time's the Charm", 'Triple Tap', ],
            },
            'on_matched_energy_shield_hit': ['Genesis'],
            'on_three_consecutive_light_hits': ['Relentless Strikes'],
            'on_hitting_all_pellets': ['One-Two Punch', ],
            'on_empty_mag_after_multiple_hits': ['Rewind Rounds'],
        },
        'on_melee_hit': ['Trench Barrel', ],
    },

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

effects = {
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
                              'Rapid Hit', 'Sneak Bow', 'Impulse Amplifier', 'Underdog', ],
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
    'regen_ammo': ['Mulligan', "Fourth Time's the Charm", 'Triple Tap', 'Tireless Blade', 'Relentless Strikes', ],

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
                                   'Chain Reaction', 'Reservoir Burst', 'Explosive Payload', 'Explosive Head', ],
    'reload_weapon': ['Demolitionist', 'Auto-Loading Holster', 'Reconstruction', 'Grave Robber', 'Slideshot',
                      'Slideways', 'Rewind Rounds', 'Subsistence', 'Bottomless Grief', 'Overflow', 'Pulse Monitor', ],
    'reload_stowed_weapons': ['Sympathetic Arsenal', ],
    'make_weapon_full_auto': ['Full Auto Trigger System', ],
    'gain_special_ammo': ['Lead from Gold', ],
    'prevent_radar_pings_from_shooting': ['Sneak Bow'],
    'change_weapon_element': ['Osmosis', ],

}
triggers = {
    'passive': ['Celerity', 'Bottomless Grief', 'Cluster Bomb', 'Explosive Head', 'Explosive Payload',
                'Lasting Impression', 'Timed Payload', 'Dual Loader', 'Elemental Capacitor', 'Backup Plan',
                'Full Auto Trigger System', 'Hip-Fire Grip', 'Impulse Amplifier', 'Rangefinder',
                'Iron Gaze', 'Iron Grip', 'Iron Reach', 'Reconstruction', 'Snapshot Sights', 'Vorpal Weapon', ],
    # passive is defined as something that is either a flat boost with no action required to activate it, or a buff that
    # buffs the action required to activate it, i.e. dual loader buffs reload speed, and also is activated by reloading

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
                             'Sympathetic Arsenal', ],
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


def generate_perks_dict():
    import numpy
    import pandas

    weapons_df = pandas.read_pickle('dataframes/weapons_dataframe.pkl')
    weapon_traits = sorted(set(
        numpy.append(weapons_df['perk_column_4'].explode().unique(), weapons_df['perk_column_3'].explode().unique())))
    perks = dict.fromkeys(weapon_traits)
    for key in triggers.keys():
        for perk in triggers[key]:
            if perks[perk] is None:
                perks[perk] = {'triggers': [key], 'effects': []}
            else:
                perks[perk]['triggers'].append(key)
    for key in effects.keys():
        for perk in effects[key]:
            perks[perk]['effects'].append(key)
