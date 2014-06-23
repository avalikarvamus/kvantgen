#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from app.config import SQLALCHEMY_DATABASE_URI
from app import db
import os.path
from app.models import Faction, Star, Planet, Ship, Body

def fillData():
    madulased=Faction(name="shshhh",race=u"madulased")
    inimesed=Faction(name="inimesed",race=u"humanoidid")
    db.session.add(madulased)
    ship=Ship(name="Enterprise", faction=inimesed, body=Body(coordX=10, coordY=10))
    db.session.add(ship)
    db.session.commit()

fillData()
