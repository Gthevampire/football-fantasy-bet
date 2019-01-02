from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    bets = db.relationship('Bet', backref='player', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    end_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    extra_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    shootout_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    home_team = db.relationship('Team', foreign_keys=home_team_id)
    away_team = db.relationship('Team', foreign_keys=away_team_id)
    end_score = db.relationship('Score', foreign_keys=end_score_id)
    extra_score = db.relationship('Score', foreign_keys=extra_score_id)
    shootout_score = db.relationship('Score', foreign_keys=shootout_score_id)

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match = db.relationship('Match', foreign_keys=match_id)
    score = db.relationship('Score', foreign_keys=score_id)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)
