from werkzeug import generate_password_hash, check_password_hash

from models import db

class User(db.Model):

  __tablename__ = 'User'
  Id = db.Column(db.Integer, primary_key = True)
  Nick = db.Column(db.String(45))
  Email = db.Column(db.String(45), unique=True)
  Role = db.Column(db.String(6))
  Password = db.Column(db.String(255))
   
  def __init__(self, nick, email, role, password):


    self.Nick = nick.title()
    self.Email = email.lower()
    self.Role = role.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.Password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.Password, password)