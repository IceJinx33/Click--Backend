import sqlite3
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


association_table_user_interest = db.Table('association_user_interest', db.Model.metadata,
    db.Column('interest_id', db.Integer, db.ForeignKey('Interests_Table.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users_Table.id'))
)

association_table_request_send = db.Table('association_request_send', db.Model.metadata,
    db.Column('request_id', db.Integer, db.ForeignKey('Requests_Table.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users_Table.id'))
)

association_table_request_rec = db.Table('association_request_rec', db.Model.metadata,
    db.Column('request_id', db.Integer, db.ForeignKey('Requests_Table.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users_Table.id'))
)

class User(db.Model):
    __tablename__ = 'Users_Table'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)
    school = db.Column(db.String, nullable = False)
    interests = db.relationship('Interest', secondary = association_table_user_interest, back_populates = 'users')
    met_users = db.relationship('Friend', cascade = 'delete')
    requests_sent = db.relationship('Request', secondary = association_table_request_send, back_populates = 'sender')
    requests_rec = db.relationship('Request', secondary = association_table_request_rec, back_populates = 'receiver')

    def __init__(self, **kwargs):
        self.name= kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.year = kwargs.get('year', '')
        self.school = kwargs.get('school', '')
        self.met_users = []

    def serialize_long(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            'year': self.year,
            'school': self.school,
            'interests': [i.serialize() for i in self.interests],
            'met_users': [m.serialize() for m in self.met_users]
        }

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'netid': self.netid,
            'year': self.year,
            'school': self.school,
            'interests': [i.serialize() for i in self.interests]
        }


class Interest(db.Model):
    __tablename__ = 'Interests_Table'
    id = db.Column(db.Integer, primary_key = True)
    interest_name = db.Column(db.String, nullable = False)
    users = db.relationship('User', secondary = association_table_user_interest, back_populates = 'interests')

    def __init__(self, **kwargs):
        self.interest_name= kwargs.get('interest_name', '')

    def serialize_long(self):
        return {
            'id': self.id,
            'interest_name': self.interest_name,
            'users': [u.serialize() for u in self.users]
        }

    def serialize(self):
        return {
            'id': self.id,
            'interest_name': self.interest_name
        }

class Friend(db.Model):
    __tablename__='Friends_Table'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users_Table.id'), nullable = False)

    def __init__(self, **kwargs):
        self.netid = kwargs.get('netid')
        self.user_id = kwargs.get('user_id')

    def serialize(self):
        user = User.query.filter_by(netid=self.netid).first()
        return {
            'id': user.id,
            'name': user.name,
            'netid': user.netid,
            'year': user.year,
            'school': user.school,
            'interests': [i.serialize() for i in user.interests]
        }

class Request(db.Model):
    __tablename__='Requests_Table'
    id = db.Column(db.Integer, primary_key=True)
    sender = db.relationship('User', secondary = association_table_request_send, back_populates = 'requests_sent')
    receiver = db.relationship('User', secondary = association_table_request_rec, back_populates = 'requests_rec')
    accepted = db.Column(db.Boolean, nullable = False)

    def __init__(self, **kwargs):
        self.accepted = kwargs.get('accepted', False)

    def serialize(self):
        return {
        'id': self.id,
        'sender_netid': [s.netid for s in self.sender],
        'receiver_netid': [r.netid for r in self.receiver],
        'accepted': self.accepted
        }
