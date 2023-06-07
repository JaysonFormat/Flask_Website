import re
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from datetime import datetime, time, timedelta,date
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, DateTimeField, SelectField, DateTimeLocalField, RadioField, IntegerField, DecimalField, DateField,FloatField
from wtforms.widgets import DateTimeInput, DateInput
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp, NumberRange, Optional
from project.models import User

bcrypt = Bcrypt()

class RegistrationForm(FlaskForm):
    fname = StringField("First name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=20), 
        Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please Choose a new one!')

    terms = BooleanField('Agree Terms and Conditions')



class LoginForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])

    password = PasswordField('Password',validators=[DataRequired()])

    remember = BooleanField('Remember Me')

    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    fname = StringField("First name", validators=[DataRequired(), Length(min=2, max=50)])

    lname = StringField("Last name", validators=[DataRequired(), Length(min=2, max=50)])

    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=18, max=100)])

    gender = RadioField('Gender', validators=[DataRequired()], choices=[('Male','Male'),('Female','Female')])

    address = StringField("Address", validators=[DataRequired(), Length(max=200)])

    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])

    contact = StringField('Contact Number', validators=[Length(min=11, max=11)])

    submit = SubmitField('Update')

    def validate_last(self, lname):

        if lname.data != current_user.lname:
            user = User.query.filter_by(lname=lname.data).first()
            if user:
                raise ValidationError('Last Name is already present. Please Choose a new one!')

    def validate_email(self, email):

            if email.data != current_user.email:
                user = User.query.filter_by(email=email.data).first()
                if user:
                    raise ValidationError('Email is already present. Please Choose a new one!')

    def validate_last(self, fname):

        if fname.data != current_user.fname:
            user = User.query.filter_by(fname=fname.data).first()
            if user:
                raise ValidationError('First Name is already present. Please Choose a new one!')


class UpdatePasswordForm(FlaskForm):

    current_password = PasswordField('Current Password', validators=[Optional()])

    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, max=20),Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(),EqualTo('new_password')])

    submit_update = SubmitField('Change Password')

class UserUpdatePasswordForm(FlaskForm):
    
    current_password = PasswordField('Current Password', validators=[Optional()])

    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=8, max=20),Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(),EqualTo('new_password')])

    submit_update = SubmitField('Change Password')

    def validate_current_password(self, current_password):
        # Check if the entered current password matches the user's registered password
        if not bcrypt.check_password_hash(current_user.password, current_password.data):
            raise ValidationError('Current password is incorrect.')

    def validate_new_password(self, new_password):
        # Check if the new password is the same as the user's registered password
        if bcrypt.check_password_hash(current_user.password, new_password.data):
            raise ValidationError('New password cannot be the same as the current password.')

