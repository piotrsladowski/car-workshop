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
import datetime
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
# data = [{
#   "name": "spojler_fiat_126p",
#   "description": "Spojler do malucha",
#   "amount": "122",
#   "price": "450"
# },
#  {
#   "name": "plandeka_zuk",
#   "description": "Plandeka od żuka",
#   "amount": "0",
#   "price": "123,23"
# }, {
#   "name": "felgi",
#   "description": "Chromowane felgi",
#   "amount": "10",
#   "price": "99"
# }]
# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
# columns = [
#   {
#     "field": "name", # which is the field's name of data key 
#     "title": "name", # display as the table header's name
#     "sortable": True,
#   },
#   {
#     "field": "description",
#     "title": "description",
#     "sortable": True,
#   },
#   {
#     "field": "amount",
#     "title": "amount",
#     "sortable": True,
#   },
#   {
#     "field": "price",
#     "title": "price",
#     "sortable": True,
#   }
# ]

def check_date(date: str) -> bool:
  try:
    dt = datetime.date.fromisoformat(date)
    return True
  except ValueError:
    return False

formula = '[ `!@#$%^&*()+=\[\]{};\':"\\|,.<>\/\?~]'


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
    c.execute('''select id, name, surname from workers where is_working=1 and busy=0;''')
    rv = c.fetchall()
    
    workers = []
    for row in rv:
      full_name = row['name'] + ' ' + row['surname']
      workers.append({'id': row['id'], 'full_name': fullname})

    c.execute('''select id, description from cars where is_considered=0''')
    cars = c.fetchall()

    if request.method == 'POST':
      success = True
      pd = {}
      messages = []

      if re.search(formula, request.form['desc']) is not None:
        messages.append('You cannot enter special characters into the database in Realisation name!')
        success = False
      else:
        if len(request.form['desc'].strip()) == 0:
          messages.append('Description is required.')
          success = False
        elif len(request.form['desc'].strip()) < 200:
          pd['description'] = request.form['desc'].strip()
        else:
          messages.append('Description too long.')
          success = False
      
      if request.form['car'] not in [c['id'] for c in cars]:
        messages.append('You cannot choose car that does not exist in the database!')
        success = False
      else:
        pd['car_id'] = request.form['car']
      
      if request.form['worker'] not in [w['id'] for w in workers]:
        messages.append('You cannot choose worker that does not work in our workshop!')
        success = False
      else:
        pd['worker_id'] = request.form['worker']

      if request.form['cost'] not in ['less', 'more']:
        messages.append('There is no option for quality service you are looking for.')
        success = False
      else:
        if request.form['cost'] == 'less':
          pd['is_original'] = 0
        else:
          pd['is_original'] = 1

      if request.form['status'] not in ['open', 'rejected', 'finished']:
        messages.append('No other status option is considered.')
        success = False
      else:
        pd['status'] = request.form['status']

      if not check_date(request.form['deadline'].strip()):
        messages.append('This is not a date format. Stop messing HTML!')
        success = False
      else:
        pd['deadline'] = request.form['deadline']

      if success:
        c.execute('''
        insert into realisations
        (description, car_id, part_id, worker_id, cost, status, deadline)
        values
        ({0}, {1}, choose_part({1}, {3}), {2}, set_cost(choose_part({1}, {3}), {4}, {5}), {4}, {5})
        '''.format(pd['desc'], pd['car_id'], pd['worker_id'], pd['is_original'], pd['status'], pd['deadline']))
        rid = c.lastrowid
        mysql.connection.commit()
        # this should have a trigger to change car's is_considered to 1 and set worker to busy

        c.select('''select status, part_id from realisations where id={}'''.format(rid))
        rvr = c.fetchall()

        if rvr['status'] != 'rejected':
          c.execute('''select amount from parts where id={}'''.format(rvr['part_id']))
          part = c.fetchall()
          if part['amount'] > 0:
            c.execute('''update parts set amount={} where id={}'''.format(part['amount'], part['id']))
            mysql.connection.commit()

      return render_template('newJob.html', workers=workers, cars=cars, alerts=messages, success=success)

    return render_template('newJob.html', workers=workers, cars=cars)


