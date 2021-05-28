def retrieve_manifest(manifest_location):
    """ """
    import urllib.request
    urllib.request.urlretrieve('https://www.bungie.net' + manifest_location, 'manifest\\manifest.zip')


def check_manifest_updates():
    import requests
    with open('api-key.txt', "r") as file:
        api_key = file.read()
    manifest_version = open('manifest_version.txt', "w+")
    HEADERS = {"X-API-Key": api_key}
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/", headers=HEADERS)
    manifest_location = r.json()['Response']['mobileWorldContentPaths']['en']
    if manifest_version.read() != manifest_location.split('/')[-1][18:-8]:
        manifest_version.write(manifest_location.split('/')[-1][18:-8])
        retrieve_manifest(manifest_location)

def main():
    """ """
    check_manifest_updates()

if __name__ == '__main__':
    main()
