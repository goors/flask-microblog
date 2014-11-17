from flask import Blueprint, redirect, render_template, request
from TagModel import *
from PostModel import *
from UserModel import *
from CommentModel import *

fe = Blueprint('fe', __name__)


@fe.route('/tag/<tagname>', methods=['GET'])
def hometags(tagname=None):

    tag = TagModel()
    post = PostModel()
    tagId = tag.getTagByName(tagname)
    return render_template("home/index.html", tags=tag.tags(), posts=post.posts(None, tagId))

@fe.route('/', methods=['GET'])
def home():

    tag = TagModel()
    post = PostModel()
    return render_template("home/index.html", tags=tag.tags(), posts=post.posts(True, None))


@fe.route('/read/<slug>', methods=['GET','POST'])
def read(slug=None):

    from models import db
    tag = TagModel()
    post = PostModel()
    comment = CommentModel()
    id = post.post(slug)

    id.NoOfViews += 1
    db.session.commit()

    postFiles = post.getPostFiles(id.Id)

    if request.method == "POST":

        if 'comment' in request.form:

            comment.addcomment(request.form['comment'], request.form['email'], request.form['nick'], id.Id)

    return render_template("home/read.html", tags=tag.tags(), post=post.post(slug), comments = comment.comments(id), postFiles=postFiles)

#helper methods

@fe.context_processor
def utility_processor():
    def format_font(id):
        tag = TagModel()


        return tag.getRepeats(id)
    return dict(format_font=format_font)

@fe.context_processor
def utility_processor():
    def snap(c):
        return c[0:500]+"..."
    return dict(snap=snap)

@fe.context_processor
def utility_processor():
    def getnick(id):
        u = UserModel()
        user = u.getUser(id)
        return user.Nick
    return dict(getnick=getnick)

@fe.context_processor
def utility_processor():
    def getimages(id):
        p = PostModel()
        return p.getPostImages(id)
    return dict(getimages=getimages)