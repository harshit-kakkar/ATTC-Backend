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
        print(user.first_name)
        local_user_dict["name"] = user.first_name + " " + user.last_name
        local_user_dict["balance"] = user.balance
        print(local_user_dict["name"])

        user_arr.append(local_user_dict)

        send_user_json = json.dumps(user_arr)
        return send_user_json


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        user_details = request.json
        user = Users(first_name=user_details["first_name"], last_name=user_details["last_name"],
                     phone=user_details["phone"])
        db.session.add(user)
        db.session.commit()
        print(user_details["first_name"])
        return "Added new User.", 200
