from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
# import pyrebase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
# from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "Avricus"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iit3.db'  # Change the database URL as per your preference
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
# migrate = Migrate(app, db)

class IIT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), default="NA")

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/home")
def home():
    return render_template("index.html", contents = "Testing")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user


        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else: 
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()


        flash(f"Login Successful!!!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You are already Logged In!!!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!!!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email = email)
    else:
        flash(f"You are not logged in!!!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    else:
        flash(f"You are not logged in!!! LOGIN First ;)", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/')
def iit_list():
    if "user" in session:
        iits = IIT.query.all()
        return render_template("iit_table.html", iits = iits)
    else:
        flash(f"You are not logged in!!!")
        return redirect(url_for("login"))

def add_iit_names(iits):
    with app.app_context():
        
        # db.session.query(IIT).delete()

        for name in iits:
            iit = IIT(name = name)
            db.session.add(iit)

        db.session.commit()

@app.route("/college/<int:num>")
def dynamicRoute(num):
    if "user" in session:
        iit = IIT.query.filter_by(id=num).first()
        if iit:
            return render_template("IndiCol.html", iits=iit)
        else:
            flash(f"We dont have this College in our list!!!")
            return redirect(url_for("iit_list"))
    else:
        flash(f"You are not logged in!!!")
        return redirect(url_for("login")) 

@app.route("/addCollege")
def addCollege():
    return render_template("addCdata.html")


@app.route("/add_college", methods=["POST"])
def add_college():
    if "user" in session:
        if request.method == "POST":
            college_name = request.form["college_name"].lower()
            college_location = request.form["location"]

            existing_college = IIT.query.filter(func.lower(func.replace(IIT.name, ' ', '')) == func.lower(func.replace(college_name, ' ', ''))).first()
            
            if existing_college:
                if college_location:
                     existing_college.location = college_location
                elif existing_college.location == 'NA':
                    existing_college.location = college_location
                db.session.commit()
            else:
                if college_location:
                    iit = IIT(name=college_name, location=college_location)
                else:
                    iit = IIT(name=college_name)

                db.session.add(iit)
                db.session.commit()

            flash("College added successfully!")
            return redirect(url_for("iit_list"))
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))



if __name__ == "__main__":
   
    with app.app_context():
        db.create_all()

    # iit_names = ['IIT Bombay','IIT Delhi','IIT Madras','IIT Kanpur','IIT Kharagpur','IIT Roorkee','IIT Guwahati','IIT Hyderabad','IIT Indore','IIT Varanasi (BHU)','IIT Dhanbad','IIT Bhubaneswar','IIT Gandhinagar','IIT Ropar','IIT Patna','IIT Mandi','IIT Jodhpur','IIT Palakkad','IIT Tirupati','IIT Bhilai','IIT Goa','IIT Jammu','IIT Dharwad']
    # add_iit_names(iit_names)

    app.run(debug=True)