import os
from flask import Flask, request, make_response
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth
from extensions import db
from flask_cors import CORS
from flask_session import Session

from google_auth import google_bp, set_oauth  # Import set_oauth function
from users import users_bp
from notes import notes_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'  # Use file system-based session storage
app.config['SESSION_PERMANENT'] = False    # Make sessions temporary
app.config['SESSION_USE_SIGNER'] = True    # Sign the session cookies
Session(app)
app.config.from_object('config.Config')

# CORS Configuration
CORS(app,
     origins="http://localhost:5173",  # Allow requests from this origin
     allow_credentials=True,  # Allow cookies to be sent with requests
     supports_credentials=True,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"])

# OAuth setup
oauth = OAuth(app)
google_oauth = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=os.getenv("GOOGLE_DISCOVERY_URL"),
    client_kwargs={"scope": "openid email profile"},
)
set_oauth(google_oauth)

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(notes_bp, url_prefix='/notes')
@app.route('/notes', methods=["OPTIONS"])
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Credentials', 'true')

    return response

@app.before_request
def log_request():
    print(f"Request method: {request.method}, Request URL: {request.url}")

app.register_blueprint(google_bp, url_prefix="/auth")

# Initialize Database
@app.route('/initdb')
def init_db():
    db.create_all()
    return 'Database tables created!'

if __name__ == '__main__':
    app.run(debug=True)
