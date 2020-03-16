from app import db, app


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    balance = db.Column(db.Integer, default=0)
    cars = db.relationship('Cars', backref='owner')


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String)
    car_type = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tolls = db.relationship('Tolls', backref='car')


class Tolls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booth_name = db.Column(db.String)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))

