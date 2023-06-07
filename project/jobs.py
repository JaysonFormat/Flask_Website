from datetime import datetime, timedelta
from project.models import User
from project import db

def delete_inactive_accounts():
    
    # five_years_ago = datetime.utcnow() - timedelta(days=5*365)
    five_minutes_ago = datetime.utcnow() - timedelta(minutes = 5)

    # Query all inactive accounts that were deactivated more than 5 years ago
    inactive_users = User.query.filter_by(is_active=False).filter(User.deactivated_time < five_minutes_ago).all()

    # Delete all inactive accounts that were deactivated more than 5 years ago
    for user in inactive_users:
        print("User Deleted in the database")
        db.session.delete(user)

    db.session.commit()
