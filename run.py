from apscheduler.schedulers.background import BackgroundScheduler
from project import app, db
from datetime import datetime, timedelta
from project.models import User
import pytz

# two_minutes_ago = ph_now - timedelta(seconds=10)

def delete_inactive_accounts():

    ph_tz = pytz.timezone('Asia/Manila')
    ph_now = datetime.now(ph_tz)

    with app.app_context():
        five_years_ago = ph_now - timedelta(days=5*365)
        # Query all inactive accounts that were deactivated more than 5 years ago
        inactive_users = User.query.filter_by(is_active=False).filter(User.date_join < five_years_ago).all()

        if inactive_users:
            for user in inactive_users:
                db.session.delete(user)
                print(f"User {user} has been deleted.")
            db.session.commit()
        else:
            print("No inactive users found.")


scheduler = BackgroundScheduler()

if __name__ == '__main__':
    scheduler.add_job(func=delete_inactive_accounts, trigger='cron', hour=0, minute=0)
    # scheduler.add_job(id='delete_inactive_accounts', func=delete_inactive_accounts, trigger='interval', seconds = 5)
    scheduler.start()
    app.run(debug=True) #Don't Forget to turn off
