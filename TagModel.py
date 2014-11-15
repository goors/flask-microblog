
class TagModel :


    def tags(self):

        from models.Tag import Tag
        tags = Tag.query.all()

        if tags:
            return tags
        return False

    def addtag(self, name):

        from models.Tag import Tag
        from models.shared import db

        new_tag = Tag(name)
        db.session.add(new_tag)
        db.session.commit()

        return new_tag.Id


    def getRepeats(self, id):

        from models.Post import  Post
        from models.Tag import  Tag

        u = Post.query.join(Post.tags).filter(Tag.Id == id).count()
        return u


    def getTagByName(self, name):

        from models.Tag import Tag
        tag = Tag.query.filter_by(TagName=name).first()


        if tag:
            return tag.Id
        return False

