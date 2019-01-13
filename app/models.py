from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import enum
from sqlalchemy import Enum


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

class FootballMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    last_updated = db.Column(db.DateTime)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    match_score_id = db.Column(db.Integer, db.ForeignKey('match_score.id'))
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('match_status.id'))
    home_team = db.relationship('Team', foreign_keys=home_team_id)
    away_team = db.relationship('Team', foreign_keys=away_team_id)
    match_score = db.relationship('MatchScore', foreign_keys=match_score_id)
    season = db.relationship('Season', foreign_keys=season_id)
    status = db.relationship('MatchStatus', foreign_keys=status_id)

class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('football_match.id'))
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match = db.relationship('FootballMatch', foreign_keys=match_id)
    score = db.relationship('Score', foreign_keys=score_id)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_goals = db.Column(db.Integer)
    away_goals = db.Column(db.Integer)

class MatchScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('winner.id'))
    full_time_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    half_time_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    extra_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    penalties_score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
    winner = db.relationship('Winner', foreign_keys=winner_id)
    full_time_score = db.relationship('Score', foreign_keys=full_time_score_id)
    half_time_score = db.relationship('Score', foreign_keys=full_time_score_id)
    extra_score = db.relationship('Score', foreign_keys=extra_score_id)
    penalties_score = db.relationship('Score', foreign_keys=penalties_score_id)

class EnumMatchStatus(enum.Enum):
    POSTPONED = 1
    SCHEDULED = 2
    CANCELED = 3
    SUSPENDED = 4
    IN_PLAY = 5
    PAUSED = 6
    AWARDED = 7
    LIVE = 8

class MatchStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(Enum(EnumMatchStatus))

class EnumWinner(enum.Enum):
    HOME_TEAM = 1
    AWAY_TEAM = 2
    DRAW = 3

class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner = db.Column(Enum(EnumWinner))

class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(9))

class League(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    code = db.Column(db.String(3))

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'))
    points = db.Column(db.Integer)
    league = db.relationship('League', foreign_keys=league_id)

