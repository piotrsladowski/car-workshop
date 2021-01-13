from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import os
import subprocess
import platform

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_WORD='dev')
app.config['SECRET_KEY'] = 'you-will-never-guess'
mysql = None
if platform.node() == 'bazy':
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'g02'
    app.config['MYSQL_PASSWORD'] = 'uythozxt'
    app.config['MYSQL_DB'] = 'g02'

    mysql = MySQL(app)


bootstrap = Bootstrap(app)

if os.name == 'nt':
    from car_workshop.app import routes
else:    
    if not (subprocess.check_output('uname -mrs', stderr=subprocess.STDOUT, shell=True).rstrip().decode('utf-8') == 'Linux 4.18.0-240.1.1.el8_3.x86_64 x86_64'):
        from car_workshop.app import routes
