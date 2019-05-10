#!/usr/bin/env python3
# script to add a user
# to the database

import requests
api_endpoint = "http://127.0.0.1:5000/user"

params = {
		'username' : "test",
		'email' : "matteyeux@gmail.com",
		'pseudo' : "tester",
		'pwd' : "this_is_a_test"
	}

r = requests.post(url=api_endpoint, data=params)

print(r)
