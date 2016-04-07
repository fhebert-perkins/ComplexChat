from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import pickle

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(32))
    subscriptions = db.Column(db.Text)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.subscriptions = pickle.dumps([])

    def login(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def addSubscription(self, conversationId):
        subs = pickle.loads(self.subscriptions)
        subs.append(conversationId)
        self.subscriptions = pickle.dumps(subs)

    def remSubscription(self, conversationId):
        subs = pickle.loads(self.subscriptions)
        subs.remove(conversationId)
        self.subscriptions = pickle.dumps(subs)

    def __repr__(self):
        return "<User %s>" % self.username

class Conversation(db.Model):
    """Conversation room entry in the database"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    motd = db.Column(db.Text)
    path = db.Column(db.String(100))
    admin = db.Column(db.Integer)

    def __init__(self, name, motd, path, userId):
        self.name = name
        self.motd = motd
        self.path = path
        self.admin = userId

    def updateMOTD(self, motd):
        self.motd = motd
    def __repr__(self):
        return "<Conversation %s>" % self.name
