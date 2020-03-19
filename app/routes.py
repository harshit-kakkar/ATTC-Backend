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


@app.route('/car', methods=['POST', 'GET'])
def car_details():
    if request.method == 'POST':
        car_info = request.json
        user = Users.query.filter_by(phone=car_info["phone"]).first()
        car = Cars(car_number=car_info["car_number"], car_type=car_info["car_type"],
                   owner_id=user.id)
        db.session.add(car)
        db.session.commit()
        return "Added new car.", 201

    if request.method == 'GET':
        user_info = request.json
        cars = Cars.query.filter_by(owner_id=user_info["user_id"]).all()
        car_arr = []
        for car in cars:
            local_car_dict = dict()
            local_car_dict["car_number"] = car.car_number
            local_car_dict["car_type"] = car.car_type
            tolls_arr = []
            for cur_toll in car.tolls_crossed:
                local_toll_dict = dict()
                toll = Tolls.query.filter_by(id=cur_toll.toll).first()
                local_toll_dict["toll_name"] = toll.booth_name
                tolls_arr.append(local_toll_dict)
            local_car_dict["tolls_crossed"] = tolls_arr

            car_arr.append(local_car_dict)
        send_car_json = json.dumps(car_arr)
        return send_car_json, 200


