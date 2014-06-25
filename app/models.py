from app import db


class Novelty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site = db.Column(db.String(15))
    url = db.Column(db.String(2048), unique=True, index=True, nullable=False)
    headline = db.Column(db.String(512), nullable=False)
    published_date = db.Column(db.DateTime)
    comments_count = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)

    def comments(self):
        return Comment.query.filter_by(novelty_id=self.id)

    def user_comments_count(self):
        return Comment.query.filter_by(novelty_id=self.id).count()

    def _repr__(self):
        return '<Novelty %r>' % self.headline


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime)
    nickname = db.Column(db.String(20))
    novelty_id = db.Column(db.Integer, db.ForeignKey('novelty.id'))

    def __repr__(self):
        return '<Comment %r>' % self.body