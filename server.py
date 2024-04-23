#!/usr/bin/env python3
import sqlite3
import string

import time
import binascii

from flask import Flask, render_template, render_template_string, request, abort, redirect, make_response, g, session, jsonify

app = Flask(__name__)

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('emoji.db')
    db.cursor().execute("PRAGMA journal_mode = MEMORY")
    db.commit()
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

@app.route('/')
def index():
  return render_template('index.html', user=session.get('user', None), ip=request.remote_addr)

def do_login(user, password, flag):
  return render_template('success.html', user=session.get('user', None), ip=request.remote_addr, flag=flag)

@app.route('/login', methods=['GET','POST'])
def login():
  user = request.form.get('user', None)
  password = request.form.get('password', None)

  if user is None or password is None:
    return render_template('login.html', ip=request.remote_addr)

  if "'" in password:
    return render_template('login.html', ip=request.remote_addr, message='Sorry, no single quotes allowed in password')

  c = get_db().cursor()

  statement = "select secretemoji from users where name='%s' and password='%s'" %(user,password)
  result = c.execute(statement).fetchone()

  if result:
    return do_login(user, password, result[0])
  else:
    return render_template('login.html', ip=request.remote_addr, message='Incorrect username or password')

if __name__ == '__main__':
  app.run(debug = True)
