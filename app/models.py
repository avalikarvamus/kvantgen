# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from app import app, db
from datetime import datetime
from sqlalchemy.orm import relationship, backref

shippartowners = db.Table('shippartowners',
                                    db.Column('ship.id', db.Integer,
                                              db.ForeignKey('ship.id')),
                                    db.Column(
                                        'shippart.id',
                                        db.Integer,
                                        db.ForeignKey('shippart.id'))
                                    )

class Faction(db.Model):
    __tablename__    = 'faction'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=True)
    race        = db.Column(db.String(), unique=True, nullable=True)

class Player(db.Model):
    __tablename__    = 'player'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=True)
    time_added_to_base = db.Column(db.DateTime(timezone=True), default=db.func.now())
    faction_id  = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=False)
    faction     = db.relationship("Faction", backref="player", lazy="joined")

class Body(db.Model):
    __tablename__    = 'body'
    id          = db.Column(db.Integer, primary_key=True)
    coordX      = db.Column(db.Float)
    coordY      = db.Column(db.Float)
    mass        = db.Column(db.Float)

    def __init__(self, coordX, coordY, mass):
        self.coordX = coordX
        self.coordY = coordY
        self.mass   = mass

class Star(db.Model):
    __tablename__    = 'star'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    body_id     = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body        = db.relationship('Body', uselist=False, backref=db.backref('star', uselist=False), lazy='joined')

    def __init__(self, name, coordX, coordY, mass):
        self.name = name;
        self.body = Body(coordX, coordY, mass);


    def serialize(self):
        return {
            self.name : {
                'cX': str(self.body.coordX),
                'cY': str(self.body.coordY)
            }
        }

class Planet(db.Model):
    __tablename__    = 'planet'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    body_id     = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body        = db.relationship('Body', uselist=False, backref=db.backref('planet', uselist=False), lazy='joined')
    star_id     = db.Column(db.Integer, db.ForeignKey('star.id'), nullable=False, index=True, unique=True)
    star        = db.relationship('Star', backref=db.backref('star'), lazy='joined')


class ShipClass(db.Model):
    __tablename__    = 'shipclass'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    #ships       = db.relationship("Ship", backref="shipclass", lazy="dynamic")

class ShipPartClass(db.Model):
    __tablename__    = 'shippartclass'
    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(), unique=True, nullable=False)

class ShipPart(db.Model):
    __tablename__    = 'shippart'
    id               = db.Column(db.Integer, primary_key=True)
    shippartclass_id = db.Column(db.Integer, db.ForeignKey('shippartclass.id'), nullable=False)
    shippartclass    = db.relationship('ShipPartClass', backref=db.backref('shippart', uselist=False), lazy='joined')
    maxstructure     = db.Column(db.Integer, default=0)
    curstructure     = db.Column(db.Integer, default=0)
    
    #def __init__(self):
	#	self.maxstructure = 0
	#	self.curstructure = 0
		

class Ship(db.Model):
    __tablename__    = 'ship'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(), unique=True, nullable=False)
    faction_id   = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=False)
    faction      = db.relationship("Faction", backref="ships", lazy="joined")
    body_id      = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body         = db.relationship('Body', uselist=False, backref=db.backref('ship', uselist=False), lazy='joined')
    shipclass_id = db.Column(db.Integer, db.ForeignKey('shipclass.id'), nullable=False, index=True, unique=True)
    shipclass    = db.relationship('ShipClass', backref=db.backref('ship', uselist=False), lazy='joined')
    #ship parts#
    shipparts    = db.relationship("ShipPart", backref="ship", secondary="shippartowners", lazy="dynamic")

    @property
    def maxstructure(self):
        maxstr = 0
        for part in self.shipparts:
			if part.maxstructure is not None:
				maxstr = maxstr + part.maxstructure
        return maxstr

    @property
    def curstructure(self):
        curstr = 0
        for part in self.shipparts:
			if part.curstructure is not None:
				curstr = curstr + part.curstructure
        return curstr

    @property
    def condition(self):
		curstr = self.curstructure
		maxstr = self.maxstructure
		if curstr > 0 and maxstr > 0:
			return curstr / maxstr * 100
		else :
			return 0

class Game(db.Model):
    __tablename__    = 'game'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
