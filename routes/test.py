# routes/user_routes.py
from flask import Blueprint, render_template
from flask_socketio import SocketIO
from sqlalchemy.orm import Session

class TestRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    def __init__(self, name:str, import_name:str, socketio: SocketIO, session:Session):
        super().__init__(name, import_name)
        self.session = session
        self.socketio = socketio

        @self.route('/')
        def child_route():
            return f'Hello from the child blueprint! Additional data: ?'
        
        @self.route('/<string:id>')
        def child_2(id):
            return f'Hello from the child blueprint! Additional data: ? {id}'

