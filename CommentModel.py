class CommentModel:


    def comments(self, post):

        from models.Comment import Comment
        comments = Comment.query.filter_by(Post=post.Id).all()

        if comments:
            return comments
        return False

    def addcomment(self, comment, email, nick, post):

        from models.Comment import Comment
        from models.shared import db

        new_comment = Comment(nick, email, comment, post)
        db.session.add(new_comment)
        db.session.commit()

        return new_comment.Id


