#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
from random import randint
from app.models import Faction, System, Star, Planet, Ship, ShipClass, ShipPart, ShipPartClass, Body

def generateGalaxy():
    for i in range(1,100):
        star =  Star('Name '+str(i),
                randint(10, 200),
                randint(10, 200),
                randint(100, 20000))
        system = System(star)
        db.session.add(system)


def fillData():
    generateGalaxy()
    madulased=Faction(name="shshhh",race=u"madulased")
    inimesed=Faction(name="inimesed",race=u"humanoidid")
    db.session.add(madulased)
    engine=ShipPartClass(name="engine")
    ship=Ship(name="Enterprise", faction=inimesed, body=Body(10, 10, 100),
                shipclass=ShipClass(name="Independence"),
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship)
    ship2=Ship(name="dZahadum", faction=madulased, body=Body(100, 120, 100),
                shipclass=ShipClass(name="Gorath"),
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship2)
    db.session.commit()

fillData()
