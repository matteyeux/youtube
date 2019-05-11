from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://youtube:youtube@localhost/youtube'

# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False