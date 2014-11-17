class TagModel:

    def __init__(self):

        from models import Tag
        from models import  Post

        self.Tag = Tag.Tag
        self.Post = Post.Post

    def tags(self):

        tags = self.Tag.query.all()

        if tags:
            return tags
        return False

    def addtag(self, name):

        from models import db
        new_tag = self.Tag(name)
        db.session.add(new_tag)
        db.session.commit()

        return new_tag.Id


    def getRepeats(self, id):

        u = self.Post.query.join(self.Post.tags).filter(self.Tag.Id == id).count()
        return u


    def getTagByName(self, name):

        tag = self.Tag.query.filter_by(TagName=name).first()

        if tag:
            return tag.Id
        return False

