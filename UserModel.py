from DB import *

import appconfig
import datetime
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
class UserModel:

    def __init__(self):
        self.cryptkey = appconfig.CRYPT_KEY


    def login(self, email, password):

        db = DB()
        sql = '''SELECT
                      u.Email as email,
                      u.Role as role,
                      u.Nick as nick,
                      u.Password as password,
                      u.Id as Id

                      FROM User u
                         WHERE u.Email=%s'''


        query = db.query(sql, (email, ))
        user = query.fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session['auth'] = user
            return True
        return False


    def register(self, email, password, nick, role):


        db = DB()
        sql = '''INSERT INTO User (Id, Nick, Email, Role, Password) VALUES (NULL, %s, %s, %s, %s) '''
        db.query(sql, (nick, email, role, generate_password_hash(password)))
        db.conn.commit()
        #Todo add send email method