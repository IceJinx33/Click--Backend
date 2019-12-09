import json
import db
from db import db, User, Interest, Request, Friend
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

@app.route('/')
def welcome():
    return os.environ['GOOGLE_CLIENT_ID'], 200

# get all users
@app.route('/api/user/all/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    res = {'success': True, 'data': [u.serialize_long() for u in users]}
    return json.dumps(res), 200

# get a user by their netid
@app.route('/api/user/<string:net_id>/', methods=['GET'])
def get_user(net_id):
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    else:
        return json.dumps({'success': True, 'data': user.serialize_long()}), 200

# get all of a user's friends
@app.route('/api/user/friends/<string:net_id>/', methods=['GET'])
def get_friends(net_id):
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    else:
        friends = user.met_users
        res = {'success': True, 'data': [f.serialize() for f in friends]}
        return json.dumps(res), 200

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
@app.route('/api/user/<string:net_id>/', methods=['DELETE'])
def delete_user(net_id):
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404

    all_friends = Friend.query.all()
    for f in all_friends:
        if f.netid == user.netid:
            db.session.delete(f)
    db.session.delete(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize_long()}), 201

# get all interests
@app.route('/api/interest/all/', methods=['GET'])
def get_all_interests():
    interests = Interest.query.all()
    res = {'success': True, 'data': [i.serialize_long() for i in interests]}
    return json.dumps(res), 200

# get an interest by name
@app.route('/api/interest/<string:interest_name>/', methods=['GET'])
def get_interest(interest_name):
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        return json.dumps({'success': False, 'error': 'Interest not found!'}), 404
    else:
        return json.dumps({'success': True, 'data': interest.serialize_long()}), 200

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
        return json.dumps({'success': False, 'error': 'Interest already exists!'}), 404

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
@app.route('/api/user/<string:net_id>/interest/<string:interest_name>/', methods=['DELETE'])
def delete_user_interest(net_id, interest_name):
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        return json.dumps({'success': False, 'error': 'Interest not found!'}), 404
    user.interests.remove(interest)
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data': user.serialize()}), 201

# delete an interest tag
@app.route('/api/interest/<string:interest_name>/', methods=['DELETE'])
def delete_interest_tag(interest_name):
    interest = Interest.query.filter_by(interest_name = interest_name).first()
    if not interest:
        return json.dumps({'success': False, 'error': 'Interest not found!'}), 404
    db.session.delete(interest)
    db.session.commit()
    return json.dumps({'success': True, 'data': interest.serialize()}), 201

# get recommended users for a specific user
@app.route('/api/user/<string:net_id>/rec/', methods=['GET'])
def get_recommendation(net_id):
    user = User.query.filter_by(netid=net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    else:
        met_people = []
        for p in user.met_users:
            met_people.append(p.netid)
        rec_users = []
        for i in user.interests:
            for u in i.users:
                if (u is not user and u.netid not in met_people and u not in rec_users):
                    rec_users.append(u)
        res = {'success': True, 'data': [us.serialize() for us in rec_users]}
        return json.dumps(res), 200

# get all requests
@app.route('/api/request/all/', methods=['GET'])
def get_all_requests():
    reqs = Request.query.all()
    res = {'success': True, 'data': [r.serialize() for r in reqs]}
    return json.dumps(res), 200

# get a request by id
@app.route('/api/request/<int:request_id>/', methods=['GET'])
def get_request(request_id):
    req = Request.query.filter_by(id = request_id).first()
    if not req:
        return json.dumps({'success': False, 'error': 'Request not found!'}), 404
    else:
        return json.dumps({'success': True, 'data': req.serialize()}), 200

# get all pending requests received by a user
@app.route('/api/request/user/<string:net_id>/rec/', methods=['GET'])
def get_pending_receive_request(net_id):
    user = User.query.filter_by(netid = net_id).first()
    res = {'success': True, 'data': [r.serialize() for r in user.requests_rec]}
    return json.dumps(res), 200

# get all pending requests sent by a user
@app.route('/api/request/user/<string:net_id>/sent/', methods=['GET'])
def get_pending_sent_request(net_id):
    user = User.query.filter_by(netid = net_id).first()
    res = {'success': True, 'data': [r.serialize() for r in user.requests_sent]}
    return json.dumps(res), 200

# create a friend request
@app.route('/api/request/', methods=['POST'])
def create_request():
    post_body = json.loads(request.data)
    sender_netid = post_body.get('sender_netid', "")
    receiver_netid = post_body.get('receiver_netid', "")

    sender = User.query.filter_by(netid=sender_netid).first()
    receiver = User.query.filter_by(netid=receiver_netid).first()

    if not sender:
        return json.dumps({'success': False, 'error': 'Sender not found!'}), 404
    elif not receiver:
        return json.dumps({'success': False, 'error': 'Recipient not found!'}), 404
    else:
        for f in sender.met_users:
            if receiver.netid == f.netid:
                return json.dumps({'success': False, 'error': 'You are already friends with this user!'}), 409
        req = Request()
        req.sender.append(sender)
        req.receiver.append(receiver)
        db.session.add(req)
        db.session.commit()
        return json.dumps({'success': True, 'data': req.serialize()}), 201

# accept or reject a friend request (done by receiver)
@app.route('/api/request/update/', methods=['POST'])
def update_user_request():
    post_body = json.loads(request.data)
    request_id = post_body.get('request_id', "")
    user_netid = post_body.get('user_netid', "")
    user = User.query.filter_by(netid=user_netid).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found'}), 404
    req = Request.query.filter_by(id = request_id).first()
    if not req:
        return json.dumps({'success': False, 'error': 'Request does not exist!'}), 404
    for i in req.receiver:
        r = i
    if (user is r):
        accepted = post_body.get('accepted')
        if(accepted == True):
            req.accepted = True
            for i in req.sender:
                s = i
            friend1 = Friend(
               netid = r.netid,
               user_id = s.netid
            )
            friend2 = Friend(
               netid = s.netid,
               user_id = r.netid
            )
            s.met_users.append(friend1)
            r.met_users.append(friend2)
            db.session.add(s)
            db.session.add(r)
            db.session.add(friend1)
            db.session.add(friend2)
            message = 'Friend request accepted!'
        else:
            message = 'Friend request rejected!'
        db.session.delete(req)
        db.session.commit()
        return json.dumps({'success': True, 'message': message, 'data': req.serialize()}), 201
    return json.dumps({'success': False, 'error': 'User cannot update this request!'}), 409

# delete a request (done by sender)
@app.route('/api/user/<string:net_id>/request/<int:request_id>/', methods=['DELETE'])
def delete_request(net_id, request_id):
    user = User.query.filter_by(netid = net_id).first()
    if not user:
        return json.dumps({'success': False, 'error': 'User not found!'}), 404
    req = Request.query.filter_by(id = request_id).first()
    if not req:
        return json.dumps({'success': False, 'error': 'Request not found!'}), 404
    for i in req.sender:
        s = i
    if user is s:
        db.session.delete(req)
        db.session.commit()
        return json.dumps({'success': True, 'message': 'Request deleted!', 'data': req.serialize()}), 201
    return json.dumps({'success': False, 'error': 'User cannot delete this request!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
