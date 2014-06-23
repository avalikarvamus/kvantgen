# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request
from app import app, db, postreciver
from models import Game, Ship, Faction, Body

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.has_key('kasutaja') and request.form.has_key('salakala'):
            clMachine = request.form['kasutaja']
            clSecret = request.form['salakala']
            if clMachine=="test" and clSecret=="toomas":
                session['user']=clMachine
                return redirect(url_for('index'))
    return render_template('loginform.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'user' in session:
        query = Ship.query.filter(Ship.body!=None)
        ships = query.all()
        return render_template("index.html", title = 'Kvantgeneraatori plahvatus', ships=ships)
    return redirect(url_for('login'))

app.secret_key = 'sjadiojapoqmwdm,ciowqewqjmdplkasm902348927ru9weojmc'
