from flask import Flask
from flask_bootstrap import Bootstrap
import os
import subprocess

app = Flask(__name__)
bootstrap = Bootstrap(app)
if not (subprocess.check_output('uname -mrs', stderr=subprocess.STDOUT, shell=True).rstrip().decode('utf-8') == 'Linux 4.18.0-240.1.1.el8_3.x86_64 x86_64'):
    from car_workshop.app import routes
