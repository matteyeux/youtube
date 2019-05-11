# youtube

## Virtual Environment

### Dependencies
Ubuntu :
- install `python3-virtualenv` : `sudo apt install python3-virtualenv`

Debian :
- install `python3-pip3` : `sudo apt install python3-pip`
- install `virtualenv`with easy_instal : `sudo easy_install3 virtualenv`

### Setup
In the root directory of the projet create the new env : `virtualenv -p python3 env`. It will create a new directory named `env` with all you need to start coding.

Enable virtual env : `source env/bin/activate`

Install Python modules : `pip3 install -r requirements.txt`

## MySQL

1) install MySQL :  `sudo apt install mysql-client mysql-server`
2) create database : `CREATE DATABASE youtube;`
3) create youtube user : `CREATE USER 'youtube'@'localhost' IDENTIFIED BY 'youtube';`
(In case of error : )
4) grant all privileges to youtube user for youtube DB : `GRANT ALL PRIVILEGES ON *.* TO 'youtube'@'localhost';`
5) insert data : `mysql -u youtube  youtube < resources/database.sql`
6) ???
7) start coding

## Run tha API

`youtube/youtube.py`

### Followed tutorial

This one uses MySQL instead of SQLite3 https://www.roytuts.com/python-rest-api-crud-example-using-flask-and-mysql/
