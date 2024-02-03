from flask import Blueprint, render_template
from flask_socketio import SocketIO
from sqlalchemy.orm import Session

class MainRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    def __init__(self, name:str, import_name:str, session:Session , socketio: SocketIO):
        super().__init__(name, import_name)
        self.socketio = socketio
        self.session = session

        @self.route('/')
        def index():
            return render_template('index.html')
        
        @self.route('/404')
        def notFound(message=""):
            return render_template('404.html',message=message)
        
