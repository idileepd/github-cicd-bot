# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from sqlalchemy.orm import Session
from db import Account, Repository
from secure import Secure

class RepoRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    def __init__(self, name:str, import_name:str, session:Session , socketio: SocketIO):
        super().__init__(name, import_name)
        self.socketio = socketio
        self.session = session

        @self.route('/')
        def index():
            accounts = self.session.query(Account).all()
            return render_template('repos/index.html', accounts=accounts)
        
        @self.route('/create', methods=['GET', 'POST'], )
        def create():
            if request.method == 'POST':
                # Get form data
                account_id = request.form['account_id']
                repoId = request.form['id']

                # Create new Account instance
                new_repo = Repository(repoId=repoId,accountId=account_id)

                # Add to the database
                self.session.add(new_repo)
                self.session.commit()

                # refresh if any user listening
                repos = session.query(Repository).filter_by(accountId=account_id).all()
                socketio.emit(f"refresh_repos/{account_id}", {'repos': [repos.get_json() for repo in repos]})

                return redirect(f"/account/{account_id}")


            return render_template('root/create.html')


        # @self.route('/update/<string:account_id>', methods=['GET', 'POST'])
        # def update(account_id):
        #     try:
        #         account = self.session.query(Account).filter_by(accountId=account_id).one()

        #         if request.method == 'POST':
        #             # Update account information
        #             account.name = request.form['name']
        #             account.gitToken = request.form['git_token']
        #             self.session.commit()

        #             # refresh if any user listening
        #             accounts = session.query(Account).all()
        #             socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

        #             return redirect(url_for('root.index'))

        #         return render_template('root/update.html', account=account)
        #     except Exception as e:
        #         return 'Account not found', 404
            
        # @self.route('/delete/<string:account_id>', methods=['GET', 'POST'])
        # def delete(account_id):
        #     try:
        #         account = self.session.query(Account).filter_by(accountId=account_id).one()

        #         if request.method == 'POST':
        #             # Delete the account
        #             self.session.delete(account)
        #             self.session.commit()

        #             # refresh if any user listening
        #             accounts = session.query(Account).all()
        #             socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

        #             return redirect(url_for('root.index'))

        #         return render_template('root/delete.html', account=account)
        #     except Exception as e:
        #         return 'Account not found', 404