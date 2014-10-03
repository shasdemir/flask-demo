import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing


DATABASE = '/tmp/flask_demo.db'
DEBUG = True
SECRET_KEY = 'for all uppercase 34 variables defined there.'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cursor = g.db.execute('select title, text from entries order by id desc')
    entries = [{'title': row[0], 'text':row[1]} for row in cursor.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if nit session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)'), [request.form['title'], request.form['text']]
    g.db.commit()
    flash('New entry was successfully posted.')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()