import os
import sys

import python.database as database
import python.dataframes.dataframes as dataframes
import python.lists_sets_dicts as data
import python.manifest.manifest as manifest


def main():
    os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    update_needed, location = manifest.check_manifest_updates()

    if update_needed:
        open('manifest/manifest_version.txt', "r+").write(location.split('/')[-1][18:-8])
        manifest.retrieve_manifest(location)
    if not os.path.exists('manifest/manifest.sqlite') or update_needed:
        manifest.extract_manifest()
    db = database.Database('manifest/manifest.sqlite')
    for name, columns in data.name_column_zip:
        if update_needed:
            dataframes.generate_pickle(db, name, columns)
    update_needed = True
    if update_needed:
        dataframes.generate_perk_pickle()
        dataframes.generate_weapons_pickle()
        database.create_image_archive()
        database.generate_sql_database()


if __name__ == '__main__':
    main()
