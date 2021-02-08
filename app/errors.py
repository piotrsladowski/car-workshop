from flask import render_template
import subprocess
import os
import time

if os.name == 'posix':
  if (subprocess.check_output('uname -mrs', stderr=subprocess.STDOUT, shell=True).rstrip().decode('utf-8') == 'Linux 4.18.0-240.10.1.el8_3.x86_64 x86_64'):
    from project.car_workshop.app import app
  else:
    from car_workshop.app import app
elif os.name == 'nt':
  from car_workshop.app import app


@app.errorhandler(404)
def not_found_error(error):
    num = int(time.time()) % 2
    return render_template('404.html', num=num), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

