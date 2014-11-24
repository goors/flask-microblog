from flask import Blueprint, redirect, render_template, request
from TagModel import *
from PostModel import *
from UserModel import *
from CommentModel import *
from htmlmin.minify import html_minify
from appconfig import *

fe = Blueprint('fe', __name__)


@fe.route('/tag/<tagname>', methods=['GET'])
def hometags(tagname=None):

    tag = TagModel()
    post = PostModel()
    tagId = tag.getTagByName(tagname)
    t = render_template("home/index.html", tags=tag.tags(), posts=post.posts(None, tagId))
    return html_minify(unicode(t).encode('utf-8'))

@fe.route('/', methods=['GET'])
def home():

    tag = TagModel()
    post = PostModel()

    t = render_template("home/index.html", tags=tag.tags(), posts=post.posts(True, None))
    return html_minify(unicode(t).encode('utf-8'))


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

        if 'comment' in request.form and 'cid' not in request.form:

            comment.addcomment(request.form['comment'], request.form['email'], request.form['nick'], id.Id)

        if 'comment' in request.form and 'cid' in request.form:

            comment.addcomment(request.form['comment'], request.form['email'], request.form['nick'], id.Id, request.form['cid'])

            ##send reply to if any email address defined
            c = comment.getCommentEmail(request.form['cid'])
            if c.Email:
                from UserModel import UserModel
                u = UserModel()
                u.send_email(request.form['nick'] + " just commented on post "+id.Title, c.Email, request.form['comment']+ "<p>"+URL_FE+"read/"+id.Slug+"</p>", c.Nick)

        if 'password' in request.form:

            from werkzeug import check_password_hash

            if check_password_hash(id.Password, request.form['password']):
                t = render_template("home/read.html", tags=tag.tags(), post=post.post(slug), comments = comment.comments(id), postFiles=postFiles)
                return html_minify(unicode(t).encode('utf-8'))

    if id.Password != 'NULL':
        t = render_template("home/read-with-password.html", tags=tag.tags(), post=post.post(slug), comments = comment.comments(id), postFiles=postFiles)
    else:
        t = render_template("home/read.html", tags=tag.tags(), post=post.post(slug), comments = comment.comments(id), postFiles=postFiles)
    return html_minify(unicode(t).encode('utf-8'))


@fe.route("/sitemap.xml", methods=["GET"])
def sitemap():
    p =  PostModel()
    return p.generateSiteMap()
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


@fe.context_processor
def utility_processor():
    def getChildren(id):
        p = CommentModel()
        return p.getChildren(id)
    return dict(getChildren=getChildren)