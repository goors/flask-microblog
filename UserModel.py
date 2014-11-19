from flask import session
from appconfig import *


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

        if id:
            u = self.User.query.filter_by(Id=id).first()
            u.Email = email
            u.Role = role
            u.set_password(password)
            u.Nick = nick
            subject = "You account is updated"

        else:
            u = self.User(nick, email, role, password)
            db.session.add(u)
            subject = "Account is created"

        res = db.session.commit()
        body = "<p>Hello "+nick+", </p> <p>Your login details for "+URL+" :</p> <p>Username: "+email+" <br />Password: "+password+"</p>"
        self.send_email(subject, email, body, nick)
        return u.Id


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

    def send_email(self, subject, recipients, html_body, nick):
        import mandrill
        try:
            mandrill_client = mandrill.Mandrill('ajQ8I81AVELYSYn--6xbmw')
            message = {
             'from_email': ADMINS[0],
             'from_name': 'Blog admin',
             'headers': {'Reply-To': ADMINS[0]},
             'html': html_body,
             'important': True,
             'subject': subject,
             'to': [{'email': recipients,
                     'name': nick,
                     'type': 'to'}],
             }
            result = mandrill_client.messages.send(message=message, async=False)
            '''
            [{'_id': 'abc123abc123abc123abc123abc123',
              'email': 'recipient.email@example.com',
              'reject_reason': 'hard-bounce',
              'status': 'sent'}]
            '''

        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
            raise