from shared import db
from models.Post import Post

class PostFile(db.Model):

  __tablename__ = 'PostFile'

  Id = db.Column(db.Integer, primary_key = True)
  Post = db.Column(db.Integer, db.ForeignKey(Post.Id))
  FileName = db.Column(db.String(128))

  def __init__(self, post, file):


    self.Post = post
    self.FileName = file
