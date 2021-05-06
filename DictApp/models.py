from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    words = db.relationship('Word',backref='author', lazy=True)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50),nullable=False)
    definition = db.Column(db.String(1000),nullable=False)
    examples = db.Column(db.String(1000),nullable=False)
    power = db.Column(db.Integer,default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Word('{self.word}')"

db.create_all()