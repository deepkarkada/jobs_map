from flask import Flask 
from database import db 

#import auth as auth_blueprint 
from authorization import authorization as auth

def create_application(db_uri: str) -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    # blueprint for auth routes in app 
    app.register_blueprint(
        auth)
    
    return app
    
if __name__=="__main__":
    app = create_application(db_uri="sqlite:///users.db")
    app.run("0.0.0.0", port=5002, debug=True)