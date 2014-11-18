class CommentModel:

    def __init__(self):

        from models import  Comment

        self.Comment = Comment.Comment


    def comments(self, post):

        comments = self.Comment.query.filter_by(Post=post.Id).all()

        if comments:
            return comments
        return False

    def addcomment(self, comment, email, nick, post):

        from models import db
        new_comment = self.Comment(nick, email, comment, post)
        db.session.add(new_comment)
        db.session.commit()

        return new_comment.Id