class AppointmentForm(FlaskForm):

    email = StringField('Email', validators=[Optional(), Email()])

    #is_paid = SelectField('Online Payment?', validators=[DataRequired()], choices=[('','Select if YES or NO'),('YES','YES'),('NO','NO')])

    branch = SelectField('Branch', validators=[DataRequired()], choices=[('','Select your Branch'),('FCM','Fairview Center Mall Branch'),('Zapote','Zapote Branch')])
    
    service = SelectField('Book #1', validators=[DataRequired()], choices=[('','What type of service do you want?'),('Haircut with style','Haircut with style'),('Haircut Trim','Haircut Trim'),('Traditional Perm','Traditional Perm'),('Hair Extenstion','Hair Extenstion'),('Hair Color','Hair Color')
        ,('Highlights','Highlights'),('Hair Rebond','Hair Rebond'),('Brazilian','Brazilian'),('Bayalage','Bayalage'),('',''),('Manicure','Manicure'),('Pedicure','Pedicure'),('Manicure Gel','Manicure Gel'),('Ordinary Manicure','Ordinary Manicure'),('Pedicure Gel','Pedicure Gel'),('Pedicure Ordinary','Pedicure Ordinary')
        ,('Footspa','Footspa'),('Footspa with Footmask','Footspa with Footmask'),('Footspa with Gel','Footspa with Gel'),('',''),('1 Hour Massage','1 Hour Massage'),('1 1/2 Massage','1 1/2 Massage'),('2 Hours Massage','2 Hours Massage'),('1 Hour Massage with Hot Compress','1 Hour Massage with Hot Compress'),('1 1/2 Hour Massage with Hot Compress','1 1/2 Hour Massage with Hot Compress')
        ,('2 Hours Massage with Hot Compress','2 Hours Massage with Hot Compress'),('1 Hour Massage with Hot Stone','1 Hour Massage with Hot Stone'),('1 1/2 Hour Massage with Hot Stone', '1 1/2 Hour Massage with Hot Stone'),('2 Hours Massage with Hot Stone','2 Hours Massage with Hot Stone '),('1 Hour Massage with Ventosa','1 Hour Massage with Ventosa'),('1 1/2 Hour Massage with Ventosa','1 1/2 Hour Massage with Ventosa')
        ,('30 Mins FootReflex','30 mins FootReflex'),('1 Hour FootReflex','1 Hour Footreflex'),('Ear Candle Only','Ear Candle Only'),('Ear Candle with Massage','Ear Candle with Massage'),('1 1/2 Hour Body Scrub with Massage','1 1/2 Hour Body Scrub with Massage'),('2 Hours Body Scrube with Massage','2 Hours Body Scrube with Massage'),('',''),('Whitening','Whitening'),('Waxing Underarm','Waxing Underarm')
        ,('Waxing Legs','Waxing Legs'),('Waxing Bikini','Waxing Bikini'),('Eyelash Extenstion','Eyelash Extenstion'),('Eyelash Firming','Eyelash Firming'),('Eyebrow Threading','Eyebrow Threading'),('Eyebrow Shaving','Eyebrow Shaving'),('Traditional Hair & Make-up','Traditional Hair & Make-up'),('Air Brush Make-up','Air Brush Make-up')])

    service2 = SelectField('Book #2', validators=[Optional()], choices=[('','Add more service?'),('Haircut with style','Haircut with style'),('Haircut Trim','Haircut Trim'),('Traditional Perm','Traditional Perm'),('Hair Extenstion','Hair Extenstion'),('Hair Color','Hair Color')
        ,('Highlights','Highlights'),('Hair Rebond','Hair Rebond'),('Brazilian','Brazilian'),('Bayalage','Bayalage'),('',''),('Manicure','Manicure'),('Pedicure','Pedicure'),('Manicure Gel','Manicure Gel'),('Ordinary Manicure','Ordinary Manicure'),('Pedicure Gel','Pedicure Gel'),('Pedicure Ordinary','Pedicure Ordinary')
        ,('Footspa','Footspa'),('Footspa with Footmask','Footspa with Footmask'),('Footspa with Gel','Footspa with Gel'),('',''),('1 Hour Massage','1 Hour Massage'),('1 1/2 Massage','1 1/2 Massage'),('2 Hours Massage','2 Hours Massage'),('1 Hour Massage with Hot Compress','1 Hour Massage with Hot Compress'),('1 1/2 Hour Massage with Hot Compress','1 1/2 Hour Massage with Hot Compress')
        ,('2 Hours Massage with Hot Compress','2 Hours Massage with Hot Compress'),('1 Hour Massage with Hot Stone','1 Hour Massage with Hot Stone'),('1 1/2 Hour Massage with Hot Stone', '1 1/2 Hour Massage with Hot Stone'),('2 Hours Massage with Hot Stone','2 Hours Massage with Hot Stone '),('1 Hour Massage with Ventosa','1 Hour Massage with Ventosa'),('1 1/2 Hour Massage with Ventosa','1 1/2 Hour Massage with Ventosa')
        ,('30 Mins FootReflex','30 mins FootReflex'),('1 Hour FootReflex','1 Hour Footreflex'),('Ear Candle Only','Ear Candle Only'),('Ear Candle with Massage','Ear Candle with Massage'),('1 1/2 Hour Body Scrub with Massage','1 1/2 Hour Body Scrub with Massage'),('2 Hours Body Scrube with Massage','2 Hours Body Scrube with Massage'),('',''),('Whitening','Whitening'),('Waxing Underarm','Waxing Underarm')
        ,('Waxing Legs','Waxing Legs'),('Waxing Bikini','Waxing Bikini'),('Eyelash Extenstion','Eyelash Extenstion'),('Eyelash Firming','Eyelash Firming'),('Eyebrow Threading','Eyebrow Threading'),('Eyebrow Shaving','Eyebrow Shaving'),('Traditional Hair & Make-up','Traditional Hair & Make-up'),('Air Brush Make-up','Air Brush Make-up')])

    service3 = SelectField('Book #3', validators=[Optional()], choices=[('','Add more service?'),('Haircut with style','Haircut with style'),('Haircut Trim','Haircut Trim'),('Traditional Perm','Traditional Perm'),('Hair Extenstion','Hair Extenstion'),('Hair Color','Hair Color')
        ,('Highlights','Highlights'),('Hair Rebond','Hair Rebond'),('Brazilian','Brazilian'),('Bayalage','Bayalage'),('',''),('Manicure','Manicure'),('Pedicure','Pedicure'),('Manicure Gel','Manicure Gel'),('Ordinary Manicure','Ordinary Manicure'),('Pedicure Gel','Pedicure Gel'),('Pedicure Ordinary','Pedicure Ordinary')
        ,('Footspa','Footspa'),('Footspa with Footmask','Footspa with Footmask'),('Footspa with Gel','Footspa with Gel'),('',''),('1 Hour Massage','1 Hour Massage'),('1 1/2 Massage','1 1/2 Massage'),('2 Hours Massage','2 Hours Massage'),('1 Hour Massage with Hot Compress','1 Hour Massage with Hot Compress'),('1 1/2 Hour Massage with Hot Compress','1 1/2 Hour Massage with Hot Compress')
        ,('2 Hours Massage with Hot Compress','2 Hours Massage with Hot Compress'),('1 Hour Massage with Hot Stone','1 Hour Massage with Hot Stone'),('1 1/2 Hour Massage with Hot Stone', '1 1/2 Hour Massage with Hot Stone'),('2 Hours Massage with Hot Stone','2 Hours Massage with Hot Stone '),('1 Hour Massage with Ventosa','1 Hour Massage with Ventosa'),('1 1/2 Hour Massage with Ventosa','1 1/2 Hour Massage with Ventosa')
        ,('30 Mins FootReflex','30 mins FootReflex'),('1 Hour FootReflex','1 Hour Footreflex'),('Ear Candle Only','Ear Candle Only'),('Ear Candle with Massage','Ear Candle with Massage'),('1 1/2 Hour Body Scrub with Massage','1 1/2 Hour Body Scrub with Massage'),('2 Hours Body Scrube with Massage','2 Hours Body Scrube with Massage'),('',''),('Whitening','Whitening'),('Waxing Underarm','Waxing Underarm')
        ,('Waxing Legs','Waxing Legs'),('Waxing Bikini','Waxing Bikini'),('Eyelash Extenstion','Eyelash Extenstion'),('Eyelash Firming','Eyelash Firming'),('Eyebrow Threading','Eyebrow Threading'),('Eyebrow Shaving','Eyebrow Shaving'),('Traditional Hair & Make-up','Traditional Hair & Make-up'),('Air Brush Make-up','Air Brush Make-up')])


    start_time = time(hour=10, minute=0)
    end_time = time(hour=16, minute=0)

    # minimum date is tomorrow
    min_date = datetime.now().date() + timedelta(days=1)

    # maximum date is one week ahead
    max_date = min_date + timedelta(days=7)

    # set minimum and maximum times for each day
    min_time = datetime.combine(min_date, start_time)
    max_time = datetime.combine(min_date, end_time)

    date = DateTimeLocalField('Appointment Date & Time', 
        format='%Y-%m-%dT%H:%M', 
        validators=[DataRequired()], 
        default=min_time, 
        render_kw={'min': min_time.strftime('%Y-%m-%dT%H:%M'), 
                   'max': datetime.combine(max_date, end_time).strftime('%Y-%m-%dT%H:%M'), 
            }
        )
      
    submit = SubmitField('Book')

    submit_another = SubmitField('Paynow')

    def validate_appointment_date(self, appointment_date):
        if appointment_date.data.time() < self.start_time:
            raise ValidationError('Appointment time must be after 10am.')
        elif appointment_date.data.time() > self.end_time:
            raise ValidationError('Appointment time must be before 4pm.')

    def validate(self):
        if not super(AppointmentForm, self).validate():
            return False

        if self.service3.data and not self.service2.data:
            self.service2.errors.append('Please select Service 2 before selecting Service 3')
            return False

        return True


