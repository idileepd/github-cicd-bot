# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from sqlalchemy.orm import Session
from db import Account
from secure import Secure

class MainRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    def __init__(self, name:str, import_name:str, session:Session , socketio: SocketIO):
        super().__init__(name, import_name)
        self.socketio = socketio
        self.session = session

        @self.route('/')
        def index():
            accounts = self.session.query(Account).all()
            return render_template('root/index.html', accounts=accounts)
        
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

                # refresh if any user listening
                accounts = session.query(Account).all()
                socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

                return redirect(url_for('root.index'))


            return render_template('root/create.html')


        @self.route('/update/<string:account_id>', methods=['GET', 'POST'])
        def update(account_id):
            try:
                account = self.session.query(Account).filter_by(accountId=account_id).one()

                if request.method == 'POST':
                    # Update account information
                    account.name = request.form['name']
                    account.gitToken = request.form['git_token']
                    self.session.commit()

                    # refresh if any user listening
                    accounts = session.query(Account).all()
                    socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

                    return redirect(url_for('root.index'))

                return render_template('root/update.html', account=account)
            except Exception as e:
                return 'Account not found', 404
            
        @self.route('/delete/<string:account_id>', methods=['GET', 'POST'])
        def delete(account_id):
            try:
                account = self.session.query(Account).filter_by(accountId=account_id).one()

                if request.method == 'POST':
                    # Delete the account
                    self.session.delete(account)
                    self.session.commit()

                    # refresh if any user listening
                    accounts = session.query(Account).all()
                    socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

                    return redirect(url_for('root.index'))

                return render_template('root/delete.html', account=account)
            except Exception as e:
                return 'Account not found', 404