# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions, datetime
from flask import (render_template, flash, redirect,
                session, url_for, request, jsonify, json)
from app import app, db, postreciver
from models import Game, Ship, Faction, Body, Star, System, Person
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


noUser = "{ 'error' : 'No user in session!' }"

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if ('kasutaja' in request.form and
                    'salakala' in request.form):
            clMachine = request.form['kasutaja']
            clSecret = request.form['salakala']
            if clMachine == "test" and clSecret == "toomas":
                session['user'] = clMachine
                return redirect(url_for('index'))
    return render_template('loginform.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'user' in session:
        return render_template("index.html",
                title = 'Kvantgeneraatori plahvatus')
    return redirect(url_for('login'))


@app.route('/api/ships/')
def api_ships():
    if 'user' in session:
        shipquery = Ship.query #.filter(Ship.body!=None)
        ships = shipquery.all()
        return jsonify(ships=[{'name': ship.name,
                'class': ship.shipclass.name,
                'faction': ship.faction.name,
                'condition': ship.condition}
                for ship in ships])
    return noUser

@app.route('/api/ships/<int:ship_id>')
def api_ship(ship_id):
    if 'user' in session:
        ship = Ship.query.get(ship_id)
        return jsonify({'name': ship.name,
                'class': ship.shipclass.name,
                'faction': ship.faction.name,
                'condition': ship.condition}
                )
    return noUser

@app.route('/api/stars/')
def api_stars():
    if 'user' in session:
        query = Star.query
        stars = query.all()
        #for item in stars:
        #    data.add("name":item.name)
        return jsonify(allstars=[{'name' : star.name,
                                  'cx' : star.body.coordX,
                                  'cy' : star.body.coordY} for star in stars])
    return redirect(url_for('login'))

@app.route('/api/stars/<int:star_id>')
def api_star(star_id):
    if 'user' in session:
        star = Star.query.get(star_id)
        return jsonify(star={'name': star.name,
                'system': star.system.name,
                'cx':star.body.coordX,
                'cy':star.body.coordY,
                'mass':star.body.mass}
                )
    return noUser

@app.route('/api/leaders/')
def api_persons():
    if 'user' in session:
        query = Person.query
        persons = query.all()
        return jsonify(persons=[{'person' : {'firstname' : person.firstname,
                                  'surename' : person.surename,
                                  'stren' : person.stren }} for person in persons])
    return redirect(url_for('login'))

@app.route('/api/imperiums/')
def api_imperiums():
    if 'user' in session:
        query = Person.query
        persons = query.all()
        #for item in stars:
        #    data.add("name":item.name)
        return jsonify(persons=[{'person' : {'firstname' : person.firstname,
                                  'surename' : person.surename,
                                  'stren' : person.stren }} for person in persons])
    return redirect(url_for('login'))


@app.route('/api/systems/', methods=["GET", "POST"])
def systems():
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
            for planet in system.planets:
                xplanet = ET.SubElement(xsystem, "planet")
                plident = ET.SubElement(xplanet, "id")
                plident.text = str(planet.id)
                plname = ET.SubElement(xplanet, "name")
                plname.text = str(planet.name)
                mass = ET.SubElement(xplanet, "mass")
                mass.text = str(planet.body.mass)
        return jsonify(systems=[{'system' : {'star' : { 'name' : star.name,
                                  'cx' : star.body.coordX,
                                  'cy' : star.body.coordY,
                                  'mass' : star.body.mass } } for star in system.stars } for system in systems])
    return redirect(url_for('login'))


#old XML part wich is used by current GUI demo
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
            for planet in system.planets:
                xplanet = ET.SubElement(xsystem, "planet")
                plident = ET.SubElement(xplanet, "id")
                plident.text = str(planet.id)
                plname = ET.SubElement(xplanet, "name")
                plname.text = str(planet.name)
                mass = ET.SubElement(xplanet, "mass")
                mass.text = str(planet.body.mass)
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
        planets = ET.SubElement(root, "planets")
        for planet in star.system.planets:
                xplanet = ET.SubElement(planets, "planet")
                plident = ET.SubElement(xplanet, "id")
                plident.text = str(planet.id)
                plname = ET.SubElement(xplanet, "name")
                plname.text = str(planet.name)
                platm = ET.SubElement(xplanet, "atmo")
                platm.text = str(planet.atmosphere)
                cx = ET.SubElement(xplanet, "cx")
                cx.text = str(planet.body.coordX)
                cy = ET.SubElement(xplanet, "cy")
                cy.text = str(planet.body.coordY)
                platm = ET.SubElement(xplanet, "mass")
                platm.text = str(planet.body.mass)
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
        crew = ET.SubElement(xship, "crew")
        for person in ship.personel:
            member = ET.SubElement(crew, "person")
            member.text = str(person.firstname)
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

# a route for generating sitemap.xml
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
      """Generate sitemap.xml. Makes a list of urls and date modified."""
      pages=[]
      ten_days_ago=(datetime.datetime.now() - datetime.timedelta(days=10)).date().isoformat()
      # static pages
      for rule in app.url_map.iter_rules():
          if "GET" in rule.methods and len(rule.arguments)==0:
              pages.append(
                           [rule.rule,ten_days_ago]
                           )

      # user model pages
      #users=User.query.order_by(User.modified_time).all()
      #for user in users:
    #       url=url_for('user.pub',name=user.name)
    #      modified_time=user.modified_time.date().isoformat()
    #      pages.append([url,modified_time])

      sitemap_xml = render_template('sitemap.xml', pages=pages)
      #response= make_response(sitemap_xml)
      #response.headers["Content-Type"] = "application/xml"

      #return response
      return sitemap_xml

app.secret_key = 'sjadiojapoqmwdm,ciowqewqjmdplkasm902348927ru9weojmc'
