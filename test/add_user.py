#!/usr/bin/env python3
# script to add a user
# to the database

import requests
api_endpoint = "http://127.0.0.1:5000/user"

params = {
		'username' : "weed",
		'email' : "weed@gmail.com",
		'pseudo' : "great",
		'password' : "ccc"
	}

r = requests.post(url=api_endpoint, json=params)

print(r)
