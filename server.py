# pylint: disable-all

from flask import Flask, request, render_template
import hashlib
from markupsafe import escape
import logger
import sessions

app = Flask(__name__)

admin_username = "admin"
admin_pass_hash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
json_path = "log.json"
log = logger.Logger()
manager = sessions.SessionManager()
try:
    log.load_json(json_path)
except:
    pass


@app.route("/")
def index():
    entry = request.values.get("log")
    id = request.values.get("id")
    if entry:
        log.append_log(data=entry, source_ip=request.remote_addr, id=id)
        log.dump_json(json_path)
        return render_template("text.html", text="WebLog Submitted")
    else:
        return render_template("index.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    username = request.values.get("username")
    password = request.values.get("password")
    if username or password:
        if username == admin_username and hashlib.sha256(password.encode("utf-8")).hexdigest() == admin_pass_hash:
            key = manager.get_key()
            return render_template("view.html", html=escape(str(log)), key=key)
        else:
            return render_template("text.html", text="Invalid username or password.")
    else:
        return render_template("login.html")


app.run("localhost", 8003)
