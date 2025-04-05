from flask import Flask
from public import public
from admin import admin
# from user import user
from doctors import doctors

from api import api

web=Flask(__name__)

web.secret_key='remainssecret'

web.register_blueprint(public)
web.register_blueprint(admin,url_prefix='/')
# app.register_blueprint(user,url_prefix='/user')

web.register_blueprint(api,url_prefix='/api')
web.register_blueprint(doctors,url_prefix='/doctors')
web.run(debug=True,port=5537,host="0.0.0.0")