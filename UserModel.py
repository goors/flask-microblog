from flask import session
class UserModel:

    def __init__(self):

        from models import Tag
        from models import  Post
        from models import  User

        self.Tag = Tag.Tag
        self.Post = Post.Post
        self.User = User.User

    def login(self, email, password):


        user = self.User.query.filter_by(Email = email).first()
        if user and user.check_password(password):

            session['email'] = user.Email
            session['nick'] = user.Nick
            session['Id'] = user.Id
            return True
        return False



    def register(self, email, password, nick, role, id = None):
        from models import db
        newuser = self.User(nick, email, role, password)
        if id:
            u = self.User.query.filter_by(Id=id).first()
            u.Email = email
            u.Role = role
            u.set_password(password)
            u.Nick = nick

        else:
            db.session.add(newuser)
        res = db.session.commit()
        print res


    def list(self):

        users = self.User.query.all()
        if users:
            return  users
        return False

    def getUser(self, id):

        user = self.User.query.filter_by(Id=id).first()

        if user:
            return  user
        return False