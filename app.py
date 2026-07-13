from flask import Flask,render_template,redirect,url_for,request,session
from models import db,User,Booking,Trek
from config import Config
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,date

app=Flask(__name__)
app.config.from_object(Config)
app.secret_key=Config.SECRET_KEY
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
    else:
        print("Admin already exists")

@app.route("/")
def homepage():
    return render_template("home-page.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        email=request.form.get("email")
        password=request.form.get("password")

        user=User.query.filter_by(email=email).first()
        if user is None:
            return "Invalid Email"
        elif not user.approved:
            return "Your account is not approved"
        elif user.blacklisted:
            return "Your account is blacklisted"
        else:
            if not check_password_hash(user.password,password):
                return "Invalid Password"
            else:
                session["user_id"]=user.user_id
                session["role"]=user.role
                if user.role=="admin":
                    return redirect(url_for("admin"))
                elif user.role=="staff":
                    return redirect(url_for("staff"))
                elif user.role=="trekker":
                    return redirect(url_for("trekker"))
                else:
                    return "You are not logged in"
           
@app.route("/admin")
def admin():
    if session.get("role")!="admin":
        return "You are not an Admin"
    total_trekkers=User.query.filter_by(role="trekker").count()
    total_staff=User.query.filter_by(role="staff").count()
    total_treks=Trek.query.count()
    total_bookings=Booking.query.count()
    return render_template("dashboard/admin.html",total_trekkers=total_trekkers,total_staff=total_staff,total_treks=total_treks,total_bookings=total_bookings)

@app.route("/staff")
def staff():
    if session.get("role")!="staff":
        return "You are not staff"
    user_id=session["user_id"]
    treks=Trek.query.filter_by(assigned_staff_id=user_id).all()
    total_treks=len(treks)
    trekkers=Booking.query.all()
    participants=[]
    for trekker in trekkers:
        for trek in treks:
            if trekker.trek_id==trek.trek_id:
                participants.append(trekker)
    total_trekkers=len(participants)
    return render_template("dashboard/staff.html",total_treks=total_treks,total_trekkers=total_trekkers)

@app.route("/trekker")
def trekker():
    if session.get("role")!="trekker":
        return "You are not a trekker"
    return render_template("dashboard/trekker.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        name=request.form.get("name")
        email=request.form.get("email")
        contact=request.form.get("contact")
        password=request.form.get("password")
        confirm_password=request.form.get("confirm_password")
        role=request.form.get("role")
        if password!=confirm_password:
            return "Passwords do not match"
        existinguser=User.query.filter_by(email=email).first()
        if existinguser is not None:
            return "Email already exists"
        hashed_password=generate_password_hash(password)
        if role=="staff":
            approved=False
        else:
            approved=True
        user=User(
            name=name,
            email=email,
            password=hashed_password,
            contact=contact,
            role=role,
            approved=approved,
            blacklisted=False
        )
        db.session.add(user)
        db.session.commit()
        if approved==True:
            return redirect(url_for("login"))
        else:
            return "Your approval is pending."
        
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("homepage"))

@app.route("/add-trek",methods=["GET","POST"])
def addtrek():
    if session.get("role")!="admin":
        return "You are not the Admin"
    if request.method=="GET":
        return render_template("admin/add-trek.html")
    else:
        name=request.form.get("name")
        location=request.form.get("location")
        difficulty=request.form.get("difficulty")
        duration=request.form.get("duration")
        available_slots=request.form.get("available_slots")
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")
        today=date.today()
        start_date=datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date=datetime.strptime(end_date,"%Y-%m-%d").date()
        if start_date>end_date:
            return "Start date cannot be after end date"
        duration=int(duration)
        available_slots=int(available_slots)
        days=(end_date-start_date).days+1
        if days!=duration:
            return "Trip duration and date gaps don't match."
        if available_slots<=0:
            return "Minimum slots should be 1."
        if today>=end_date:
            trek=Trek(
                name=name,
                location=location,
                difficulty=difficulty,
                duration=duration,
                available_slots=available_slots,
                assigned_staff_id=None,
                status="complete",
                start_date=start_date,
                end_date=end_date
                )
            db.session.add(trek)
            db.session.commit()
            return redirect(url_for("viewtrek"))
        trek=Trek(
            name=name,
            location=location,
            difficulty=difficulty,
            duration=duration,
            available_slots=available_slots,
            assigned_staff_id=None,
            status="upcoming",
            start_date=start_date,
            end_date=end_date
        )        
        db.session.add(trek)
        db.session.commit()
        return redirect(url_for("viewtrek"))
    
@app.route("/view-treks")
def viewtrek():
    if session.get("role")!="admin":
        return "You are not the Admin"
    treks=Trek.query.all()
    return render_template("admin/view-treks.html",treks=treks)

@app.route("/edit-trek/<int:trek_id>",methods=["GET","POST"])
def edittrek(trek_id):
    if session.get("role")!="admin":
        return "You are not the Admin"
    trek_to_edit=Trek.query.filter_by(trek_id=trek_id).first()
    if trek_to_edit==None:
        return "Invalid Trek ID"
    if request.method=="GET":
        return render_template("admin/edit-trek.html",trek=trek_to_edit)
    else:
        name=request.form.get("name")
        location=request.form.get("location")
        difficulty=request.form.get("difficulty")
        duration=request.form.get("duration")
        available_slots=request.form.get("available_slots")
        assigned_staff_id=request.form.get("assigned_staff_id")
        status=request.form.get("status")
        start_date=request.form.get("start_date")
        end_date=request.form.get("end_date")

        start_date=datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date=datetime.strptime(end_date,"%Y-%m-%d").date()
        if start_date>end_date:
            return "Start date cannot be after end date"
        duration=int(duration)
        available_slots=int(available_slots)
        days=(end_date-start_date).days+1
        if days!=duration:
            return "Trip duration and date gaps don't match."
        if available_slots<=0:
            return "Minimum slots should be 1."
        trek_to_edit.name=name
        trek_to_edit.location=location
        trek_to_edit.difficulty=difficulty
        trek_to_edit.duration=duration
        trek_to_edit.available_slots=available_slots
        if assigned_staff_id=="":
            trek_to_edit.assigned_staff_id=None
        else:
            trek_to_edit.assigned_staff_id=assigned_staff_id
        trek_to_edit.status=status
        trek_to_edit.start_date=start_date
        trek_to_edit.end_date=end_date     
        db.session.commit()
        return redirect(url_for("viewtrek"))

@app.route("/delete-trek/<int:trek_id>")
def deletetrek(trek_id):
    if session.get("role")!="admin":
        return "You are not the Admin"
    trek=Trek.query.filter_by(trek_id=trek_id).first()
    if trek is None:
        return "Invalid Trek ID"
    db.session.delete(trek)
    db.session.commit()
    return redirect(url_for("viewtrek"))

@app.route("/view-staff")
def viewstaff():
    if session.get("role")!="admin":
        return "You are not the Admin"
    staffs=User.query.filter_by(role="staff").all()
    return render_template("admin/view-users.html",users=staffs)

@app.route("/view-trekkers")
def viewtrekkers():
    if session.get("role")!="admin":
        return "You are not the Admin"
    trekkers=User.query.filter_by(role="trekker").all()
    return render_template("admin/view-users.html",users=trekkers)

@app.route("/approvestatus/<int:user_id>")
def approvestatus(user_id):
    if session.get("role")!="admin":
        return "You are not the Admin"
    user=User.query.filter_by(user_id=user_id).first()
    if user is None:
        return "Invalid User ID"
    user.approved=not user.approved
    db.session.commit()
    return redirect(request.referrer)

@app.route("/blackliststatus/<int:user_id>")
def blackliststatus(user_id):
    if session.get("role")!="admin":
        return "You are not the Admin"
    user=User.query.filter_by(user_id=user_id).first()
    if user is None:
        return "Invalid User ID"
    user.blacklisted=not user.blacklisted
    db.session.commit()
    return redirect(request.referrer)

@app.route("/view-bookings")
def viewbookings():
    if session.get("role")!="admin":
        return "You are not the Admin"
    bookings=Booking.query.all()
    return render_template("admin/view-bookings.html",bookings=bookings)

@app.route("/available-treks")
def available_treks():
    if session.get("role")=="admin":
        return "You are the Admin"
    available_treks=Trek.query.filter_by(status="upcoming").all()
    return render_template("trekker/available-treks.html",treks=available_treks)

@app.route("/book-trek/<int:trek_id>")
def booktrek(trek_id):
    if session.get("role")!="trekker":
        return "You are not a trekker"
    trek=Trek.query.filter_by(trek_id=trek_id).first()
    if trek is None:
        return "Invalid Trek ID"
    user_id=session["user_id"]
    bookings=Booking.query.filter_by(user_id=user_id).all()
    for booking in bookings:
        if booking.trek_id==trek_id:
            if booking.status=="Booked":
                return "You have already booked for this trek."
            else:
                if trek.available_slots>0:
                    book=Booking(
                        user_id=user_id,
                        trek_id=trek_id,
                        booking_date=date.today(),
                        status="Booked"
                        )
                    db.session.add(book)
                    trek.available_slots-=1
                    db.session.commit()
                    return redirect(url_for("bookedtreks"))
                else:
                    return "No slots available."
        
@app.route("/booked-treks")
def bookedtreks():
    if session.get("role")!="trekker":
        return "You are not a trekker"
    user_id=session["user_id"]
    bookedtreks=Booking.query.filter_by(user_id=user_id,status="Booked").all()
    all_treks=Trek.query.all()
    treks=[]
    for trek in all_treks:
        for bookedtrek in bookedtreks:
            if trek.trek_id==bookedtrek.trek_id:
                treks.append(trek)
    if treks==[]:
        return "No existing bookings"
    return render_template("trekker/booked-treks.html",treks=treks)

@app.route("/cancel-booking/<int:trek_id>")
def cancelbooking(trek_id):
    user_id=session["user_id"]
    bookings=Booking.query.filter_by(user_id=user_id,status="Booked").all()
    trek=Trek.query.filter_by(trek_id=trek_id).first()
    for booking in bookings:
        if booking.trek_id==trek_id:
            booking.status="Not booked"
            trek.available_slots+=1
            db.session.commit()
            return redirect(url_for("bookedtreks"))
    return "Booking not found"
            
@app.route("/search-ppl",methods=["POST"])
def searchuser():
    if session.get("role")!="admin":
        return "You are not the Admin"
    value=request.form.get("value")
    if value.isdigit():
        user=User.query.filter_by(user_id=int(value)).all()
    else:
        user=User.query.filter_by(name=value).all()
    return render_template("admin/search-ppl.html",users=user)

@app.route("/search-trek",methods=["POST"])
def searchtrek():
    if session.get("role")!="admin":
        return "You are not the Admin"
    value=request.form.get("value")
    if value.isdigit():
        trek=Trek.query.filter_by(trek_id=int(value)).all()
    else:
        trek=Trek.query.filter_by(name=value).all()
    return render_template("admin/search-trek.html",treks=trek)

@app.route("/assigned-treks")
def assignedtreks():
    if session.get("role")!="staff":
        return "You are not a staff member"
    user_id=session["user_id"]
    treks=Trek.query.filter_by(assigned_staff_id=user_id).all()
    return render_template("staff/assigned-treks.html",treks=treks)

@app.route("/view-participants/<int:trek_id>")
def viewparticipants(trek_id):
    if session.get("role")!="staff":
        return "You are not a staff member"
    user_id=session["user_id"]
    trek=Trek.query.filter_by(assigned_staff_id=user_id,trek_id=trek_id).first()
    if trek is None:
        return "Invalid Trek"
    bookings=Booking.query.filter_by(trek_id=trek.trek_id).all()
    participants=[]
    for booking in bookings:
        user=User.query.filter_by(user_id=booking.user_id).first()
        participants.append(user)
    if participants==[]:
        return "No participants in this trek"
    return render_template("staff/participants.html",participants=participants)

@app.route("/edit-trek-slots/<int:trek_id>",methods=["GET","POST"])
def edittrekslots(trek_id):
    trek=Trek.query.filter_by(trek_id=trek_id).first()
    if trek is None:
        return "Invalid Trek"
    if request.method=="GET":
        return render_template("staff/edit-trek-slots.html",trek_id=trek_id)
    else:
        slots=request.form.get("slots")
        trek.available_slots=int(slots)
        db.session.commit()
        return redirect(url_for("assignedtreks"))

@app.route("/edit-trek-status/<int:trek_id>",methods=["GET","POST"])
def edittrekstatus(trek_id):
    trek=Trek.query.filter_by(trek_id=trek_id).first()
    if trek is None:
        return "Invalid Trek"
    if request.method=="GET":
        return render_template("staff/edit-trek-status.html",trek_id=trek_id)
    else:
        status=request.form.get("status")
        trek.status=status
        db.session.commit()
        return redirect(url_for("assignedtreks"))
    
@app.route("/update-profile",methods=["GET","POST"])
def updateprofile():
    if session.get("role")=="admin":
        return "You are an admin"
    user_id=session["user_id"]
    user=User.query.filter_by(user_id=user_id).first()
    if user is None:
        return "Invalid Attempt"
    if request.method=="GET":
        return render_template("staff/update-profile.html")
    name=request.form.get("name")
    email=request.form.get("email")
    contact=request.form.get("contact")
    user.name=name
    user.email=email
    user.contact=contact
    db.session.commit()
    return redirect(request.referrer)

@app.route("/trek-history")
def trekhistory():
    user_id=session["user_id"]
    if session.get("role")!="trekker":
        return "You are not a trekker"
    today = date.today()
    completed_bookings=db.session.query(Booking).join(Trek).filter(Booking.user_id==user_id,Booking.status!="Not booked",Trek.end_date<today).all()
    for booking in completed_bookings:
        booking.status="Booked"
    db.session.commit()
    return render_template("trekker/completed-treks.html",treks=completed_bookings)

@app.route("/trekker-search-trek",methods=["POST"])
def trekkersearchtrek():
    if session.get("role")!="trekker":
        return "You are not a trekker"
    location=request.form.get("location")
    difficulty=request.form.get("difficulty")
    treks=Trek.query.filter_by(location=location,difficulty=difficulty).all()
    return render_template("trekker/search-treks.html",treks=treks)

if __name__=="__main__":
    app.run(debug=True)