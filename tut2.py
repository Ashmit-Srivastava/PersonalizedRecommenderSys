import os
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta, datetime
# import pyrebase
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.orm import relationship
import pandas as pd
import uuid
# from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "Avricus"
app.permanent_session_lifetime = timedelta(hours=5)
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
    uuid = db.Column(db.String(36), unique=True, nullable=False)
    timestamp = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.uuid = str(uuid.uuid4())
        self.timestamp = ""

    def add_login_timestamp(self, source=None):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.timestamp:
            self.timestamp = f"{now}"
            
        else:
            self.timestamp = now

        if source == 'login':
            self.update_login_logs_file()  # Update the login log file
                

    def get_login_timestamps(self):
        return self.timestamp.split(",") if self.timestamp else []

    def update_login_logs_file(self):
        logs_file_path = os.path.join(os.path.dirname(__file__), "Logs/logs.txt")
        with open(logs_file_path, "a") as file:
            file.write(f"{self.name}: {self.get_login_timestamps()}\nEmail: {self.email}\n")
            

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name



@app.route("/home")
def home():
    return render_template("index.html", contents = "Testing")

@app.route("/view")
def view_logs():
    email = session.get("email", "")
    logs_file_path = os.path.join(app.root_path, "Logs/logs.txt")
    with open(logs_file_path, "r") as file:
        log_content = file.read()

    return render_template("view.html", log_content=log_content, email=email)

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user

        email = request.form["email"]
        session["email"] = email


        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else: 
            found_user = users(name=user, email=email)
            db.session.add(found_user)
            db.session.commit()
            
        # Update the timestamp and save the details
        found_user.add_login_timestamp('login')
        db.session.commit()
        

        flash(f"Login Successful!!!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash(f"You are already Logged In!!!")
            return redirect(url_for("user"))
        
        return render_template("login.html")

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!!!")
        else:
            if "email" in session:
                email = session["email"]

        return render_template("user.html", email=email)
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


@app.route("/college/<int:num>")
def dynamicRoute(num):
    if "user" in session:
        iit = IIT.query.filter_by(id=num).first()
        if iit:
            return render_template("IndiCol.html", iits=iit)
        else:
            flash(f"We dont have this College in our database!!!")
            return render_template("error.html", error_message="Page not found", back_url=url_for("iit_list"))
    else:
        flash(f"You are not logged in!!!")
        return redirect(url_for("login")) 

@app.errorhandler(404)
def page_not_found(error):
    
    return render_template('error.html', error_message="Page not found", back_url=url_for('iit_list')), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error.html", error_message="Internal Server Error", back_url=url_for("iit_list")), 500

@app.route("/addCollege")
def addCollege():
    states = City.query.all()
    return render_template("addCdata.html", states=states)


def update_crud_logs_file(user, email, data_dict, operation):
    log_entry = f"The User has performed a {operation} Operation. User: {user}, Email: {email}, Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, College Name: {data_dict['college_name']}, College Location: {data_dict['college_location']}\n\n"
    log_file_path = os.path.join(os.path.dirname(__file__), "Logs/CRUDlog.txt")
    with open(log_file_path, "a") as file:
        file.write(log_entry)


@app.route("/add_college", methods=["POST"])
def add_college():
    if "user" in session:
        if request.method == "POST":
            college_name = request.form["college_name"]
            college_location = request.form["location"]
            

            if college_location:
                # Use the selected city from the dropdown
                location = college_location
            else:
                # No location specified
                location = None

            existing_college = IIT.query.filter(func.lower(func.replace(IIT.name, ' ', '')) == func.lower(func.replace(college_name, ' ', ''))).first()
            if existing_college:
                existing_college.location = location
                db.session.commit()
                data_dict = {'college_name':college_name, 'college_location':college_location}
                update_crud_logs_file(user=session["user"], email=session["email"], data_dict=data_dict, operation='Update')  #CRUD Operations log file update
            else:
                iit = IIT(name=college_name, location=location)
                db.session.add(iit)
                db.session.commit()
                data_dict = {'college_name':college_name, 'college_location':college_location}
                update_crud_logs_file(user=session["user"], email=session["email"], data_dict=data_dict, operation='Create')  #CRUD Operations log file update

            
            flash("College added/updated successfully!")
            return redirect(url_for("iit_list"))
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


@app.route("/populate_cities")
def populate_cities():
    existing_states = City.query.all()

    df = pd.read_excel("C:/Users/ashmi/OneDrive/Desktop/Avricus PS1/Flask/cities/states.xlsx")
    states = df["State"].tolist()

    # Remove existing states from the database
    for state in existing_states:
        db.session.delete(state)

    # Add the new states
    for state in states:
        db.session.add(City(name=state))

    db.session.commit()
    flash("States updated successfully!")
    return redirect(url_for("addCollege"))



if __name__ == "__main__":
   
    with app.app_context():
        db.create_all()

    app.run(debug=True)