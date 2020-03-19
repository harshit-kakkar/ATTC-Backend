from app import db, app


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    password = db.Column(db.String)
    phone = db.Column(db.String, unique=True)
    balance = db.Column(db.Integer, default=0)
    cars = db.relationship('Cars', backref='owner')


class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_number = db.Column(db.String, unique=True)
    car_type = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tolls_crossed = db.relationship('TollsCrossed', backref='car')


class TollsCrossed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # toll = db.relationship('Tolls', backref='toll_crossed', uselist=False)
    toll = db.Column(db.Integer, db.ForeignKey('tolls.id'))
    car_number = db.Column(db.String, db.ForeignKey('cars.car_number'))


class Tolls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booth_name = db.Column(db.String)
    car_toll_price = db.Column(db.Integer)
    bus_toll_price = db.Column(db.Integer)


