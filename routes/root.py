# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from sqlalchemy.orm import Session
from db import Account
from secure import Secure

# root_bp = Blueprint('root', __name__)

# @root_bp.route('/')
# def index():
#     print("got Route")
#     return render_template('index.html', accounts=[])



class MainRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    def __init__(self, name:str, import_name:str, session:Session , socketio: SocketIO):
        super().__init__(name, import_name)
        self.socketio = socketio
        self.session = session

        @self.route('/')
        def index():
            print("----- > Work !!")
            accounts = self.session.query(Account).all()
            # print(accounts)
            return render_template('index.html', accounts=accounts)
        
        @self.route('/create', methods=['GET', 'POST'], )
        def create():
            if request.method == 'POST':
                # Get form data
                account_id = request.form['account_id']
                name = request.form['name']
                git_token = Secure.encrypt(request.form['git_token'])

                # Create new Account instance
                new_account = Account(accountId=account_id, name=name, gitToken=git_token)

                # Add to the database
                self.session.add(new_account)
                self.session.commit()

                return redirect(url_for('root.index'))


            return render_template('create.html')