@app.route('/newCar', methods=['GET', 'POST'])
def newCar():

    # fetching car_models
    c = mysql.connection.cursor()
    c.execute('''select id, car_model from car_models order by car_model;''')
    models = c.fetchall()

    c.execute('''select id, description from damages;''')
    damages = c.fetchall()

    if request.method == 'POST':
      pd = {}
      success = True
      messages = []
      # checking if the form values are not corrupted
      if re.search(formula, request.form['desc']) is not None:
        messages.append('You cannot enter special characters into the database in Description!')
        success = False
      else:
        if len(request.form['desc'].strip()) == 0:
          messages.append('Description is required.')
          success = False
        elif len(request.form['desc'].strip()) < 200:
          pd['description'] = request.form['desc'].strip()
        else:
          messages.append('Description too long.')
          success = False

      if request.form['model'] not in [m['id'] for m in models]:
        messages.append('You cannot enter Car Model to the database that our workshop cannot fix!')
        success = False
      else:
        pd['model_id'] = int(request.form['model'])

      if re.match(formula, request.form['vin']) is not None:
        messages.append('You cannot enter special characters into the database in Vin number!')
        success = False
      else:
        pd['vin_number'] = str(request.form['vin'])

      if request.form['damage'] not in [d['id'] for d in damages]:
        messages.append('You cannot enter Damage Type to the database that our workshop cannot fix!')
        success = False
      else:
        pd['damage'] = int(request.form['damage'])

      if request.form['isStolen'] not in ['stolenYes','stolenNo']:
        messages.append('Stop changing values in html tags!')
        success = False
      else:
        if request.form['isStolen'] == 'stolenYes':
          pd['is_stolen'] = 1
        elif request.form['isStolen'] == 'stolenNo':
          pd['is_stolen'] = 0

      if re.fullmatch('^\d+', request.form['carcounter']) is not None:
        if 0 < int(float(request.form['carcounter'])) and int(float(request.form['carcounter'])) < 100000:
            pd['car_counter'] = int(request.form['carcounter'])
        else:
          messages.append('Car counter out of range!')
          success = False
      else:
        messages.append('Car counter accepts only integer digit values.')
        success = False

      if re.fullmatch('^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', request.form['color']) is None:
        messages.append('Color HEX code is wrong. Go check it one more time.')
        success = False
      else:
        pd['color'] = str(request.form['color'])

      # actual insert
      if success:
        c.execute('''
        insert into cars 
        (description, model_id, vin_number, damage, is_stolen, car_counter, color, is_considered)
        values
        ({0}, {1}, {2}, {3}, {4}, {5}, {6}, 0);
        '''.format(pd['description'], pd['model_id'], pd['vin_number'], pd['damage'], pd['is_stolen'], pd['car_counter'], pd['color']))
        cid = str(c.lastrowid)
        mysql.connection.commit()

      return render_template('newCar.html', models=models, damages=damages, alerts=messages, success=success, cid=cid)

    return render_template('newCar.html', models=models, damages=damages)

@app.route('/pending')
def pending():
    # fetch pending jobs
    c = mysql.connection.cursor()
    c.execute('''select 
      (select description as 'car_desc'
      from cars 
      where id=r.car_id),
      (select 
        (select car_model as 'car_model'
        from car_models 
        where id=c.model_id), 
        c.vin_number as 'vin_number', 
        (select 
          description as 'dmg_desc'
        from damages 
        where id=c.damage)
      from cars as c 
      where c.id=r.car_id),
      (select code as 'code'
        from parts 
        where id=r.part_id), 
      (select 
        fullname(w.name, w.surname) as 'worker'
      from workers 
      where w.id=r.worker_id), 
      r.repair_cost as 'price', 
      r.deadline as 'deadline'
    from realisations as r
    where 
      r.status='open'
      or 
      r.status='delayed';''')
    data = c.fetchall()

    columns = [
      {
        "field": "car_desc",
        "title": "Car Description", 
        "sortable": False,
      },
      {
        "field": "car_model",
        "title": "Model of the repaired car",
        "sortable": True,
      },
      {
        "field": "vin_number",
        "title": "Car's VIN Number",
        "sortable": False,
      },
      {
        "field": "dmg_desc",
        "title": "Damage Description",
        "sortable": True,
      },
      {
        "field": "code",
        "title": "Code of the part used to repair the car", 
        "sortable": True,
      },
      {
        "field": "price",
        "title": "Price of the whole realisation",
        "sortable": True,
      },
      {
        "field": "deadline",
        "title": "Deadline",
        "sortable": True,
      },
      {
        "field": "worker",
        "title": "Person responsible for repair",
        "sortable": True,
      }
    ]

    return render_template('pending.html', data=data, columns=columns)

