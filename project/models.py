import jwt
from datetime import datetime, timezone, timedelta
from project import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy import CheckConstraint


# MODELS for COLUMNS in DATABASE (MySQL)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), default=False)
    barcode_id = db.Column(db.String(16), nullable=True, unique=True, default=None)
    age = db.Column(db.Integer, nullable=True, default=None)
    role = db.Column(db.String(50), nullable=False, default="Customer")
    address = db.Column(db.String(200), nullable=True, default=None)
    contact = db.Column(db.String(11), nullable=True, default=None)  # CHANGE TO INTEGER IF NO LEADING ZERO
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    is_active = db.Column(db.Boolean, default=True)
    date_join = db.Column(db.DateTime, default=datetime.now, nullable=False)
   

    def get_id(self):
        return str(self.user_id)

    def get_reset_token(self, expires_sec=1800):
        reset_token = jwt.encode({"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expires_sec), "user_id": self.user_id}, 
            app.config['SECRET_KEY'], algorithm="HS256")
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])['user_id']
        except:
            return None

        return User.query.get(user_id)  

class Attendance(db.Model):
    attendance_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.now, nullable=False)
    time_out = db.Column(db.DateTime)
    overtime_hours = db.Column(db.Float)
    total_hours = db.Column(db.Float, default=0) # add total hours

    user = db.relationship('User', backref=db.backref('attendances'))
    payroll = db.relationship('Payroll', back_populates='attendance')

    def get_id(self):
        return str(self.attendance_id)


    def calculate_overtime_hours(self):        # Check if both time_in and time_out are available
        if self.time_in and self.time_out:
            # Define the fixed start time and end time
            start_time = self.time_in.replace(hour=9, minute=0, second=0)
            end_time = self.time_out.replace(hour=17, minute=0, second=0)

            # Calculate the duration between start time and end time
            duration = end_time - start_time

            # Calculate the overtime hours
            overtime_hours = max(duration - timedelta(hours=8), timedelta())

            # Set the value of overtime_hours attribute
            self.overtime_hours = overtime_hours.total_seconds() / 3600

            # Return the total overtime hours
            return overtime_hours

        # Set the value of overtime_hours attribute to None if either time_in or time_out is missing
        self.overtime_hours = None
        return None


class Payroll(db.Model):
    payroll_id = db.Column(db.Integer, primary_key=True)
    payrate = db.Column(db.Numeric(precision=8, scale=2))
    gross_pay = db.Column(db.Numeric(precision=8, scale=2))
    tax = db.Column(db.Numeric(precision=5, scale=2))
    net_pay = db.Column(db.Numeric(precision=8, scale=2))
    month = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    generated = db.Column(db.DateTime, default=datetime.now)
    attendance_id = db.Column(db.Integer, db.ForeignKey('attendance.attendance_id'))

    user = db.relationship('User', backref='payroll_user')
    attendance = db.relationship('Attendance', back_populates='payroll')

    def get_id(self):
        return str(self.payroll_id)



class Employee(UserMixin, db.Model):
    employee_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.employee_id)              

class Book_date(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50))
    service = db.Column(db.String(50))
    service2 = db.Column(db.String(50), nullable=True, default=None)
    service3 = db.Column(db.String(50), nullable=True, default=None)
    date = db.Column(db.DateTime,nullable=False)
    is_done = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('book_dates', lazy=True, cascade="all, delete-orphan"))

    def get_id(self):
        return str(self.book_id)

    #Cascade option when the parent object is deleted " cascade="all, delete-orphan " if the User object deleted
    #all of its associated 'book_date' will be deleted.

    # def __repr__(self):
    #     return f" User('{self.lname}', '{self.email}', '{self.image_file}')"

class AuditTrail(db.Model):
    log_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    event_type = db.Column(db.String(50))
    event_description = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref=db.backref('audit_trail_entries', lazy=True))

    def __repr__(self):
        return f"<AuditTrail(id={self.id}, user_id={self.user_id}, event_type='{self.event_type}', timestamp='{self.timestamp}')>"

class Inventory(db.Model):
    inventory_id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(50))
    category = db.Column(db.String(50))
    price = db.Column(db.Numeric(precision=8, scale=2)) #rounded of 2 decimal places
    stock = db.Column(db.Integer)
    expiration_date = db.Column(db.DateTime, nullable=True)

    def get_id(self):
        return str(self.inventory_id)




