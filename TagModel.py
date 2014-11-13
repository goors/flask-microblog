from DB import *

class TagModel:


    def tags(self):

        from models.Tag import Tag
        tags = Tag.query.all()

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

        from models.Tag import Tag
        tag = Tag.query.filter_by(TagName=name).first()


        if tag:
            return tag.Id
        return False

