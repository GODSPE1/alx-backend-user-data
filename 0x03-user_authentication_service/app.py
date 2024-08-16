#!/usr/bin/env python3
"""A Flask App"""
from flask import Flask, request, jsonify, abort, redirect
from auth import Auth

app = Flask(__name__)
Auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home():
    """Return a jsonify payload of the form"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Get user email"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = Auth.register_user(email, password)
        return jsonify({
            "email": "<registered email>", "message": "user created"
            })
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """login a user and create a session"""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(404, description="Missing email or password")

    if Auth.valid_login(email, password):
        session_id = Auth.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response, 200
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """logout out a user and destroy the session"""
    session_id = request.cookies.get("session_id")

    if user:
        Auth.destroy_session()

    if not session_id:
        abort(403)

    user = Auth.get_user_from_session_id(session_id=session_id)
    if user:
        Auth.destroy_session(user.id)
        return redirect("/")

    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """get a given user profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = Auth.get_user_from_session_id('session_id')
    if user:
        return jsonify({"email": user.email})
    abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Generating a reset passowrd token for the user
    """

    email = request.form.get("email")
    session_id = Auth.create_session(email)

    if not session_id:
        abort(403)

    token = Auth.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Updating the user's password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        Auth.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
