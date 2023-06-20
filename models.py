from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    recipes = db.relationship('Recipe', backref='author', lazy=True)
    favorites = db.relationship('Recipe', secondary='favorites', backref=db.backref('favorited_by', lazy=True))

    def __repr__(self):
        return f"User('{self.username}')"


favorites = db.Table('favorites',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                     db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
                     )


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Recipe('{self.title}', '{self.author.username}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"Comment(id={self.id}, text='{self.text[:20]}...', created_at={self.created_at}, user_id={self.user_id}, recipe_id={self.recipe_id})"
