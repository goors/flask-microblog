import appconfig
from flask import session



class UserModel:


    def login(self, email, password):

        from models.User import User
        user = User.query.filter_by(Email = email).first()
        if user and user.check_password(password):

            session['email'] = user.Email
            session['nick'] = user.Nick
            session['Id'] = user.Id
            return True
        return False



    def register(self, email, password, nick, role, id = None):


        from models.User import User
        from models.User import db

        newuser = User(nick, email, role, password)
        if id:
            u = User.query.filter_by(Id=id).first()
            u.Email = email
            u.Role = role
            u.set_password(password)
            u.Nick = nick

        else:
            db.session.add(newuser)
        res = db.session.commit()
        print res


    def list(self):

        from models.User import User
        users = User.query.all()
        if users:
            return  users
        return False

    def getUser(self, id):

        from models.User import User
        user = User.query.filter_by(Id=id).first()


        if user:
            return  user
        return False