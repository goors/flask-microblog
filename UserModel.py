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


    def register(self, email, password, nick, role, id = None):


        db = DB()
        if id:
            sql = '''UPDATE User set Nick=%s, Email=%s, Role=%s, Password=%s '''
        else:
            sql = '''INSERT INTO User (Id, Nick, Email, Role, Password) VALUES (NULL, %s, %s, %s, %s) '''

        q = db.query(sql, (nick, email, role, generate_password_hash(password)))
        db.conn.commit()
        #Todo add send email method
        return q.lastrowid

    def list(self):
        db = DB()
        sql = '''SELECT * FROM User '''

        query = db.query(sql)
        users = query.fetchall()
        db.close()

        if users:
            return  users
        return False

    def getUser(self, id):
        db = DB()
        sql = '''SELECT * FROM User WHERE Id=%s'''

        query = db.query(sql, (id,))
        user = query.fetchone()
        db.close()

        if user:
            return  user
        return False