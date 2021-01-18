from flask import render_template
import subprocess
import os
import time

if os.name == 'posix':
  if (subprocess.check_output('uname -mrs', stderr=subprocess.STDOUT, shell=True).rstrip().decode('utf-8') == 'Linux 4.18.0-240.1.1.el8_3.x86_64 x86_64'):
    from project.car_workshop.app import app
  else:
    from car_workshop.app import app, mysql
elif os.name == 'nt':
  from car_workshop.app import app, mysql


@app.errorhandler(404)
def not_found_error(error):
    num = int(time.time()) % 2
    return render_template('404.html', num=num), 404