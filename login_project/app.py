from flask import Flask, render_template, request, redirect, session
import csv
import re

app = Flask(__name__)
app.secret_key = "secret123"

def validate_password(password):

    if len(password) < 6:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True

def save_user(username, password):

    with open("users.csv", "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([username, password])

def username_exists(username):

    with open("users.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:

            if row and row[0] == username:
                return True

    return False

def check_login(username, password):

    with open("users.csv", "r") as file:

        reader = csv.reader(file)

        for row in reader:

            if row and row[0] == username and row[1] == password:
                return True

    return False

@app.route("/")
def home():
    return "Hello Internship Project"

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if not validate_password(password):
            return """
            Password must:
            <br>- Be at least 6 characters
            <br>- Contain one capital letter
            <br>- Contain one number
            """
        if username_exists(username):
            return "Username already exists"
        

        save_user(username, password)

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if check_login(username, password):
            session["user"] = username
            return redirect("/role")

        return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/role", methods=["GET", "POST"])
def role():
    if "user" not in session:
        return redirect("/login")
    
    if request.method == "POST":

        selected_role = request.form["role"]

        return redirect(f"/welcome/{selected_role}")

    return render_template("role.html")

@app.route("/welcome/<role>")
def welcome(role):

    if "user" not in session:
        return redirect("/login")

    return render_template("welcome.html", role=role)
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)