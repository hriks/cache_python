from flask import Flask, render_template, request, redirect, url_for,\
    session, flash
from logging import Formatter, FileHandler
from forms import *
import logging
import sys
import csv


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config.from_object('config')


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
    flash('Records Saved')
    return render_template('layouts/shutdown.html')


# Controllers.


def write():
    try:
        records = cache_records()
        for i in records:
            print i
    except Exception:
        flash('New File created with name %s' % (sys.argv[1]))

    with open(sys.argv[1], 'w+') as csvfile:
        fieldnames = ['ids', 'student_name', 'academics', 'sports', 'social']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        try:
            for record in records:
                writer.writerow(record)
        except Exception:
            flash('New File created with name %s' % (sys.argv[1]))


def read():
    input_file = csv.DictReader(open(sys.argv[1]))
    data = []
    for i in input_file:
        data.append(i)
    return data


def read_cache():
    data = session['data']
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
        return data


def delete_cache(ids):
    data = cache_records()
    if ids:
        for delete in data:
            if int(delete['ids']) == int(ids):
                data.pop(data.index(delete))
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
    ids = session['ids']
    name = session['student_name']
    if request.method == 'POST':
        academics = form.academics.data
        sports = form.sports.data
        social = form.social.data
        if academics is None or int(academics) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Academics' % (
                    academics))
            return redirect(url_for('update'))
        elif sports is None or int(sports) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Sports' % (
                    sports))
            return redirect(url_for('update'))
        elif social is None or int(social) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Social' % (
                    social))
            return redirect(url_for('update'))
        else:
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
    try:
        ids = ids_get()
    except Exception:
        flash('File Doesnot exits Shutdown to Create a file with name %s' % (sys.argv[1]))
        return redirect(url_for('home'))
    form = add_student(request.form)
    if request.method == 'POST':
        student_name = form.student_name.data
        academics = form.academics.data
        sports = form.sports.data
        social = form.social.data
        if student_name is None:
            flash('%s is not vaild. Please Enter valid name' % student_name)
            return redirect(url_for('addinfo'))
        elif academics is None or int(academics) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Academics' % (
                    academics))
            return redirect(url_for('addinfo'))
        elif sports is None or int(sports) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Sports' % (
                    sports))
            return redirect(url_for('addinfo'))
        elif social is None or int(social) > 100:
            flash(
                '%s is not a valid score.\
                 Please enter valid score for Social' % (
                    social))
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
        try:
            records = cache_records()
        except Exception:
            flash(
                'No such file Present,\
                 please provide a vailid file or shutdown to create file')
            return redirect(url_for('home'))
        try:
            match = filter(
                lambda record: int(record["ids"]) == int(search), records
            )
            for i in records:
                if i['ids'] == int(search):
                    count[int(search)] = count[int(search)] + 1
        except Exception:
            flash('Invalid ID Provided, Please Provide ID')
            return redirect(url_for('home'))
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
