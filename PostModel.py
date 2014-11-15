from DB import *

import appconfig
import datetime
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug import secure_filename
import os
import time

UPLOAD_FOLDER = 'static/files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class PostModel:



    def posts(self, fe = None, tag = None):

        from models.Post import Post
        from models.Tag import Tag

        if fe:
            return Post.query.order_by(Post.Id.desc()).all()

        elif tag:
            return Post.query.join(Post.tags).filter(Tag.Id == tag).all()
        else:
            return Post.query.all()



    def addPost(self, title, slug, content, file, active, id=None):



        if file:
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            p = self.getPost(id)

            filename = p.Photo


        if(id):

            from models.shared import db
            from models.Post import Post

            p = Post.query.filter_by(Id=id).first()
            p.Title = title
            p.Slug = slug
            p.Content = content
            p.Photo = filename
            p.PostStatus = active
            db.session.commit()




        else:


            from models.shared import db
            from models.Post import Post

            p = Post(title, content, filename, session['Id'], slug, active, 0)
            db.session.add(p)
            db.session.commit()


        #todo return something
        return  p.Id

    def deletePost(self, id):

        from models.shared import db
        from models.Post import Post


        sql = 'DELETE FROM PostTag WHERE Post='+id
        db.engine.execute(sql)
        


        singlepost = Post.query.filter_by(Id=id).first()
        if singlepost:
            db.session.delete(singlepost)
            db.session.flush()



    def getPost(self, id):
        from models.Post import Post

        post = Post.query.filter_by(Id=id).first()


        if post:
            return post
        return False

    def addTags(self, tags, post):


        from models.shared import db

        sql = 'DELETE FROM PostTag WHERE Post='+post
        db.engine.execute(sql)
        db.session.commit()

        for tag in tags:


            sql = 'INSERT INTO PostTag VALUES  (%s, %s)'
            db.engine.execute(sql, (tag, post, ))
            db.session.commit()




    def getPostTags(self, id):

        from models.Post import Post

        posts = Post.query.join(Post.tags).filter(Post.Id == id).all()
        if(posts):
            return posts
        return False




    def post(self, slug):
        from models.Post import Post

        post = Post.query.filter_by(Slug=slug).first()


        if post:
            return post
        return False


