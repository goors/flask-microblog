from models import db
from models.Post import Post

class PostImage(db.Model):

  __tablename__ = 'PostImage'

  Id = db.Column(db.Integer, primary_key = True)
  Post = db.Column(db.Integer, db.ForeignKey(Post.Id))
  ImageName = db.Column(db.String(128))

  def __init__(self, post, file):


    self.Post = post
    self.ImageName = file
