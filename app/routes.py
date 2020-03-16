"""
API's for the project.
"""

from flask import request
from app import app, db
from app.models import Users, Cars, Tolls
import json


@app.route('/home', methods=['GET'])
def profile():
    if request.method == 'GET':
        user_phone = request.json
        user = Users.query.filter_by(phone=user_phone["phone"]).first()

        user_arr = []
        local_user_dict = dict()
        local_user_dict["name"] = user.first_name + " " + user.last_name
        local_user_dict["balance"] = user.balance

        user_arr.append(local_user_dict)

        send_user_json = json.dumps(user_arr)
        return send_user_json


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_details = request.json
        user = Users(first_name=user_details["first_name"], last_name=user_details["last_name"],
                     phone=user_details["phone"], password=user_details["password"])
        db.session.add(user)
        db.session.commit()
        return "Added new User.", 200


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user_info = request.json
        user = Users.query.filter_by(phone=user_info["phone"]).first()
        if user.password == user_info["password"]:
            return "Login successful.", 200
        else:
            return "Incorrect Username/Password", 401


@app.route('/recharge', methods=['PUT'])
def recharge():
    if request.method == 'PUT':
        user_info = request.json
        user = Users.query.filter_by(phone=user_info["phone"]).first()
        user.balance = user.balance + user_info["balance"]
        db.session.commit()
        return "Balance added successfully", 200


