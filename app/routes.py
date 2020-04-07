"""
API's for the project.
"""

from flask import request
from app import app, db
from app.models import Users, Cars, Tolls, TollsCrossed, Admin
import json


@app.route('/deploy', methods=['GET'])
def deploy():
    some_json = {"message": "Deploy Successful"}
    return some_json, 200


@app.route('/', methods=['GET'])
def index():
    some_json = {"message": "This is example route"}
    return some_json, 200

@app.route('/home', methods=['POST'])
def home():
    user_phone = request.json

    user = Users.query.filter_by(phone=user_phone["phone"]).first()

    local_user_dict = dict()
    local_user_dict["name"] = user.first_name + " " + user.last_name
    local_user_dict["balance"] = user.balance
    local_user_dict["id"] = user.id

    send_user_json = json.dumps(local_user_dict)
    return send_user_json
    # return "GOT REQUEST", 200



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
            return "Incorrect Username/Password", 400


@app.route('/recharge', methods=['PUT'])
def recharge():
    if request.method == 'PUT':
        user_info = request.json
        user = Users.query.filter_by(phone=user_info["phone"]).first()
        user.balance = user.balance + user_info["balance"]
        db.session.commit()
        send_user_balance = {"balance": user.balance}
        return send_user_balance, 200


@app.route('/car', methods=['POST', 'GET'])
def car_list():
    if request.method == 'POST':
        car_info = request.json
        user = Users.query.filter_by(phone=car_info("phone")).first()
        car = Cars(car_number=car_info["car_number"], car_type=car_info["car_type"],
                   owner_id=user.id)
        db.session.add(car)
        db.session.commit()
        return "Added new car.", 201

    if request.method == 'GET':
        user_info = request.args.get('user_id')
        cars = Cars.query.filter_by(owner_id=user_info).all()
        car_arr = []
        for car in cars:
            local_car_dict = dict()
            local_car_dict["Vehicle_Number"] = car.car_number
            local_car_dict["Vehicle_Type"] = car.car_type
            car_arr.append(local_car_dict)
        send_car_json = json.dumps(car_arr)
        return send_car_json, 200

@app.route('/car-details', methods=['GET'])
def car_details():
    vehicle_number = request.args.get('vehicle_number')
    vehicle = Cars.query.filter_by(car_number=vehicle_number).first()
    tolls_arr = []
    for cur_toll in vehicle.tolls_crossed:
        local_toll_dict = dict()
        toll = Tolls.query.filter_by(id=cur_toll.toll).first()
        local_toll_dict["toll_name"] = toll.booth_name
        tolls_arr.append(local_toll_dict)
    print(tolls_arr)
    send_tolls_json = json.dumps(tolls_arr)
    return send_tolls_json




@app.route('/toll-crossed', methods=['POST'])
def toll_crossed():
    """
    This is the function where ML models will be integrated.
    First the car number is read by ML model which is provided as input here.
    Second facial recognition, to recognize the owner of the car (NOT IMPLEMENTED HERE).
    """
    if request.method == 'POST':
        crossing_details = request.json
        car = Cars.query.filter_by(car_number=crossing_details["car_number"]).first()
        toll = Tolls.query.filter_by(id=crossing_details["toll"]).first()
        if car.car_type == "car":
            rem_balance = car.owner.balance - toll.car_toll_price
        else:
            rem_balance = car.owner.balance - toll.bus_toll_price
        if rem_balance >= 0:
            car.owner.balance = rem_balance
            toll = TollsCrossed(toll=crossing_details["toll"], car_number=crossing_details["car_number"])
            db.session.add(toll)
            db.session.commit()
            return "OPEN GATEWAY", 200
        else:
            return "Not enough balance.", 403


@app.route('/admin', methods=['POST'])
def admin_login():
    if request.method == 'POST':
        admin_details = request.json
        admin = Admin.query.filter_by(username=admin_details["username"]).first()
        if admin.password == admin_details["password"]:
            return "Login successful.", 200
        else:
            return "Incorrect Username/Password", 400

