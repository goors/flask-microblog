from flask import session
from werkzeug import secure_filename
import os
import CommentModel
UPLOAD_FOLDER = 'static/files/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class PostModel:
    def __init__(self):

        from models import Tag
        from models import Post
        from models import User
        from models import Comment
        from models import PostFile
        from models import PostImage


        self.Tag = Tag.Tag
        self.Post = Post.Post
        self.User = User.User
        self.Comment = Comment.Comment
        self.Comment = Comment.Comment
        self.PostImage = PostImage.PostImage
        self.PostFile = PostFile.PostFile


    def posts(self, fe=None, tag=None):

        if fe:
            return self.Post.query.filter_by(PostStatus='1').order_by(self.Post.Id.desc()).all()

        elif tag:
            return self.Post.query.join(self.Post.tags).filter(self.Tag.Id == tag).all()
        else:
            return self.Post.query.all()


    def addPost(self, title, slug, content, file, active, id=None):

        from models import db

        if file:
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            p = self.getPost(id)

            filename = p.Photo

        if (id):

            p = self.Post.query.filter_by(Id=id).first()
            p.Title = title
            p.Slug = slug
            p.Content = content
            p.Photo = filename
            p.PostStatus = active
            db.session.commit()

        else:

            p = self.Post(title, content, filename, session['Id'], slug, active, 0)
            db.session.add(p)
            db.session.commit()


        # todo return something
        return p.Id

    def deletePost(self, id):

        from models import db


        post = db.session.query(self.Post).get(id)
        comments = self.Comment.query.filter_by(Post=id).all()
        for c in comments:
            db.session.delete(c)

        self.removefiles(id)
        self.removeimages(id)

        post.tags = []

        db.session.delete(post)
        db.session.commit()


    def getPost(self, id):

        post = self.Post.query.filter_by(Id=id).first()

        if post:
            return post
        return False

    def addTags(self, tags, post):

        from models import db

        postTags = db.session.query(self.Post).get(post)

        if postTags.tags:
            postTags.tags = []
            db.session.commit()

        for tag in tags:
            t = db.session.query(self.Tag).get(tag)
            postTags.tags.append(t)
            db.session.add(t)
            db.session.commit()


    def addFiles(self, files, post):


        from models import db

        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            pf = self.PostFile(post, filename)
            db.session.add(pf)
            db.session.commit()


    def addImages(self, images, post):

        from models import db
        import os


        for image in images:



            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))

            self.generateImage(80, 80, filename, "th_")
            self.generateImage(400, 400, filename, "gallery_")

            '''im = Image.open(UPLOAD_FOLDER + filename)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(UPLOAD_FOLDER + "th_" + filename, "JPEG")'''

            pi = self.PostImage(post, filename)
            db.session.add(pi)
            db.session.commit()


    def getPostTags(self, id):


        posts = self.Post.query.join(self.Post.tags).filter(self.Post.Id == id).all()
        if (posts):
            return posts
        return False


    def getPostFiles(self, id):


        posts = self.PostFile.query.filter_by(Post=id).all()
        if (posts):
            return posts
        return False

    def getPostImages(self, id):


        posts = self.PostImage.query.filter_by(Post=id).all()
        if (posts):
            return posts
        return False


    def post(self, slug):

        post = self.Post.query.filter_by(Slug=slug).first()

        if post:
            return post
        return False


    def removefile(self, id):

        from models import db

        posts = self.PostFile.query.filter_by(Id=id).all()
        if (posts):
            for p in posts:
                db.session.delete(p)
                if os.path.isfile(UPLOAD_FOLDER + p.FileName):
                    os.remove(UPLOAD_FOLDER + p.FileName)
            db.session.commit()
        return False


    def removeimage(self, id):

        from models import db

        posts = self.PostImage.query.filter_by(Id=id).all()
        if (posts):
            for p in posts:
                db.session.delete(p)
                if os.path.isfile(UPLOAD_FOLDER + p.ImageName) and os.path.isfile(UPLOAD_FOLDER + "th_"+p.ImageName) and os.path.isfile(UPLOAD_FOLDER + "gallery_"+p.ImageName):
                    os.remove(UPLOAD_FOLDER + p.ImageName)
                    os.remove(UPLOAD_FOLDER + "th_" + p.ImageName)
                    os.remove(UPLOAD_FOLDER + "gallery_" + p.ImageName)
            db.session.commit()
        return False


    def removefiles(self, post):

        from models import db

        posts = self.PostFile.query.filter_by(Post=post).all()
        if (posts):
            for p in posts:
                db.session.delete(p)
                if os.path.isfile(UPLOAD_FOLDER + p.FileName):
                    os.remove(UPLOAD_FOLDER + p.FileName)
                os.remove(UPLOAD_FOLDER + p.FileName)
            db.session.commit()
        return False


    def removeimages(self, post):

        from models import db

        posts = self.PostImage.query.filter_by(Post=post).all()
        if (posts):
            for p in posts:
                db.session.delete(p)
                if os.path.isfile(UPLOAD_FOLDER + p.ImageName) and os.path.isfile(UPLOAD_FOLDER + "th_"+p.ImageName) and os.path.isfile(UPLOAD_FOLDER + "gallery_"+p.ImageName):
                    os.remove(UPLOAD_FOLDER + p.ImageName)
                    os.remove(UPLOAD_FOLDER + "th_" + p.ImageName)
                    os.remove(UPLOAD_FOLDER + "gallery_" + p.ImageName)
            db.session.commit()
        return False

    def getNumberOfComments(self, post):
        commentsNo = self.Comment.query.filter_by(Post=post).count()

        if commentsNo:
            return commentsNo
        return 0

    def generateImage(self, size_w, size_h, filename, ex):

        from PIL import Image

        size = size_w, size_h

        im = Image.open(UPLOAD_FOLDER + filename)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(UPLOAD_FOLDER + ex + filename, "JPEG")



