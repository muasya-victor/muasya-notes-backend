import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
import requests
from flask import Blueprint, redirect, session, jsonify, request
from flask_restful import Api, Resource
from extensions import db
from users.models import User
import random
import string
from authlib.integrations.flask_client import OAuthError

google_bp = Blueprint('google', __name__)
api = Api(google_bp)

google = None


def set_oauth(oauth_instance):
    global google
    google = oauth_instance


# Generate a nonce for OAuth state verification
def generate_nonce(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


class GoogleLogin(Resource):
    def get(self):
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        nonce = generate_nonce()
        print('nonce login', nonce)
        session['nonce'] = nonce  # Store nonce in session
        return google.authorize_redirect(redirect_uri, state=nonce)


class GoogleCallback(Resource):
    def get(self):
        # Retrieve the access token from Google
        try:
            token = google.authorize_access_token()
            id_token = token.get("id_token")  # Extract the ID token
            access_token = token.get("access_token")  # Extract the access token
        except OAuthError as e:
            return {"error": "Failed to authenticate with Google", "details": str(e)}, 400

        # Get Google's public keys to verify the ID token
        try:
            response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
            response.raise_for_status()
            public_keys = response.json()
        except requests.RequestException as e:
            return {"error": "Failed to fetch Google public keys", "details": str(e)}, 500

        # Decode the ID token
        try:
            user_info = jwt.decode(
                id_token,
                public_keys,
                algorithms=["RS256"],
                audience=os.getenv("GOOGLE_CLIENT_ID"),
                options={"verify_at_hash": True},
                access_token=access_token  # Provide the access token for at_hash verification
            )
        except JWTError as e:
            return {"error": "Invalid ID token", "details": str(e)}, 400

        # Extract email and name
        email = user_info.get("email")
        name = user_info.get("name")
        picture = user_info.get("picture")

        # Generate a custom JWT for your application
        custom_token = jwt.encode(
            {
                "email": email,
                "name": name,
                "exp": datetime.utcnow() + timedelta(minutes=50),
            },
            os.getenv("SECRET_KEY"),
            algorithm="HS256"
        )

        # Check if the user exists; if not, create a new one
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=name, email=email)
            db.session.add(user)
            db.session.commit()

        # Return user data and token to the frontend
        return {
            "status": "success",
            "token": custom_token,
            "photoURL": picture,
            "message": "User authenticated successfully!",
            "data": {"name": name, "email": email},
        }, 200


# Add resources to the blueprint
api.add_resource(GoogleLogin, "/login")
api.add_resource(GoogleCallback, "/callback")
