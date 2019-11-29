import sqlite3
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

association_table_met_users = db.Table('association_met_users', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('Users_Table.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users_Table.id'))
)

association_table_user_interest = db.Table('association_user_interest', db.Model.metadata,
    db.Column('interest_id', db.Integer, db.ForeignKey('Interests_Table.id')),
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
    met_users = db.relationship('User', secondary = association_table_met_users, back_populates = 'met_users')

    def __init__(self, **kwargs):
        self.name= kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.year = kwargs.get('year', '')
        self.school = kwargs.get('school', '')

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
    
    # updating in the branch
    class User(db.Model):
    __tablename__ = 'Users_Table'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    netid = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)
    school = db.Column(db.String, nullable = False)
    interests = db.relationship('Interest', secondary = association_table_user_interest, back_populates = 'users')
    met_users = db.relationship('User', secondary = association_table_met_users, back_populates = 'met_users')
    requests = db.relationship('Request', secondary=association_table_met_users, back_populates='requests')


    def __init__(self, **kwargs):
        self.name= kwargs.get('name', '')
        self.netid = kwargs.get('netid', '')
        self.year = kwargs.get('year', '')
        self.school = kwargs.get('school', '')

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
    
    class Request(db.Model):
        __tablename__='Request_Table'
        id = db.Column(db.Integer, primary_key=True)
        sender = db.relationship('User', secondary=association_table_met_users, back_populates='requests')
        receiver = db.relationship('User', secondary=association_table_met_users, back_populates='requests')
        # User must be updated to have a field called requests
        accepted = db.Column(db.Boolean, nullable = False)

        def __init__(self, **kwargs):
            self.accepted = False
        
        def serialize(self):
            return {
            'id': self.id,
            'sender': self.sender.serialize(),
            'receiver': self.receiver.serialize(),
            'accepted': self.accepted
            }



    
    
