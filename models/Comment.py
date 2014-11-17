from models import db
from models.Post import Post
import time

class Comment(db.Model):

  __tablename__ = 'Comment'

  Id = db.Column(db.Integer, primary_key = True)
  Post = db.Column(db.Integer, db.ForeignKey(Post.Id))
  Comment = db.Column(db.Text)
  Email = db.Column(db.String(45), unique=True)
  Nick = db.Column(db.String(6))
  DateCreated = db.Column(db.DateTime)
   
  def __init__(self, nick, email, comment, post):


    self.Post = post
    self.Comment = comment
    self.Email = email
    self.Nick = nick
    self.DateCreated = time.strftime('%Y-%m-%d %H:%M:%S')