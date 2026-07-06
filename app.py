from flask import Flask
from models import db,User,Booking,Trek
from config import Config
from werkzeug.security import generate_password_hash

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    existing_admin=User.query.filter_by(email="admin@trek.com").first()
    if existing_admin is None:
        admin=User(user_id=1,
                   name="Admin",
                   email="admin@trek.com",
                   password=generate_password_hash("admin123"),
                   contact="+918858077433",
                   role="admin",
                   approved=True,
                   blacklisted=False)
        db.session.add(admin)
        db.session.commit()
        print("Default admin created")
    else:
        print("Admin already exists")

if __name__=="__main__":
    app.run(debug=True)