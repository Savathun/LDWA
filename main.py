def retrieve_manifest(manifest_location):
    """ """
    import urllib.request
    urllib.request.urlretrieve('https://www.bungie.net' + manifest_location, 'manifest\\manifest.zip')


def extract_manifest():
    from zipfile import ZipFile
    with ZipFile('manifest\\manifest.zip', 'r') as zipObj:
        zipObj.infolist()[0].filename = 'manifest.sqlite3'
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
    db = dbclass.Database('manifest\\manifest.sqlite3')


def main():
    """ """
    check_manifest_updates()
    connect_db()


if __name__ == '__main__':
    main()
