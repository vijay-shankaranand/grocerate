import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///grocerate.db")

@app.route("/")
@login_required
def index():
    """Show available pickups"""

    pickups = db.execute("SELECT food,address,time FROM transactions")

    return render_template("index.html", pickups = pickups)


@app.route("/mine")
@login_required
def myposts():

    pickups = db.execute("SELECT food,address,time,remarks FROM transactions where userid = ?",session["user_id"])

    return render_template("mine.html", pickups = pickups)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must Provide Username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must Provide Password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid Username And/Or Password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add Post."""
    if request.method == "POST":
        if not request.form.get("food"):
            return apology("Provide Valid Title", 400)
        if not request.form.get("address"):
            return apology("Provide Valid Location", 400)
        if not request.form.get("contact").isdigit():
            return apology("Provide Valid Contact Nummber", 400)
        if not request.form.get("remarks"):
            return apology("Provide Valid Description", 400)
        else:
            name = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["fullname"]
            db.execute("INSERT INTO transactions (userid,food,address,contact,remarks,name) VALUES (?,?,?,?,?,?)", session["user_id"] , request.form.get("food") , request.form.get("address"), request.form.get("contact"), request.form.get("remarks"),name)

        flash('Post Added!')
        return redirect("/")
    else:
        return render_template("add.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
         # Ensure username was submitted
        if not request.form.get("fullname"):
            return apology("Must Provide Fullname", 400)

        if not request.form.get("username"):
            return apology("Must Provide Username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must Provide Password", 400)

        elif not request.form.get("confirmation"):
            return apology("Must Re-Enter Password", 400)

        elif not request.form.get("password") == request.form.get("confirmation"):
            return apology("Passwords Do Not Match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) != 1:
            newuser = db.execute("INSERT INTO users(fullname,username,hash) VALUES(?,?,?)",request.form.get("fullname"),request.form.get("username"),generate_password_hash(request.form.get("password")))
            session["user_id"] = newuser
            flash("Registration Sucessful!")
            return redirect("/")

        else:
            return apology("Username Has Already Been Taken",400)

    else:
        return render_template("register.html")




@app.route("/delete", methods=["POST"])
@login_required
def delete():
    """remove post"""

    db.execute("DELETE FROM transactions WHERE userid = ? AND food = ?",session["user_id"], request.form.get("foods"))

    return redirect("/")

@app.route("/info", methods=["POST"])
@login_required
def info():
    """more info on the particular post"""

    informations = db.execute("SELECT food,address,time,remarks,name,contact FROM transactions WHERE time = ?", request.form.get("times"))

    return render_template("info.html", informations = informations)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
