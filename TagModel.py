from DB import *

class TagModel:

    def __init__(self):
        self.cryptkey = appconfig.CRYPT_KEY


    def tags(self):

        db = DB()
        sql = '''SELECT * FROM Tag'''

        query = db.query(sql)
        tags = query.fetchall()

        db.close()

        if tags:
            return tags
        return False

    def addtag(self, name):

        db = DB()
        sql = '''INSERT INTO Tag (Id,TagName) VALUES (NULL, %s)'''

        q = db.query(sql, (name,) )
        db.conn.commit()
        db.close()


        return  q.lastrowid;
        #todo return id or something