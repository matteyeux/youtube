from algoliasearch.search_client import SearchClient
import json
import configparser
import requests

ini = configparser.ConfigParser()
ini.read('config.ini')
app_id = ini['YOUTUBE']['app_id']
admin_key = ini['YOUTUBE']['admin_key']

client = SearchClient.create(app_id, admin_key)
index = client.init_index('videos')

URL = "http://127.0.0.1:5000/videos"
r = requests.get(URL)

data = r.json()
print(data['data'])

# send data to algolia
index.save_objects(data['data'], {'autoGenerateObjectIDIfNotExist': True})

# # Search for a first name
# print(json.dumps(index.search('matteyeux'), indent=4))
# Search for a first name with typo
#print(index.search('jimie'))
## Search for a company
#print(index.search('Alex'))
## Search for a first name and a company
#print(index.search('jimmie paint'))


