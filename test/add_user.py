#!/usr/bin/env python3
# script to add a user
# to the database
import random
import string
import requests

def random_str():
	letters = string.ascii_lowercase
	return ''.join(random.sample(letters, 8))

api_endpoint = "http://127.0.0.1:5000/user"

string_to_gen = random_str()
mail = string_to_gen + "@pornhub.com"
params = {
		'username' : string_to_gen,
		'email' : mail,
		'pseudo' : "great",
		'password' : "ccc"
	}

r = requests.post(url=api_endpoint, json=params)

print(r)
