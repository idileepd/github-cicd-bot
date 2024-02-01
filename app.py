from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from flask_socketio import SocketIO
from routes.root import MainRoutes
from routes.account import AccountRoutes
from db import DB, Account

session = DB.get_session()

# RealTime Stuff ----------------------------------------
app = Flask(__name__)
socketio = SocketIO()

# app.register_blueprint(root_bp)
app.register_blueprint(MainRoutes(name='root', import_name=__name__, session=session, socketio=socketio), url_prefix='/')
app.register_blueprint(AccountRoutes(name='account', import_name=__name__, session=session, socketio=socketio), url_prefix='/accounts')

@socketio.on('update_accounts')
def handle_update_accounts():
    accounts = session.query(Account).all()
    socketio.emit('refresh_accounts', {'accounts': accounts})

if __name__ == '__main__':
    socketio.init_app(app)
    socketio.run(app, debug=True)