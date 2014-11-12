#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
from random import randint
from app.models import (Faction, System, Star, Planet, Ship, ShipClass,
                        ShipPart, ShipPartClass, Body, Atmosphere)


def generateGalaxy():
#    for i in range(1,100):
    atms = []
    atms.append(Atmosphere("oxygen", 23.4))
    atms.append(None)
    for i in range(1, 100):
        star = Star('Name ' + str(i),
               randint(1, 100),
               randint(1, 100),
               randint(100, 20000))
        system = System(star)
        for j in range(1, randint(1, 5)):
            planet = Planet("S" + str(i) +
                    "P" + str(j), star.body.coordX,
                    star.body.coordY,
                    randint(10, 20))
            planet.atmosphere = atms[1]
            system.planets.append(planet)
        db.session.add(system)


def fillData():
    generateGalaxy()
    neutral = Faction(name="", race=u"")
    madulased = Faction(name="shshhh", race=u"madulased")
    inimesed = Faction(name="inimesed", race=u"humanoidid")
    db.session.add(neutral)
    db.session.add(madulased)
    engine = ShipPartClass(name="engine")
    indep = ShipClass(name="Independence")
    ship = Ship(name="Enterprise", faction=inimesed, body=Body(10, 10, 100),
                shipclass=indep,
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship)
    ship1 = Ship(name="Illustrious", faction=inimesed, body=Body(10, 40, 100),
                shipclass=indep,
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship1)
    gorath = ShipClass(name="Gorath")
    ship2 = Ship(name="dZahadum", faction=madulased, body=Body(67, 40, 100),
                shipclass=gorath,
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship2)
    ship3 = Ship(name="dYummy", faction=madulased, body=Body(69, 60, 100),
                shipclass=gorath,
                shipparts=[ShipPart(shippartclass=engine)])
    db.session.add(ship3)
    db.session.commit()

fillData()
