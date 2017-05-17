from flask import Flask, render_template, request, redirect, url_for,\
    session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from functools import wraps
from forms import *
import logging
import sys
import csv


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
app.config.from_object('config')
db = SQLAlchemy(app)


# Decorator's

def id_requied(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['id']:
            return f(*args, **kwargs)
        else:
            flash(
                ' Sorry! You dont have entered anything')
            return redirect(url_for('home'))
    return wrap

# Controllers.


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('pages/placeholder.home.html')


def read():
    session.clear()
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
    new_dict = {}
    new_dict['ids'] = ids_get()
    new_dict['student_name'] = student_name
    new_dict['academics'] = academics
    new_dict['sports'] = sports
    new_dict['social'] = social
    data.append(new_dict)
    return data


def ids_get():
    try:
        return len(read_cache()) + 1
    except Exception:
        return len(read()) + 1


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
        if academics is None or sports is None or social is None: # noqa
            flash(
                'ERROR! Please enter interger value on Score and text on Name or\
                 check id already exists.'
            )
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


def cache_records():
    try:
        return read_cache()
    except Exception:
        return read()


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form['search']
        records = cache_records()
        match = filter(
            lambda record: int(record["ids"]) == int(search), records
        )
        print match
        return render_template(
            'pages/placeholder.search.html', match=match, search=search
        )
    return render_template('pages/placeholder.search.html', search=search)


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        models.post_messages(
            session['name'], request.form['message'])
        return redirect(url_for('home'))


@app.route('/delete', methods=['GET', 'POST'])
@id_requied
def delete():
    if request.method == 'POST':
        models.message_delete(
            request.form['submit'])
        return redirect(url_for('home'))


@app.route('/edit', methods=['GET', 'POST'])
@id_requied
def edit():
    if request.method == 'POST':
        session['editid'] = request.form['submit']
        return redirect(url_for('update'))


@app.route('/update', methods=['GET', 'POST'])
@id_requied
def update():
    if session['editid']:
        userid = session['editid']
    else:
        userid = session['name']
    form = UpdateForm(request.form)
    get_info = models.get_info(userid)
    if request.method == 'POST':
        user = models.update(
            form.role.data, userid, form.password.data,
            form.email.data, form.name.data
        )
        if user != 1:
            flash(
                "ERROR! Already on this role, or you hadn't updated anything"
            )
            return redirect(url_for('update'))
        else:
            flash(
                'Successfully Role changed for  %s to %s' % (
                    userid, form.role.data)
            )
            session['editid'] = None
            return redirect(url_for('users'))
    return render_template(
        'forms/update.html', form=form, userid=userid, get_info=get_info
    )


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
