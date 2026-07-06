from app import app
from models import db,User,Trek,Booking
from werkzeug.security import check_password_hash,generate_password_hash
from flask import render_template, url_for, request, redirect, session

@app.route('/')
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
           
@app.route("/admin")
def admin():
    return render_template("dashboard/admin.html")

@app.route("/staff")
def staff():
    return render_template("dashboard/staff.html")

@app.route("/trekker")
def trekker():
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

