import datetime
from flask import Flask, request, render_template, escape
import hashlib

app = Flask(__name__)

adminusername = "admin"
adminpasshash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"


@app.route("/")
def index():
    entry = request.values.get("log")
    if entry:
        entry = f"[{datetime.datetime.now()}: log entry from {request.remote_addr}] {entry}\n"
        log(entry)
        return ""
    else:
        return render_template("logger.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    username = request.values.get("username")
    password = request.values.get("password")
    if username or password:
        if username == adminusername and hashlib.sha256(password.encode("utf-8")).hexdigest() == adminpasshash:
            with open("log.txt") as f:
                data = f.read()
                return render_template("viewer.html", html=escape(data))
        else:
            return "Invalid username or password."
    else:
        return render_template("view.html")


def log(data):
    with open("log.txt", "a") as f:
        f.write(data)


app.run("localhost", 8000)
