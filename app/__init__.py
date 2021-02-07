from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import os
import subprocess
import platform

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'you-will-never-guess'
mysql = None
if platform.node() == 'bazy':
    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'g02'
    # app.config['MYSQL_PASSWORD'] = 'uythozxt'
    # app.config['MYSQL_DB'] = 'g02'
    # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql = MySQL(app)


bootstrap = Bootstrap(app)

if platform.node() != 'bazy':
    from car_workshop.app import routes
