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

    def __init__(self):
        self.cryptkey = appconfig.CRYPT_KEY


    def posts(self):

        db = DB()
        sql = '''SELECT * FROM Post p WHERE p.User=%s'''


        query = db.query(sql, (session["auth"]["Id"], ))
        posts = query.fetchall()
        db.close()

        if posts:
            return posts
        return False

    def addPost(self, title, slug, content, file, active, id=None):

        if file:
            filename = secure_filename(file.filename)

            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            p = self.getPost(id)

            filename = p['Photo']


        db = DB();
        if(id):
            sql = '''UPDATE Post SET Title=%s, DateModified=%s, Content=%s, Photo=%s, Slug=%s, PostStatus=%s WHERE Id=%s'''
            q = db.query(sql, (title, time.strftime('%Y-%m-%d %H:%M:%S'), content, filename, slug, active, id))
        else:
            sql = '''INSERT INTO Post (Id, Title, DateCreated, Content, Photo, User, Slug, PostStatus) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)'''
            q = db.query(sql, (title, time.strftime('%Y-%m-%d %H:%M:%S'), content, filename, session['auth']['Id'], slug, active))

        db.conn.commit();
        db.close();

        #todo return something
        return  q.lastrowid;

    def deletePost(self, id):
        db = DB();


        delSql = '''DELETE FROM PostTag WHERE Post=%s'''
        db.query(delSql,(id))
        db.conn.commit();


        sql = '''DELETE FROM Post WHERE  Id=%s'''
        db.query(sql, (id))
        db.conn.commit();
        db.close();

    def getPost(self, id):
        db = DB()
        sql = '''SELECT * FROM Post p WHERE p.Id=%s'''


        query = db.query(sql, (id, ))
        post = query.fetchone()
        db.close()

        if post:
            return post
        return False

    def addTags(self, tags, post):
        db = DB()
        if (self.getPostTags(post)):

            delSql = '''DELETE FROM PostTag WHERE Post=%s'''
            db.query(delSql,(post))
            db.conn.commit();

        for tag in tags:


            sql = '''INSERT INTO PostTag VALUES  (%s, %s);'''
            db.query(sql,(tag, post))


        db.conn.commit();
        db.close();

    def getPostTags(self, id):
        db = DB()
        sql = '''SELECT Tag FROM PostTag p WHERE p.Post=%s'''


        query = db.query(sql, (id, ))
        post = query.fetchall()
        db.close()

        if post:
            return post
        return False
