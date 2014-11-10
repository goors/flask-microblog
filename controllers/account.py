
from UserModel import *
from flask import Blueprint, render_template, session, redirect, url_for, request

account_api = Blueprint('account_api', __name__)


@account_api.route('/admin/login', methods=['POST','GET'])
def login():

    if session:
        return redirect("/admin")

    error = ""

    if 'email' in request.form and 'password' in request.form:

        model = UserModel()
        if(model.login(request.form['email'], request.form['password'])):
            #url_for('admin') -> not working
            return redirect("/admin")
        error = "Error. Either something is missing from filed or user/pass is wrong."

    return render_template('admin/login.html', error=error)

@account_api.route('/admin/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/admin/login")


