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
        sql = '''INSERT INTO Tag (Id, TagName) VALUES (NULL, %s)'''

        q = db.query(sql, (name,) )
        db.conn.commit()
        db.close()


        return  q.lastrowid;
        #todo return id or something

    def getRepeats(self, id):
        db = DB()
        sql = '''SELECT COUNT(*) as c FROM PostTag WHERE  Tag=%s'''

        query = db.query(sql, (id,))
        tags = query.fetchone()
        db.close()
        return tags['c']

    def getTagByName(self, name):
        print name
        db = DB()
        sql = '''SELECT * FROM Tag WHERE TagName=%s'''

        query = db.query(sql, (name, ))
        tags = query.fetchone()

        db.close()

        if tags:
            return tags['Id']
        return False

