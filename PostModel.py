
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
        from models.Comment import Comment


        post = db.session.query(Post).get(id)
        comments = Comment.query.filter_by(Post=id).all()
        for c in comments:
            db.session.delete(c)

        self.removefiles(id)
        self.removeimages(id)


        post.tags = []

        db.session.delete(post)
        db.session.commit()





    def getPost(self, id):
        from models.Post import Post

        post = Post.query.filter_by(Id=id).first()


        if post:
            return post
        return False

    def addTags(self, tags, post):


        from models.shared import db
        from models.Post import Post
        from models.Tag import Tag

        postTags = db.session.query(Post).get(post)

        if postTags.tags:
            postTags.tags = []
            db.session.commit()


        for tag in tags:

            t = db.session.query(Tag).get(tag)
            postTags.tags.append(t)
            db.session.add(t)
            db.session.commit()


    def addFiles(self, files, post):


        from models.shared import db
        from models.PostFile import PostFile


        for file in files:

            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            pf = PostFile(post, filename)
            db.session.add(pf)
            db.session.commit()


    def addImages(self, images, post):


        from models.shared import db
        from models.PostImage import PostImage

        from PIL import Image
        import glob, os

        size = 80, 80

        for image in images:

            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            im = Image.open(UPLOAD_FOLDER+filename)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(UPLOAD_FOLDER+"th_"+filename, "JPEG")

            pi = PostImage(post, filename)
            db.session.add(pi)
            db.session.commit()




    def getPostTags(self, id):

        from models.Post import Post

        posts = Post.query.join(Post.tags).filter(Post.Id == id).all()
        if(posts):
            return posts
        return False


    def getPostFiles(self, id):

        from models.PostFile import PostFile

        posts = PostFile.query.filter_by(Post = id).all()
        if(posts):
            return posts
        return False

    def getPostImages(self, id):

        from models.PostImage import PostImage

        posts = PostImage.query.filter_by(Post = id).all()
        if(posts):
            return posts
        return False




    def post(self, slug):
        from models.Post import Post

        post = Post.query.filter_by(Slug=slug).first()

        if post:
            return post
        return False


    def removefile(self, id):

        from models.PostFile import PostFile
        from models.shared import db

        posts = PostFile.query.filter_by(Id = id).all()
        if(posts):
            for p in posts:
                db.session.delete(p)
                os.remove(UPLOAD_FOLDER+p.FileName)
                os.remove(UPLOAD_FOLDER+"th_"+p.FileName)
            db.session.commit()
        return False


    def removeimage(self, id):

        from models.PostImage import PostImage
        from models.shared import db

        posts = PostImage.query.filter_by(Id = id).all()
        if(posts):
            for p in posts:
                db.session.delete(p)
                os.remove(UPLOAD_FOLDER+p.ImageName)
                os.remove(UPLOAD_FOLDER+"th_"+p.ImageName)
            db.session.commit()
        return False


    def removefiles(self, post):

        from models.PostFile import PostFile
        from models.shared import db

        posts = PostFile.query.filter_by(Post = post).all()
        if(posts):
            for p in posts:
                db.session.delete(p)
                os.remove(UPLOAD_FOLDER+p.FileName)
                os.remove(UPLOAD_FOLDER+"th_"+p.FileName)
            db.session.commit()
        return False


    def removeimages(self, post):

        from models.PostImage import PostImage
        from models.shared import db

        posts = PostImage.query.filter_by(Post = post).all()
        if(posts):
            for p in posts:

                db.session.delete(p)
                os.remove(UPLOAD_FOLDER+"th_"+p.ImageName)
            db.session.commit()
        return False


