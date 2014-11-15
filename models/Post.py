from werkzeug import generate_password_hash, check_password_hash

from shared import db
import time
from User import  User
from Tag import  Tag


tags = db.Table('PostTag',
    db.Column('Tag', db.Integer, db.ForeignKey('Tag.Id')),
    db.Column('Post', db.Integer, db.ForeignKey('Post.Id'))
)


class Post(db.Model):

  __tablename__ = 'Post'
  Id = db.Column(db.Integer, primary_key = True)
  Title = db.Column(db.String(128))
  DateCreated = db.Column(db.DateTime)
  DateModified = db.Column(db.DateTime)
  Content = db.Column(db.Text)
  Photo = db.Column(db.String(45))

  Slug = db.Column(db.String(45))
  NoOfViews = db.Column(db.Integer)
  PostStatus = db.Column(db.Enum("0", "1"))
  User = db.Column(db.Integer, db.ForeignKey(User.Id))
  tags = db.relationship("Tag", secondary=tags)

  def __init__(self, title, content, photo, user, slug, status, noofviews):


    self.Title = title
    self.Content = content
    self.Photo = photo
    self.User = user
    self.NoOfViews = noofviews
    self.Slug = slug

    self.PostStatus = status
    self.DateCreated = time.strftime('%Y-%m-%d %H:%M:%S')
    self.DateModified = time.strftime('%Y-%m-%d %H:%M:%S')

     
