# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from app import app, db, postreciver
from models import Game, Ship, Faction, Body, Star
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

@app.route('/ships')
def api_ships():
    if 'user' in session:
        shipquery = Ship.query.filter(Ship.body!=None)
        ships = shipquery.all()
        return jsonify(ships=[{'name' : ship.name, 'faction' : ship.faction.name } for ship in ships])
    return ""


#@app.route('/api/stars')
#def api_stars():
#    if 'user' in session:
#        starquery = Star.query
#        stars = starquery.all()
#        return jsonify(stars=[{'name' : star.name, 'x' : star.coo} for star in stars])
#    return ""

@app.route('/stars')
def api_stars():
    if 'user' in session:
        query = Star.query
        stars = query.all()
        #for item in stars:
        #    data.add("name":item.name)
        return jsonify(allstars=[{'name' : star.name, 'cx' : star.body.coordX, 'cy' : star.body.coordY} for star in stars])
    return redirect(url_for('login'))

@app.route('/stars.xml', methods=["GET", "POST"])
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

@app.route('/star<int:star_id>.xml', methods=["GET", "POST"])
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

@app.route('/imperium.xml', methods=["GET", "POST"])
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
