# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from app import app, db, postreciver
from models import Game, Ship, Faction, Body, Star

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
        return render_template("index.html", title = 'Kvantgeneraatori plahvatus')
    return redirect(url_for('login'))


@app.route('/api/ships')
def api_ships():
    if 'user' in session:
        shipquery = Ship.query.filter(Ship.body!=None)
        ships = shipquery.all()
        return jsonify(ships=[{'name' : ship.name} for ship in ships])
    return ""


@app.route('/api/stars')
def api_stars():
    if 'user' in session:
        starquery = Star.query
        stars = starquery.all()
        return jsonify(stars=[{'name' : star.name} for star in stars])
    return ""



@app.route('/stars')
def stars():
    if 'user' in session:
        query = Star.query
        stars = query.all()
        #for item in stars:
        #    data.add("name":item.name)
        return jsonify(allstars=[e.serialize() for e in stars])
    return redirect(url_for('login'))


app.secret_key = 'sjadiojapoqmwdm,ciowqewqjmdplkasm902348927ru9weojmc'
