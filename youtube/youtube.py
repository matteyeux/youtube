#!/usr/bin/env python3

import sys
from app import app

import user
import users
import video
import errors

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=5000)
