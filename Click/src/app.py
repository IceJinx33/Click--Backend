import json
import db
from db import db, User, Interest
from flask import Flask, request
import os

app = Flask(__name__)
db_filename = 'Click.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

# get all users
@app.route('/api/user/all/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize_long() for u in users]}
    return json.dumps(res), 200

# get a user by their netid
@app.route('/api/user/', methods=['GET'])
def get_user():
    post_body = json.loads(request.data)
    net_id = post_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 409
    else:
        return json.dumps({'success': True, 'data': user.serialize_long()}), 201

# create a user
@app.route('/api/user/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    net_id = post_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        user = User(
            name = post_body.get('name', ''),
            netid = net_id,
            year = post_body.get('year', ''),
            school = post_body.get('school', '')
        )
        db.session.add(user)
        db.session.commit()
        return json.dumps({'success': True, 'data': user.serialize_long()}), 201
    else:
        return json.dumps({'success': False, 'error': 'User already exists!'}), 409

# delete a user
@app.route('/api/user/', methods=['DELETE'])
def delete_user():
    delete_body = json.loads(request.data)
    net_id = delete_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    db.session.delete(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize_long()}), 200

# get all interests
@app.route('/api/interest/all/', methods=['GET'])
def get_all_interests():
    interests = Interest.query.all()
    res = {'success': True, 'data': [i.serialize_long() for i in interests]}
    return json.dumps(res), 200

# get an interest by name
@app.route('/api/interest/', methods=['GET'])
def get_interest():
    post_body = json.loads(request.data)
    interest_name = post_body.get('interest_name', '')
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        return json.dumps({'success': False, 'error': 'Interest not found!'}), 409
    else:
        return json.dumps({'success': True, 'data': interest.serialize_long()}), 201

# create an interest tag
@app.route('/api/interest/', methods=['POST'])
def create_interest():
    post_body = json.loads(request.data)
    interest_name = post_body.get('interest_name', '')
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        interest = Interest(
            interest_name = interest_name
        )
        db.session.add(interest)
        db.session.commit()
        return json.dumps({'success': True, 'data': interest.serialize()}), 201
    else:
        return json.dumps({'success': False, 'error': 'Interest already exists!'}), 409

# update a user's profile info
@app.route('/api/user/update/', methods=['POST'])
def update_user():
    post_body = json.loads(request.data)
    net_id = post_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    user.name = post_body.get('name', '')
    user.netid = net_id
    user.year = post_body.get('year', '')
    user.school = post_body.get('school', '')
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize_long()}), 201

# add an interest tag to a user profile
@app.route('/api/user/interest/add/', methods=['POST'])
def add_user_interest():
    post_body = json.loads(request.data)
    interest_name = post_body.get('interest_name', '')
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        interest = Interest(
            interest_name = interest_name
        )
        db.session.add(interest)
    net_id = post_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    user.interests.append(interest)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

# delete an interest tag from a user profile
@app.route('/api/user/interest/', methods=['DELETE'])
def delete_user_interest():
    delete_body = json.loads(request.data)
    net_id = delete_body.get('netid', '')
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    interest_name = delete_body.get('interest_name', '')
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        return json.dumps({'success': False, 'error': 'Interest not found!'}), 404
    user.interests.remove(interest)
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
