from flask import Flask, request, Response, render_template, redirect, url_for
import requests
import json

def create_application() -> Flask:
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/logout')
    def logout():
        return 'Logout'

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/signup', methods=['GET'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/signup', methods=['POST'])
    def signup_post():
        # Get the payload from our incoming request
        #payload = request.get_json(force=True)
        userinfo = {
            'email': request.form.get('email'),
            'name': request.form.get('name'),
            'password': request.form.get('password')
        }
        payload = json.dumps(userinfo)

        # Forward the payload to the relevant endpoint in auth
        #response = requests.get(f'http://jobs_map-auth-1:5003/signup')
        response = requests.post(f'http://jobs_map-auth-1:5002/signup', data=payload)
        
        return Response(response.content, response.status_code)
        # Forward the response back to the client
        #return redirect(url_for('login'))
    

    def get_proxy_headers(response):
        # A function to get the needed headers from the requests response
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [
            (name, value)
            for (name, value) in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]
        return headers
    
    return app 

if __name__=="__main__":
    app = create_application()
    app.run("0.0.0.0", port=5001, debug=True)