class EditUserForm(FlaskForm):
    fname = StringField("First name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last name", validators=[DataRequired(), Length(min=2, max=50)])

    # password = PasswordField('New Password', validators=[
    #     DataRequired(), 
    #     Length(min=8, max=20), 
    #     Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    email = EmailField('Email', validators=[DataRequired(), Length(min=2, max=50), Email()])
    contact = StringField('Contact Number', validators=[Length(min=11, max=11)])
    submit = SubmitField('Update')

class InventoryForm(FlaskForm):
    product = StringField("Product", validators=[DataRequired(), Length(min=2, max=50)])
    category = SelectField("Category", validators=[DataRequired()], choices=(('', 'Item Category'), ('Nail','Nail'), ('Hair','Hair'), ('Spa','Spa'), ('Massage','Massage'),('Face/Other','Face and Other')))
    price = DecimalField("Price", places=2, render_kw={"placeholder": "0.00"}, validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=1, max=500)])
    expiration_date = DateField('Expiration Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Product')
    submit_update = SubmitField("Update")

    # def validate_expiration_date(self, field):
    #     if field.data and field.data < date.today():
    #         raise ValidationError("Expiration date must be in the future.")


class EmployeeForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])

    password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)
    ,Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    role = SelectField('Role', validators=[DataRequired()], choices=[('','Choose a Role'),('Super_admin', 'Super_admin'),('Admin','Admin'),('Staff','Staff')])
    email = StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])    
    submit = SubmitField("Add Employee")

    def validate_role(self, role):
        if role.data == '':
            raise ValidationError('Please select a role')

