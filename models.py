from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User representation representing passengers and admins."""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='User')  # 'User' or 'Admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', cascade='all, delete-orphan', lazy=True)
    recommendations = db.relationship('Recommendation', backref='user', cascade='all, delete-orphan', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Overriding flask-login methods to use user_id as identifier
    def get_id(self):
        return str(self.user_id)


class Flight(db.Model):
    """Flight details managed by admins and searched by users."""
    __tablename__ = 'flights'
    
    flight_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flight_number = db.Column(db.String(20), unique=True, nullable=False)
    airline = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    booked_seats = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')  # 'Scheduled', 'Delayed', 'Cancelled', 'Completed'
    
    # Table arguments for database indexes
    __table_args__ = (
        db.Index('idx_source_destination', 'source', 'destination'),
        db.Index('idx_flight_number', 'flight_number'),
    )
    
    # Relationships
    bookings = db.relationship('Booking', backref='flight', cascade='all, delete-orphan', lazy=True)
    seat_reservations = db.relationship('SeatReservation', backref='flight', cascade='all, delete-orphan', lazy=True)

    @property
    def occupancy_rate(self):
        if self.seats == 0:
            return 0.0
        return (self.booked_seats / self.seats) * 100.0


class Booking(db.Model):
    """Booking records associated with passengers and users."""
    __tablename__ = 'bookings'
    
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id', ondelete='CASCADE'), nullable=False)
    pnr = db.Column(db.String(10), unique=True, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    travel_date = db.Column(db.Date, nullable=False)
    
    # Passenger specific info (supports booking for others)
    passenger_name = db.Column(db.String(100), nullable=False)
    passenger_age = db.Column(db.Integer, nullable=True)
    passenger_gender = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='Booked')  # 'Booked', 'Cancelled'
    
    # Table arguments for database indexes
    __table_args__ = (
        db.Index('idx_booking_user', 'user_id'),
    )
    
    # Relationships
    seat_reservations = db.relationship('SeatReservation', backref='booking', cascade='all, delete-orphan', lazy=True)
    payments = db.relationship('Payment', backref='booking', cascade='all, delete-orphan', lazy=True)


class SeatReservation(db.Model):
    """Specific seat numbers assigned to flight bookings."""
    __tablename__ = 'seat_reservations'
    
    reservation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.flight_id', ondelete='CASCADE'), nullable=False)
    seat_number = db.Column(db.String(5), nullable=False)


class Payment(db.Model):
    """Payment transactions mapping back to booking confirmations."""
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # 'UPI', 'Credit Card', 'Debit Card', 'Net Banking'
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)  # 'Success', 'Failed'


class Recommendation(db.Model):
    """Machine learning predictions generated for users."""
    __tablename__ = 'recommendations'
    
    recommendation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    predicted_airline = db.Column(db.String(100), nullable=False)
    confidence_score = db.Column(db.Numeric(5, 2), nullable=False)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
