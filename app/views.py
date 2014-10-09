# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from app import app, db, postreciver
from models import Game, Ship, Faction, Body, Star, System
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

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


@app.route('/api/ships.json')
def api_ships():
    if 'user' in session:
        shipquery = Ship.query.filter(Ship.body!=None)
        ships = shipquery.all()
        return jsonify(ships=[{'name' : ship.name,
                'class' : ship.shipclass.name,
                'faction' : ship.faction.name,
                'condition' : ship.condition}
                for ship in ships])
    return ""


#@app.route('/api/stars')
#def api_stars():
#    if 'user' in session:
#        starquery = Star.query
#        stars = starquery.all()
#        return jsonify(stars=[{'name' : star.name, 'x' : star.coo} for star in stars])
#    return ""

@app.route('/api/stars.json')
def api_stars():
    if 'user' in session:
        query = Star.query
        stars = query.all()
        #for item in stars:
        #    data.add("name":item.name)
        return jsonify(allstars=[{'name' : star.name, 'cx' : star.body.coordX, 'cy' : star.body.coordY} for star in stars])
    return redirect(url_for('login'))

@app.route('/api/stars.xml', methods=["GET", "POST"])
def xml_stars():
    if 'user' in session:
        root = ET.Element("root")
        stars = Star.query.all()
        for star in stars:
            xstar = ET.SubElement(root, "star")
            ident = ET.SubElement(xstar, "id")
            ident.text = str(star.id)
            name = ET.SubElement(xstar, "name")
            name.text = star.name
            cx = ET.SubElement(xstar, "cx")
            cx.text = str(star.body.coordX)
            cy = ET.SubElement(xstar, "cy")
            cy.text = str(star.body.coordY)
            mass = ET.SubElement(xstar, "mass")
            mass.text = str(star.body.mass)
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))

@app.route('/api/systems.xml', methods=["GET", "POST"])
def xml_systems():
    if 'user' in session:
        root = ET.Element("root")
        systems = System.query.all()
        for system in systems:
            xsystem = ET.SubElement(root, "system")
            for star in system.stars:
                xstar = ET.SubElement(xsystem, "star")
                ident = ET.SubElement(xstar, "id")
                ident.text = str(star.id)
                name = ET.SubElement(xstar, "name")
                name.text = star.name
                cx = ET.SubElement(xstar, "cx")
                cx.text = str(star.body.coordX)
                cy = ET.SubElement(xstar, "cy")
                cy.text = str(star.body.coordY)
                mass = ET.SubElement(xstar, "mass")
                mass.text = str(star.body.mass)
            for planets in system.planets:
                xplanet = ET.SubElement(xsystem, "planet")
                ident = ET.SubElement(xplanet, "id")
                name = ET.SubElement(xplanet, "name")
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))


@app.route('/api/ships.xml', methods=["GET", "POST"])
def xml_ships():
    if 'user' in session:
        root = ET.Element("root")
        ships = Ship.query.all()
        for ship in ships:
            xship = ET.SubElement(root, "ship")
            ident = ET.SubElement(xship, "id")
            ident.text = str(ship.id)
            name = ET.SubElement(xship, "name")
            name.text = ship.name
            cx = ET.SubElement(xship, "cx")
            cx.text = str(ship.body.coordX)
            cy = ET.SubElement(xship, "cy")
            cy.text = str(ship.body.coordY)
            mass = ET.SubElement(xship, "mass")
            mass.text = str(ship.body.mass)
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))

@app.route('/api/star<int:star_id>.xml', methods=["GET", "POST"])
def xml_star(star_id):
    if 'user' in session:
        root = ET.Element("root")
        star = Star.query.get(star_id)
        xstar = ET.SubElement(root, "star")
        ident = ET.SubElement(xstar, "id")
        ident.text = str(star.id)
        name = ET.SubElement(xstar, "name")
        name.text = star.name
        cx = ET.SubElement(xstar, "cx")
        cx.text = str(star.body.coordX)
        cy = ET.SubElement(xstar, "cy")
        cy.text = str(star.body.coordY)
        mass = ET.SubElement(xstar, "mass")
        mass.text = str(star.body.mass)
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))

@app.route('/api/ship<int:ship_id>.xml', methods=["GET", "POST"])
def xml_ship(ship_id):
    if 'user' in session:
        root = ET.Element("root")
        ship = Ship.query.get(ship_id)
        xship = ET.SubElement(root, "ship")
        ident = ET.SubElement(xship, "id")
        ident.text = str(ship.id)
        name = ET.SubElement(xship, "name")
        name.text = ship.name
        classname = ET.SubElement(xship, "classname")
        classname.text = ship.shipclass.name
        cx = ET.SubElement(xship, "cx")
        cx.text = str(ship.body.coordX)
        cy = ET.SubElement(xship, "cy")
        cy.text = str(ship.body.coordY)
        mass = ET.SubElement(xship, "mass")
        mass.text = str(ship.body.mass)
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))

@app.route('/api/imperium.xml', methods=["GET", "POST"])
def xml_imperium():
    if 'user' in session:
        root = ET.Element("root")
        ships = Ship.query.all()
        for ship in ships:
            xship = ET.SubElement(root, "ship")
            ident = ET.SubElement(xship, "id")
            ident.text = str(ship.id)
            name = ET.SubElement(xship, "name")
            name.text = ship.name
            cx = ET.SubElement(xship, "cx")
            cx.text = str(ship.body.coordX)
            cy = ET.SubElement(xship, "cy")
            cy.text = str(ship.body.coordY)
            mass = ET.SubElement(xship, "mass")
            mass.text = str(ship.body.mass)
        return ET.tostring(root, 'utf-8', method="xml")
    return redirect(url_for('login'))



app.secret_key = 'sjadiojapoqmwdm,ciowqewqjmdplkasm902348927ru9weojmc'
