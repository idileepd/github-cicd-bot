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
        addRepoUrls(self,session,socketio)
        addAccountUrls(self,session,socketio)
        


def addRepoUrls(self,session,socketio):
    @self.route('/<string:account_id>/repos/<string:repo_id>')
    def repo_details(account_id, repo_id):
        account = self.session.query(Account).filter_by(accountId=account_id).first()
        repo = self.session.query(Repository).filter_by(repoId=repo_id).first()
        return render_template('account/repo_details.html',account=account,repo=repo)

    @self.route('/<string:account_id>/repos/create',methods=['GET', 'POST'])
    def create_repo(account_id):
        print("----",request.method)
        print(account_id)
        try:
            account = self.session.query(Account).filter_by(accountId=account_id).first()
            print(account)
            if account==None:
                raise Exception("Account not found")
            if request.method == 'POST':
                repoId = request.form['repoId']
                accountId = account_id
                preStartScript = request.form['preStartScript']
                startScript = request.form['startScript']
                env = request.form['env']
                checkoutLogs = ""
                preStartLogs = ""
                startLogs = ""
                allLogs = ""


                # Create new Account instance
                newRepo = Repository(accountId=accountId,repoId=repoId,preStartScript=preStartScript,startScript=startScript,env=env,checkoutLogs=checkoutLogs,preStartLogs=preStartLogs,startLogs=startLogs,allLogs=allLogs)

                # Add to the database
                self.session.add(newRepo)
                self.session.commit()

                # refresh if any user listening
                repos = session.query(Repository).filter_by(accountId=accountId).all()
                socketio.emit(f'{accountId}/refresh', {'repos': [repo.get_json() for repo in repos]})

                return redirect(f'/accounts/{accountId}')
            print("cool")
            return render_template('account/create_repo.html', account=account)
        except Exception as e:
            print(e)
            return render_template('404.html', message="Account Not Found")


def addAccountUrls(self,session,socketio):
    @self.route('/')
    def all_accounts():
        accounts = self.session.query(Account).all()
        return render_template('account/all_accounts.html', accounts=accounts)
    
    # @self.route('/<string:id>')
    # def child_2(id):
    #     return f'Hello from the child blueprint! Additional data: ? {id}'
    
    @self.route('/<string:account_id>')
    def account(account_id):
        try:
            account = self.session.query(Account).filter_by(accountId=account_id).first()
            if account==None:
                raise Exception("Account not found")
            repos = self.session.query(Repository).filter_by(accountId=account_id).all()
            return render_template('account/account.html', repos=repos, account=account)
        except Exception as e:
            print(e)
            return render_template('404.html', message="Account Not Found")
        
    
    @self.route('/create', methods=['GET', 'POST'])
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


    @self.route('/<string:account_id>/update', methods=['GET', 'POST'])
    def update(account_id):
        try:
            account = self.session.query(Account).filter_by(accountId=account_id).one()
            if account==None:
                raise Exception("Account not found")

            if request.method == 'POST':
                # Update account information
                account.name = request.form['name']
                account.gitToken = request.form['git_token']
                self.session.commit()

                # refresh if any user listening
                accounts = session.query(Account).all()
                socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

                return redirect('/accounts')

            return render_template('account/update.html', account=account.get_json())
        except Exception as e:
            print(e)
            return 'Account not found', 404
        
    @self.route('/<string:account_id>/delete', methods=['GET', 'POST'])
    def delete(account_id):
        try:
            account = self.session.query(Account).filter_by(accountId=account_id).one()
            if account==None:
                raise Exception("Account not found")

            if request.method == 'POST':
                # Delete the account
                self.session.delete(account)
                self.session.commit()

                # refresh if any user listening
                accounts = session.query(Account).all()
                socketio.emit('refresh_accounts', {'accounts': [acc.get_json() for acc in accounts]})

                return redirect('/accounts')

            return render_template('account/delete.html', account=account)
        except Exception as e:
            return 'Account not found', 404
        