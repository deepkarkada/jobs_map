## Ref: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#prerequisites

from flask import Blueprint, request
#from . import db 

authorization = Blueprint('authorization', __name__)

@authorization.route('/login')
def login():
    return 'login authorization'

@authorization.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       return 'signup post authorization', 201
    
    if request.method == 'GET':
        return 'signup get authorization', 201