from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import os
import subprocess
import platform

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'you-will-never-guess'
mysql = MySQL()
if platform.node() == 'bazy':
    from project import config
    cnf = config.Config()
    app.config.from_object(cnf)
    app.config['MYSQL_HOST'] = cnf.DB_HOST
    app.config['MYSQL_USER'] = cnf.DB_USER
    app.config['MYSQL_PASSWORD'] = cnf.DB_PASSWORD
    app.config['MYSQL_DB'] = cnf.DB_DB
    app.config['MYSQL_CURSORCLASS'] = cnf.DB_CURSORCLASS

    mysql.init_app(app)


bootstrap = Bootstrap(app)

if platform.node() != 'bazy':
    from car_workshop.app import routes, errors