class UpdateEmployee(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])

    # password = PasswordField('Password', validators=[DataRequired(),Length(min=8, max=20)
    # ,Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    role = SelectField('Role', validators=[DataRequired()], choices=[('','Choose a Role'),('Super_admin', 'Super_admin'),('Admin','Admin'),('Staff','Staff')])
    email = StringField("Email", validators=[DataRequired(), Length(min=2, max=50)])
    gender = RadioField('Gender', validators=[DataRequired()], choices=[('Male','Male'),('Female','Female')])
    age = IntegerField("Age", validators=[DataRequired(), NumberRange(min=18, max=100)])
    contact = StringField('Contact Number',  validators=[DataRequired(), Length(min=11, max=11)])
    address = StringField("Address", validators=[DataRequired(), Length(max=200)])
    file = FileField("Document", validators=[Optional(),  FileAllowed(['pdf'])])
    barcode = StringField("Barcode ID", validators=[DataRequired(), Length(max=48)])

    update = SubmitField("Update")

class RequestResetForm(FlaskForm):

    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None :
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):

    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=8, max=20), 
        Regexp(regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[$@!])[0-9a-zA-Z$@!]{8,}$')])

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class AttendanceForm(FlaskForm):
    lname = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Submit')

class TimeInForm(FlaskForm):

    barcode = StringField("Time In", validators=[DataRequired() , Length(min=13)])
    submit = SubmitField('Submit')

class TimeOutForm(FlaskForm):
    barcode = StringField("Time Out", validators=[DataRequired(), Length(min=13)])
    submit = SubmitField('Submit')


# https://www.youtube.com/watch?v=c-kd145l0R4&t=112s (Payroll system)
# ADD payroll sa models database for history
# ADD button den for payment history sa employee management


class PayrollForm(FlaskForm):
    full_name = StringField("Employee Name")
    payrate = IntegerField("Payrate", validators=[DataRequired(), NumberRange(min=2, max=1000)])
    tax = IntegerField('Tax %', validators=[ NumberRange(min=0, max=100)])
    month = StringField("Month")
    total_hours = FloatField("Total Hours of Work")
    total_overtime = FloatField("Total Overtime")
    gross_pay = IntegerField("Gross Pay")
    net_pay = IntegerField("Net Pay")

    submit = SubmitField('Submit')



    # total_hours = FloatField("Total Hours of Work", validators=[DataRequired()])
    # total_overtime = FloatField("Total Overtime", validators=[DataRequired()])
    # gross_pay = IntegerField("Gross Pay", validators=[NumberRange(min=2, max=50000)])
    # net_pay = IntegerField("Net Pay", validators=[NumberRange(min=2, max=50000)])



