# routes/main_routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_socketio import SocketIO
from sqlalchemy.orm import Session
from db import Account, Repository
from secure import Secure


# "account/"
class AccountRoutes(Blueprint):
    socketio:SocketIO
    session: Session
    
    # account/ - all accounts
    # account/id/
    # account/create
    def __init__(self, name:str, import_name:str, session:Session , socketio: SocketIO):
        super().__init__(name, import_name)
        self.socketio = socketio
        self.session = session

        @self.route('/')
        def all_accounts():
            accounts = self.session.query(Account).all()
            return render_template('account/all_accounts.html', accounts=accounts)
        
        # @self.route('/<string:id>')
        # def child_2(id):
        #     return f'Hello from the child blueprint! Additional data: ? {id}'
        
        @self.route('/<string:account_id>')
        def account(account_id):
            print("acc id", account_id)
            try:
                account = self.session.query(Account).filter_by(accountId=account_id).first()
                if account==None:
                    raise Exception("Account not found")
                repos = self.session.query(Repository).filter_by(accountId=account_id).all()
                return render_template('account/account.html', repos=repos, account=account)
            except Exception as e:
                print("Err --- &&&")
                print(e)
                print("Err --- &&&")
                return render_template('404.html', message="Account Not Found")




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

                return redirect('/accounts')


            return render_template('account/create.html')


        # @self.route('/<string:account_id>/update', methods=['GET', 'POST'])
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

        #         return render_template('account/update.html', account=account)
        #     except Exception as e:
        #         return 'Account not found', 404
            
        # @self.route('/<string:account_id>/delete', methods=['GET', 'POST'])
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

        #         return render_template('account/delete.html', account=account)
        #     except Exception as e:
        #         return 'Account not found', 404
            


            
        # @self.route('/')
        # def index():
        #     accounts = self.session.query(Account).all()
        #     return render_template('account/all_accounts.html', accounts=accounts)
            


        # @self.route('/id/<string:account_id>')
        # def id(account_id):
        #     try:
        #         account = self.session.query(Account).filter_by(accountId=account_id).one()
        #         repos = self.session.query(Repository).filter_by(accountId=account_id).all()

        #         return render_template('account/id.html', account=account, repos=repos)
        #     except Exception as e:
        #         return render_template('404.html',message="Account not found")
