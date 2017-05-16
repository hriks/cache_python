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
        if session['role'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash(
                ' Sorry! You dont have any permission to perform such action')
            return redirect(url_for('home'))
    return wrap

# Controllers.


@app.route('/', methods=['GET', 'POST'])
def home():
    input_file = csv.DictReader(open(sys.argv[1]))
    for i in input_file:
        print i
    return render_template('pages/placeholder.home.html')


@app.route('/addinfo', methods=['GET', 'POST'])
def addinfo():
    form = add_student(request.form)
    if request.method == 'POST':
        ids = form.ids.data
        print ids
        student_name = form.student_name.data
        print student_name
        academics = form.academics.data
        print academics
        sports = form.sports.data
        print sports
        social = form.social.data
        print social
#        if user == 1:
#            flash(
#                'ERROR! Please enter something or check yours\
#                username or user already exists'
#            )
#            return redirect(url_for('addinfo'))
#        else:
        return redirect(url_for('home'))
    return render_template('forms/register.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
@id_requied
def search():
    search = request.form['search']
    match = flask_login_auth.searchbox(search)
    print match
    return render_template('pages/placeholder.search.html', search=search,
                           match=match)


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
    # db_session.rollback()
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
