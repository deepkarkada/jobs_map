## Ref: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#prerequisites

from flask import Blueprint, request
from werkzeug.security import generate_password_hash
from database import db 
from models import User

authorization = Blueprint('authorization', __name__)

@authorization.route('/login')
def login():
    return 'login authorization'

@authorization.route('/signup', methods=['POST'])
def signup():
    # if request.method == 'POST':
    #    return 'signup post authorization', 201

    ## User validation
    name = request.get_json(force=True)['name']
    email = request.get_json(force=True)['email']
    password = request.get_json(force=True)['password']
    
    user = User.query.filter_by(email=email).first()

    if user:
        response = f'Welcome: {name}!'
        return response, 201
    
    ## If user is not found, create new user and add to database
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()

    response = f'Welcome: {name}! Your email: {email} is now validated!'
    return response, 201
