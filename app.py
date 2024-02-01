from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from routes.test import TestRoutes
# from routes.main import MainRoutes
from routes.root import MainRoutes

from db import DB, Account

session = DB.get_session()
# RealTime Stuff ----------------------------------------
app = Flask(__name__)
socketio = SocketIO()
# socketio = SocketIO(app)


# app.register_blueprint(root_bp)
app.register_blueprint(MainRoutes(name='root', import_name=__name__, session=session, socketio=socketio), url_prefix='/')
# app.register_blueprint(MainRoutes(name='root', import_name=__name__, session=session, socketio=socketio), url_prefix='/')

# app.register_blueprint(MainRoutes(name='main', import_name=__name__, session=session, socketio=socketio), url_prefix='/')
# app.register_blueprint(TestRoutes(name='test', import_name=__name__, session=session, socketio=socketio), url_prefix='/test')

@socketio.on('update_accounts')
def handle_update_accounts():
    accounts = session.query(Account).all()
    socketio.emit('refresh_accounts', {'accounts': accounts})

if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True)