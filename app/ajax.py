# -*- coding: utf-8 -*-
#
#    Copyright 2013 Madis Veskimeister <madis@pingviinitiivul.ee>
#

import  os, random, exceptions
from flask import render_template, flash, redirect, session, url_for, request, jsonify, json, Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from app import app
from models import Game, Ship, Faction, Body, Star
from flask_restplus import Api, Resource, fields, apidoc

ajax = Blueprint('ajax', __name__,
                        template_folder='templates')

api = Api(app, version='1.0', title='Todo API',
    description='A simple TODO API extracted from the original flask-restful example',
)

ns = api.namespace('ajax', description='Kvantgen API operations')


TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

todo = api.model('Todo', {
    'task': fields.String(required=True, description='The task details')
})

listed_todo = api.model('ListedTodo', {
    'id': fields.String(required=True, description='The todo ID'),
    'todo': fields.Nested(todo, description='The Todo')
})


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        api.abort(404, "API {} doesn't exist".format(todo_id))

parser = api.parser()
parser.add_argument('task', type=str, required=True, help='The task details', location='form')


@ns.route('/<string:todo_id>')
@api.doc(responses={404: 'Not found'}, params={'todo_id': 'The Todo ID'})
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @api.doc(description='todo_id should be in {0}'.format(', '.join(TODOS.keys())))
    @api.marshal_with(todo)
    def get(self, todo_id):
        '''Fetch a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @api.doc(responses={204: 'Todo deleted'})
    def delete(self, todo_id):
        '''Delete a given resource'''
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @api.doc(parser=parser)
    @api.marshal_with(todo)
    def put(self, todo_id):
        '''Update a given resource'''
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.marshal_list_with(listed_todo)
    def get(self):
        '''List all todos'''
        return [{'id': id, 'todo': todo} for id, todo in TODOS.items()]

    @api.doc(parser=parser)
    @api.marshal_with(todo, code=201)
    def post(self):
        '''Create a todo'''
        args = parser.parse_args()
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201
