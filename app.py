from flask import Flask, render_template, request, redirect, url_for,\
    session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from forms import *
import logging
import sys
import csv


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config.from_object('config')
db = SQLAlchemy(app)


# Shutdown Server


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    write()
    session.clear()
    shutdown_server()
    return 'Server shutting down...'


# Controllers.


def write():
    records = cache_records()
    print records
    for i in records:
        print i

    with open(sys.argv[1], 'w+') as csvfile:
        fieldnames = ['ids', 'student_name', 'academics', 'sports', 'social']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for record in records:
            print records
            writer.writerow(record)


def read():
    input_file = csv.DictReader(open(sys.argv[1]))
    data = []
    for i in input_file:
        data.append(i)
    return data


def read_cache():
    data = session['data']
    print 'read cache', data
    return data


def write_cache(student_name, academics, sports, social):
    data = cache_records()
    if len(data) >= 20:
        count = session['count']
        delete_cache(count)
    new_dict = {}
    new_dict['ids'] = ids_get()
    new_dict['student_name'] = student_name
    new_dict['academics'] = academics
    new_dict['sports'] = sports
    new_dict['social'] = social
    data.append(new_dict)
    return data


def update_cache(ids, student_name, academics, sports, social):
    data = cache_records()
    if ids and student_name:
        for update in data:
            if int(update['ids']) == int(ids) and update['student_name'] == student_name: # noqa
                update['academics'] = academics
                update['sports'] = sports
                update['social'] = social
        print data
        return data


def delete_cache(ids):
    data = cache_records()
    if ids:
        for delete in data:
            if int(delete['ids']) == int(ids):
                data.pop(data.index(delete))
        print data
        for ids in data:
            ids['ids'] = data.index(ids) + 1
        return data


def ids_get():
    try:
        return len(read_cache()) + 1
    except Exception:
        return len(read()) + 1


def cache_records():
    try:
        return read_cache()
    except Exception:
        return read()


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        session['ids'] = request.form['submit']
        session['delete'] = request.form['delete']
        ids = session['ids']
        data = delete_cache(
            session['ids']
        )
        session['data'] = data
        flash(
            'Successfully Deleted ID %s' % (ids)
        )
        session['ids'] = None
        session['student_name'] = None
        return redirect(url_for('home'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = Update_student_info(request.form)
    session['ids'] = request.form['submit']
    ids = session['ids']
    session['student_name'] = request.form['name']
    name = session['student_name']
    if request.method == 'POST':
        return redirect(url_for('update'))
    return render_template(
        'forms/update.html', form=form, ids=ids, name=name
    )


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = Update_student_info(request.form)
    print session['ids']
    ids = session['ids']
    print session['student_name']
    name = session['student_name']
    if request.method == 'POST':
        academics = form.academics.data
        print academics
        sports = form.sports.data
        print sports
        social = form.social.data
        print social
        if academics is None or academics >= 100:
            flash('Please enter valid score for Academics')
            return redirect(url_for('update'))
        elif sports is None or sports >= 100:
            flash('Please enter valid score for Sports')
            return redirect(url_for('update'))
        elif social is None or social >= 100:
            flash('Please enter valid score for Sports')
            return redirect(url_for('update'))
        else:
            print session['ids']
            data = update_cache(
                session['ids'], session['student_name'],
                academics, sports, social
            )
            session['data'] = data
            flash(
                'Successfully Updated %s \
                with ID %s' % (name, ids)
            )
            return redirect(url_for('home'))
    return render_template(
        'forms/update.html', form=form, ids=ids, name=name
    )


@app.route('/addinfo', methods=['GET', 'POST'])
def addinfo():
    ids = ids_get()
    form = add_student(request.form)
    if request.method == 'POST':
        student_name = form.student_name.data
        print student_name
        academics = form.academics.data
        print academics
        sports = form.sports.data
        print sports
        social = form.social.data
        print social
        if student_name is not str or None:
            flash('Please Enter name')
            return redirect(url_for('update'))
        elif academics is None or academics >= 100:
            flash('Please enter valid score for Academics')
            return redirect(url_for('update'))
        elif sports is None or sports >= 100:
            flash('Please enter valid score for Sports')
            return redirect(url_for('addinfo'))
        elif social is None or social >= 100:
            flash('Please enter valid score for Sports')
            return redirect(url_for('addinfo'))
        else:
            data = write_cache(
                student_name, academics, sports, social
            )
            session['data'] = data
            flash(
                'Successfully Added new Records with ID %s \
                for Student Name %s' % (ids, student_name)
            )
            return redirect(url_for('home'))
    return render_template('forms/register.html', form=form, ids=ids)


@app.route('/search', methods=['GET', 'POST'])
def search():
    count = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0} # noqa
    inverse = [(value, key) for key, value in count.items()]
    session['count'] = max(inverse)[0]
    if request.method == 'POST':
        search = request.form['search']
        records = cache_records()
        try:
            match = filter(
                lambda record: int(record["ids"]) == int(search), records
            )
            for i in records:
                if i['ids'] == search:
                    print i
                    print count[search]
                    count[search] = count[search] + 1

        except Exception:
            flash('Invalid ID Provided, Please Provide ID')
            return redirect(url_for('home'))
        print match
        return render_template(
            'pages/placeholder.search.html', match=match, search=search
        )
    return render_template('pages/placeholder.search.html', search=search)


# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('% (asctime)s % (levelname)s: % (message)s\
                  [in % (pathname)s: % (lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


# Default port:
if __name__ == '__main__':
    app.run(debug=True)
