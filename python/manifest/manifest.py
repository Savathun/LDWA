import urllib.request
import zipfile

import requests


def retrieve_manifest(manifest_location):
    """ """
    urllib.request.urlretrieve('https://www.bungie.net' + manifest_location, 'manifest/manifest.zip')


def extract_manifest():
    with zipfile.ZipFile('manifest/manifest.zip', 'r') as zipObj:
        zipObj.infolist()[0].filename = 'manifest.sqlite'
        zipObj.extract(zipObj.infolist()[0], path='manifest')


def check_manifest_updates():
    headers = {"X-API-Key": open('api_key.txt', "r").read()}
    response = requests.get("https://www.bungie.net/platform/Destiny2/Manifest/", headers=headers)
    manifest_location = response.json()['Response']['mobileWorldContentPaths']['en']
    if open('manifest/manifest_version.txt', "r+").read() != manifest_location.split('/')[-1][18:-8]:
        return True, manifest_location
    else:
        return False, manifest_location

