from DB import *
import time
class CommentModel:

    def __init__(self):
        self.cryptkey = appconfig.CRYPT_KEY


    def comments(self, post):

        db = DB()
        sql = '''SELECT * FROM Comment WHERE Post=%s'''

        query = db.query(sql, (post,))
        comments = query.fetchall()

        db.close()

        if comments:
            return comments
        return False

    def addcomment(self, comment, email, nick, post):

        db = DB()
        sql = '''INSERT INTO Comment (Id, Comment, Post, Nick, Email, DateCreated) VALUES (NULL, %s, %s, %s, %s, %s)'''

        q = db.query(sql, (comment,post,nick, email, time.strftime('%Y-%m-%d %H:%M:%S')) )
        db.conn.commit()
        db.close()


        return  q.lastrowid;
        #todo return id or something



