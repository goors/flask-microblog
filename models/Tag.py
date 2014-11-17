from models import db
class Tag(db.Model):
    __tablename__ = 'Tag'
    Id = db.Column(db.Integer, primary_key=True)
    TagName = db.Column(db.String(45))

    def __init__(self, name):
        self.TagName = name