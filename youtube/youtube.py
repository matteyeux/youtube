#!/usr/bin/env python3

from flask import Flask, request, jsonify
from app import app
import os

import users
import user

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)

