import subprocess
import os
import platform

if platform.node() == 'bazy':
    from project.car_workshop.app import app, mysql
    from project.car_workshop.app.forms import LoginForm, NewJobButtonForm, procrastinationButtonForm, ageNoButtonForm, ageYesButtonForm
else:
    from car_workshop.app import app, mysql
    from car_workshop.app.forms import LoginForm, NewJobButtonForm, procrastinationButtonForm, ageNoButtonForm, ageYesButtonForm

from flask import render_template, flash, redirect, request, url_for
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

# @app.route('/course/<coursename>')
# def course(coursename):
    """course = Course.query.filter_by(coursename=coursename).first_or_404()
    course_id = course.id
    files = Files.query.filter_by(course_id=course_id)"""
    #return render_template('course.html', course=course, files=files)
    # return render_template('course.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = LoginForm()
    newJob = NewJobButtonForm()
    procrastination = procrastinationButtonForm()
    if request.method == 'POST':
      if request.form.get('newJob') == 'New job':
        return redirect(url_for('newJob'))
      if request.form.get('procrastination') == 'Procrastinate':
        return redirect('https://www.youtube.com/watch?v=EErY75MXYXI')
    return render_template('dashboard.html', downloadingText="dummy value",form=form, newJob=newJob, procrastination=procrastination)

@app.route('/newJob', methods=['GET', 'POST'])
def newJob():
    # fetch workers
    c = mysql.connection.cursor()
    c.execute('''select name, surname, is_working, busy from workers where is_working=1 and busy=0''')
    rv = c.fetchall()
    
    workers = []
    for row in rv:
      full_name = row['name'] + ' ' + row['surname']
      workers.append(full_name)

    if request.method == 'POST':
      print(request.form)
    colours = ['Red', 'Blue', 'Black', 'Orange', 'Green', 'White']
    return render_template('newJob.html')

@app.route('/pending')
def pending():
    # fetch pending jobs
    c = mysql.connection.cursor()
    c.execute('''select (select (select car_model from car_models where id=c.model_id), vin_number, damage from cars as c where c.id=car_id), (select fullname(w.name, w.surname) from workers where w.id=worker_id), repair_cost, deadline from realisations where status='pending' ''')
    rv = c.fetchall()

    jobs_pending = list(rv)
    return render_template('pending.html', jobs=jobs_pending)

@app.route('/newCar')
def newCar():
    # fetching car_models
    c = mysql.connection.cursor()
    c.execute('''select * from car_models order by car_model''')
    rv = c.fetchall()
    models = []
    for row in rv:
      models.append(row['car_model'])
    
    # setting up models
    colours = ['Red', 'Blue', 'Black', 'Orange', 'Green', 'White']

    return render_template('newCar.html', colours=colours, models=models)

@app.route('/finished')
def finished():
    # fetch finished jobs
    c = mysql.connection.cursor()
    c.execute('''select (select (select car_model from car_models where id=c.model_id), vin_number, damage from cars as c where c.id=car_id), (select fullname(w.name, w.surname) from workers where w.id=worker_id), repair_cost, deadline from realisations where status='finished' ''')
    rv = c.fetchall()
    
    jobs_finished = list(rv)
    
    return render_template('finished.html', jobs=jobs_finished)

@app.route('/warehouse')
def warehouse():
    # fetch parts
    c = mysql.connection.cursor()
    c.execute('''select * from parts''')
    rv = c.fetchall()

    parts = list(rv)

    return render_template('warehouse.html', data=data, columns=columns, title='Car parts available')

@app.route('/calendar2021', methods=['GET', 'POST'])
def calendar2021():
    ageYes = ageYesButtonForm()
    ageNo = ageNoButtonForm()
    if request.method == 'POST':
      if request.form.get('ageNo') == 'No':
        return redirect(url_for('index'))
      if request.form.get('ageYes') == 'Yes':
        return redirect(url_for('chamberOfSecrets'))
    return render_template('calendar2021.html', ageYes=ageYes, ageNo=ageNo)

@app.route('/chamberOfSecrets')
def chamberOfSecrets():
    return redirect('https://youtu.be/dQw4w9WgXcQ?t=43')

if __name__ == '__main__':
	#print jdata
  app.run(debug=True)


