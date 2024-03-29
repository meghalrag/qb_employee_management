import jwt
from flask import session, jsonify, redirect, url_for, flash
from config import JWT_SECRET_KEY

def token_required(func):
    """decorator to verify the token in every request"""
    def wrapper(*args, **kwargs):
        token = session.get("access_token")
        if not token:
            flash("Your token is missing / expired. Please login again", "danger")
            return redirect(url_for("home_url.login"))
        
        try:
            _ = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            # You can now access payload data like payload['user_id'], payload['username'], etc.
        except jwt.ExpiredSignatureError:
            flash("Your Token is Expired", "danger")
            return redirect(url_for("home_url.login"))
        except jwt.InvalidTokenError:
            flash("Invalid Token", "danger")
            return redirect(url_for("home_url.login"))
        
        return func(*args, **kwargs)
    return wrapper