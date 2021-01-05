import subprocess
import os

if os.name == 'posix':
  if (subprocess.check_output('uname -mrs', stderr=subprocess.STDOUT, shell=True).rstrip().decode('utf-8') == 'Linux 4.18.0-240.1.1.el8_3.x86_64 x86_64'):
    from project.car_workshop.app import app
    #from app.models import Course, Files
  else:
    from flask import render_template, flash, redirect, request
    from car_workshop.app import app
elif os.name == 'nt':
  from flask import render_template, flash, redirect, request
  from car_workshop.app import app

import re
from pathlib import Path
import time
import json

# This line has to be set manually
coursesList = []

########### Logic #############

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def verbose_cls():
    clear_console()

def handle_windows_path(posix_path):
    if os.name == 'nt':
        return posix_path.replace('/', '\\')
    return posix_path

"""
def getCourseList():
    global coursesList
    tempList = Course.query.all()
    for item in tempList:
        c = str(item).split()[1]
        c = c[:-1]
        coursesList.append(c)
"""
#getCourseList()
data = [{
  "name": "spojler_fiat_126p",
  "description": "Spojler do malucha",
  "amount": "122",
  "price": "450"
},
 {
  "name": "plandeka_zuk",
  "description": "Plandeka od żuka",
  "amount": "0",
  "price": "123,23"
}, {
  "name": "felgi",
  "description": "Chromowane felgi",
  "amount": "10",
  "price": "99"
}]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
  {
    "field": "name", # which is the field's name of data key 
    "title": "name", # display as the table header's name
    "sortable": True,
  },
  {
    "field": "description",
    "title": "description",
    "sortable": True,
  },
  {
    "field": "amount",
    "title": "amount",
    "sortable": True,
  },
  {
    "field": "price",
    "title": "price",
    "sortable": True,
  }
]

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Dashboard')

@app.route('/course/<coursename>')
def course(coursename):
    """course = Course.query.filter_by(coursename=coursename).first_or_404()
    course_id = course.id
    files = Files.query.filter_by(course_id=course_id)"""
    #return render_template('course.html', course=course, files=files)
    return render_template('course.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', downloadingText="dummy value")

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/pending')
def pending():
    return render_template('pending.html')

@app.route('/finished')
def finished():
    return render_template('finished.html')

@app.route('/warehouse')
def warehouse():
    #return render_template("table.html", data=data, columns=columns, title='Flask Bootstrap Table')
    return render_template('warehouse.html', data=data, columns=columns, title='Tabela')


if __name__ == '__main__':
	#print jdata
  app.run(debug=True)


