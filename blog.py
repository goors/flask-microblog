import os
from flask import Flask
from controllers import account 
from controllers import static
from controllers import admin
from controllers import fe
from appconfig import *
from flask.ext.compress import Compress

account_api = account.account_api
static_api = static.static_api
admin_api = admin.admin_api
fe = fe.fe

app = Flask(__name__)
Compress(app)
app.register_blueprint(account_api)
app.register_blueprint(static_api)
app.register_blueprint(admin_api)
app.register_blueprint(fe)

app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+USER+':'+PASS+'@'+HOST+'/'+DATABASE

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='0209012'
    )
)
app.config.from_envvar("APP_SETTINGS", silent=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
