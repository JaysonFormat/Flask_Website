from project import db, app
from project.models import User, Employee

app.app_context().push()

person = input("Who is going to be admin? (Use Email Address) : ")

user = User.query.filter_by(email=person).first()

decide = input("Do you want to be a admin? YES OR NO: ")

if decide == "yes":
    user.role = "Super_admin"
    employee.is_admin = True
else:
    user.role = "Customer"


db.session.commit()

print('EDIT COMPLETE!!')