#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
import math.randint
from app.models import Faction, Star, Planet, Ship, ShipClass, ShipPart, ShipPartClass, Body

#def generateGalaxy():
#    for i in range(1,100):
#        db.session.add(Star('name '+i))


def fillData():
    madulased=Faction(name="shshhh",race=u"madulased")
    inimesed=Faction(name="inimesed",race=u"humanoidid")
    db.session.add(madulased)
    ship=Ship(name="Enterprise", faction=inimesed, body=Body(coordX=10, coordY=10),
                shipclass=ShipClass(name="Independence"),
                shipparts=[ShipPart(shippartclass=ShipPartClass(name="engine"))])
    db.session.add(ship)
    db.session.commit()

fillData()
