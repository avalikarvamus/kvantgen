# -*- coding: utf-8 -*-
#
#    Copyright 2014 Madis Veskimeister <madis@pingviinitiivul.ee>
#

from flask import Flask
from app import app, db
from datetime import datetime
from sqlalchemy.orm import relationship, backref

class Faction(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=True)
    race        = db.Column(db.String(), unique=True, nullable=True)

class Player(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=True)
    time_added_to_base = db.Column(db.DateTime(timezone=True), default=db.func.now())
    faction_id  = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=False)
    faction     = db.relationship("Faction", backref="player", lazy="joined")

class Body(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    coordX      = db.Column(db.Float)
    coordY      = db.Column(db.Float)

class Star(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    body_id     = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body        = db.relationship('Body', uselist=False, backref=db.backref('star', uselist=False), lazy='joined')

class Planet(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    body_id     = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body        = db.relationship('Body', uselist=False, backref=db.backref('planet', uselist=False), lazy='joined')

class Ship(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
    faction_id  = db.Column(db.Integer, db.ForeignKey('faction.id'), nullable=False)
    faction     = db.relationship("Faction", backref="ships", lazy="joined")
    body_id     = db.Column(db.Integer, db.ForeignKey('body.id'), nullable=False, index=True, unique=True)
    body        = db.relationship('Body', uselist=False, backref=db.backref('ship', uselist=False), lazy='joined')


class Game(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(), unique=True, nullable=False)
