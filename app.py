from flask import Flask, render_template as render, request, redirect,\
    url_for, session as s
from flask import flash as hriks
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
    s.clear()
    shutdown_server()
    print len(cache_records())
    try:
        if len(cache_records()) >= 1:
            hriks(
                'Notification : Records Saved !'
            )
    except Exception:
        hriks(
            'Notification : New file created with name "%s" ' % (
                sys.argv[1]
            )
        )
    return render('layouts/shutdown.html')


# Controllers.
def write():
    try:
        records = cache_records()
        for i in records:
            print i
    except Exception:
        hriks(
            'New File created with name %s' % (
                sys.argv[1]
            )
        )
    with open(sys.argv[1], 'w+') as csvfile:
        fieldnames = [
            'ids', 'student_name', 'academics', 'sports', 'social'
        ]
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames
        )

        writer.writeheader()
        try:
            for record in records:
                writer.writerow(record)
        except Exception:
            hriks('New File created with name %s' % (
                sys.argv[1]
            )
            )


def read():
    input_file = csv.DictReader(open(sys.argv[1]))
    data = []
    for i in input_file:
        data.append(i)
    return data


def read_cache():
    data = s['data']
    return data


def write_cache(student_name, academics, sports, social):
    import pdb; pdb.set_trace()
    data = cache_records()
    if len(data) == 20:
        if 'count' in s:
            count = s['count']
            print count
            data = delete_cache(count)
        else:
            data = cache_records()
            while len(data) == 20:
                data.pop()
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
    return render('pages/placeholder.home.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        s['ids'] = request.form['submit']
        s['delete'] = request.form['delete']
        ids = s['ids']
        data = delete_cache(ids)
        s['data'] = data
        hriks(
            'Notification : Successfully deleted records with ID %s' % (ids)
        )
        s['ids'] = None
        s['student_name'] = None
        return redirect(url_for('home'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = Update_student_info(request.form)
    s['ids'] = request.form['submit']
    ids = s['ids']
    s['student_name'] = request.form['name']
    name = s['student_name']
    if request.method == 'POST':
        return redirect(url_for('update'))
    return render(
        'forms/update.html', form=form, ids=ids, name=name
    )


@app.route('/update', methods=['GET', 'POST'])
def update():
    form = Update_student_info(request.form)
    ids = s['ids']
    name = s['student_name']
    if request.method == 'POST':
        academics = form.academics.data
        sports = form.sports.data
        social = form.social.data
        if academics is None or int(academics) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Academics' % (
                    academics))
            return redirect(url_for('update'))
        elif sports is None or int(sports) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Sports' % (
                    sports))
            return redirect(url_for('update'))
        elif social is None or int(social) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Social' % (
                    social))
            return redirect(url_for('update'))
        else:
            data = update_cache(
                s['ids'], s['student_name'],
                academics, sports, social
            )
            s['data'] = data
            hriks(
                'Notification : Successfully updated record for %s \
                with ID %s' % (name, ids)
            )
            return redirect(
                url_for('home')
            )
    return render(
        'forms/update.html', form=form, ids=ids, name=name
    )


@app.route('/addinfo', methods=['GET', 'POST'])
def addinfo():
    try:
        ids = ids_get()
    except Exception:
        hriks(
            'Notification : File doesnot exits. Shutdown to create a \
            file with name %s' % (sys.argv[1])
        )
        return redirect(url_for('home'))
    form = add_student(request.form)
    if request.method == 'POST':
        student_name = form.student_name.data
        academics = form.academics.data
        sports = form.sports.data
        social = form.social.data
        if student_name is None:
            hriks(
                'Notification : %s is not vaild. Please Enter valid \
                name' % student_name
            )
            return redirect(url_for('addinfo'))
        elif academics is None or int(academics) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Academics' % (
                    academics)
            )
            return redirect(url_for('addinfo'))
        elif sports is None or int(sports) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Sports' % (
                    sports)
            )
            return redirect(url_for('addinfo'))
        elif social is None or int(social) > 100:
            hriks(
                'Notification : %s is not a valid score.\
                 Please enter valid score for Social' % (
                    social)
            )
            return redirect(url_for('addinfo'))
        else:
            data = write_cache(
                student_name, academics, sports, social
            )
            s['data'] = data
            hriks(
                'Notification : %s successfully added to records \
                with ID %s' % (
                    student_name, ids
                )
            )
            return redirect(url_for('home'))
    return render('forms/register.html', form=form, ids=ids)


@app.route('/search', methods=['GET', 'POST'])
def search():
    count = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0,14:0,15:0,16:0,17:0,18:0,19:0,20:0} # noqa
    inverse = [(value, key) for key, value in count.items()]
    s['count'] = max(inverse)[0]
    if request.method == 'POST':
        search = request.form['search']
        try:
            records = cache_records()
        except Exception:
            hriks(
                'Notification : No such file present.\
                 Please provide a valid file or shutdown to create file'
            )
            return redirect(url_for('home'))
        try:
            match = filter(
                lambda record: int(record["ids"]) == int(search), records
            )
            for i in records:
                if i['ids'] == int(search):
                    count[int(search)] = count[int(search)] + 1
        except Exception:
            hriks('Notification : Invalid ID provided, Please provide ID')
            return redirect(url_for('home'))
        return render(
            'pages/placeholder.search.html', match=match, search=search
        )
    return render('pages/placeholder.search.html', search=search)


# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render('errors/404.html'), 404


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
