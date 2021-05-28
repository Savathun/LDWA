def main():
    """ """
    import requests
    import urllib.request
    import pprint
    # dictionary to hold extra headers
    with open('api-key.txt', "r") as file:
        api_key = file.read()
    HEADERS = {"X-API-Key": api_key}
    r = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/", headers=HEADERS)
    manifest_location = r.json()['Response']['mobileWorldContentPaths']['en']
    manifest_url = 'https://www.bungie.net' + manifest_location
    urllib.request.urlretrieve(manifest_url, manifest_location.split('/')[-1] + '.zip')
if __name__ == '__main__':
    main()
