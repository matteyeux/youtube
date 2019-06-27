from algoliasearch.search_client import SearchClient
import json
import configparser
import requests
import time

def send_data_to_algolia():
	ini = configparser.ConfigParser()
	ini.read('config.ini')
	app_id = ini['YOUTUBE']['app_id']
	admin_key = ini['YOUTUBE']['admin_key']

	client = SearchClient.create(app_id, admin_key)
	index = client.init_index('videos')

	URL = "http://127.0.0.1:5000/videos"
	r = requests.get(URL)

	data = r.json()

	# send data to algolia
	index.save_objects(data['data'], {'autoGenerateObjectIDIfNotExist': True})

if __name__ == '__main__':
	print('send_data_to_algolia')
	send_data_to_algolia()
	time.sleep(30)
