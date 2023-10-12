# pylint: disable-all

import datetime
from flask import Flask, request, render_template
import hashlib
from markupsafe import escape
import json

app = Flask(__name__)

adminusername = "admin"
adminpasshash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"


@app.route("/")
def index():
    entry = request.values.get("log")
    if entry:
        log(entry, request.remote_addr)
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


def log(data, remote_ip):
    with open("log.json", "r") as f:
        try:
            json_data = json.loads(f.read())
        except json.JSONDecodeError as e:
            print(e)
            print("New json log...")
            json_data = {}
        if not json_data.get(remote_ip):
            json_data[remote_ip] = {}
        json_data[remote_ip][str(datetime.datetime.now())] = data;
    with open("log.json", "w") as f:
        f.write(json.dumps(json_data))
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.datetime.now()}: log entry from {remote_ip}] {data}\n")


app.run("localhost", 8003)