@app.route('/finished')
def finished():
    # fetch finished jobs
    c = mysql.connection.cursor()
    c.execute('''select 
      (select description as 'car_desc'
      from cars 
      where id=r.car_id),
      (select 
        (select car_model as 'car_model'
        from car_models 
        where id=c.model_id), 
        c.vin_number as 'vin_number', 
        (select 
          description as 'dmg_desc'
        from damages 
        where id=c.damage)
      from cars as c 
      where c.id=r.car_id),
      (select code as 'code'
        from parts 
        where id=r.part_id), 
      (select 
        fullname(w.name, w.surname) as 'worker'
      from workers 
      where w.id=r.worker_id), 
      r.repair_cost as 'price', 
      r.deadline as 'deadline'
    from realisations as r
    where 
      r.status='rejected'
      or 
      r.status='finished';''')
    data = c.fetchall()

    columns = [
      {
        "field": "car_desc",
        "title": "Car Description", 
        "sortable": False,
      },
      {
        "field": "car_model",
        "title": "Model of the repaired car",
        "sortable": True,
      },
      {
        "field": "vin_number",
        "title": "Car's VIN Number",
        "sortable": False,
      },
      {
        "field": "dmg_desc",
        "title": "Damage Description",
        "sortable": True,
      },
      {
        "field": "code",
        "title": "Code of the part used to repair the car", 
        "sortable": True,
      },
      {
        "field": "price",
        "title": "Price of the whole realisation",
        "sortable": True,
      },
      {
        "field": "deadline",
        "title": "Deadline",
        "sortable": True,
      },
      {
        "field": "worker",
        "title": "Person responsible for repair",
        "sortable": True,
      }
    ]

    #jobs_finished = list(rv)
    
    return render_template('finished.html', data=data, columns=columns)

@app.route('/warehouse')
def warehouse():
    # fetch parts
    c = mysql.connection.cursor()
    c.execute('''select pid, code, is_original, price, amount, description from parts where amount > 0;''')
    rv = c.fetchall()

    data = []
    for row in rv:
      c.execute('''select (select car_model from car_models where id=car_id) from cars_parts where part_id={}'''.format(row['id']))
      models = c.fetchall()
      mds = ' , '.join([m['car_model'] for m in models])
      data.append({'code': row['code'], 'original': row['is_original'], 'price': row['price'], 'amount': row['amount'], 'models': mds, 'description': row['description']})

    columns = [
      {
        "field": "code",
        "title": "Code of the part", 
        "sortable": True,
      },
      {
        "field": "description",
        "title": "Description",
        "sortable": True,
      },
      {
        "field": "amount",
        "title": "Available amount",
        "sortable": True,
      },
      {
        "field": "price",
        "title": "Price",
        "sortable": True,
      },
      {
        "field": "original",
        "title": "Original part/Replacement",
        "sortable": True,
      },
      {
        "field": "models",
        "title": "Models the part fits",
        "sortable": False,
      }
    ]

    return render_template('warehouse.html', data=data, columns=columns, title='Car parts available in the warehouse')

# ADDONS
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

@app.route('/gameOver')
def gameOver():
    return render_template('gameOver.html')

if __name__ == '__main__':
	#print jdata
  app.run(debug=True)


