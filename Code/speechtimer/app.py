import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_httpauth import HTTPBasicAuth
import threading
import time
import os
import shutil
import logging 
from flask import jsonify

logging.getLogger("eventlet.wsgi").setLevel(logging.ERROR)  
logging.getLogger("engineio").setLevel(logging.WARNING) 

app = Flask(__name__)
socketio = SocketIO(app)
auth = HTTPBasicAuth()

# Admin-Zugangsdaten
users = {
    "admin": "password123"
}

@auth.get_password
def get_pw(username):
    return users.get(username)

# Timer-Statusvariablen
current_time = 0
timer_running = False
allow_overtime = False
last_set_time = 0
timer_thread = None

# Verbindungsverwaltung
connected_clients = set()

def countdown():
    global current_time, timer_running, allow_overtime
    while timer_running:
        time.sleep(1)
        if not timer_running:
            break
        if current_time == 0 and not allow_overtime:
            timer_running = False
            break
        current_time -= 1
        socketio.emit("update_time", current_time)

# Flask-Routen
@app.route("/")
def index():
    return render_template("speechtimer.html")

@app.route("/admin")
@auth.login_required
def admin():
    return render_template("admin.html")

# Socket.IO Events
@socketio.on("start_timer")
def start_timer():
    global timer_running, timer_thread
    if not timer_running:
        timer_running = True
        timer_thread = threading.Thread(target=countdown)
        timer_thread.start()

@socketio.on("stop_timer")
def stop_timer():
    global timer_running
    timer_running = False

@socketio.on("request_current_time")
def send_current_time():
    emit("update_time", current_time, room=request.sid)
    emit("show_stop_message", "", room=request.sid)
    emit("show_fullscreen_message", "", room=request.sid)
    emit("show_fullscreen_image", "", room=request.sid)
    emit("toggle_clock", False, room=request.sid)



@socketio.on("reset_timer")
def reset_timer():
    global current_time, last_set_time, timer_running
    timer_running = False
    current_time = last_set_time
    socketio.emit("update_time", current_time)
    socketio.emit("show_fullscreen_message", "")   # Vollbild-Nachricht leeren
    socketio.emit("show_stop_message", "")          # Hinweistext leeren
    socketio.emit("show_fullscreen_image", "")      # Bild ausblenden


@socketio.on("set_time")
def set_time(minutes):
    global current_time, last_set_time, timer_running
    timer_running = False
    time.sleep(0.05)  # kurz warten zum Stoppen des Threads
    current_time = int(round(minutes * 60))
    last_set_time = current_time
    socketio.emit("update_time", current_time)

@socketio.on("set_overtime")
def set_overtime(allowed):
    global allow_overtime
    allow_overtime = allowed

@socketio.on("show_stop_message")
def show_stop_message(message):
    socketio.emit("show_stop_message", message)

@socketio.on("show_fullscreen_message")
def show_fullscreen_message(message):
    socketio.emit("show_fullscreen_message", message)

@socketio.on("show_fullscreen_image")
def show_fullscreen_image(url):
    socketio.emit("show_fullscreen_image", url)

@socketio.on("toggle_clock")
def toggle_clock(show):
    socketio.emit("toggle_clock", show)

# Timerverbindung wird signalisiert
@socketio.on("timer_connected")
def handle_timer_connected():
    connected_clients.add(request.sid)
    socketio.emit("timer_status", {"connected": True})

# Verbindung trennt sich
@socketio.on("disconnect")
def handle_disconnect():
    connected_clients.discard(request.sid)
    is_online = len(connected_clients) > 0
    socketio.emit("timer_status", {"connected": is_online})

@socketio.on("adjust_time")
def handle_adjust_time(delta):
    global current_time
    current_time += int(delta)
    if current_time < 0:
        current_time = 0
    socketio.emit("update_time", current_time)

@socketio.on("request_timer_status")
def handle_request_timer_status():
    is_online = len(connected_clients) > 0
    emit("timer_status", {"connected": is_online})


@app.route("/replace-images", methods=["POST"])
@auth.login_required
def replace_images():
    usb_path = "/media/usb"
    image_dir = os.path.join("static", "images")
    expected_files = ["image1.jpg", "image2.jpg", "image3.jpg"]

    try:
        found = all(os.path.isfile(os.path.join(usb_path, f)) for f in expected_files)
        if found:
            for filename in expected_files:
                shutil.copy(os.path.join(usb_path, filename), os.path.join(image_dir, filename))
            return jsonify({"status": "success", "message": "Bilder erfolgreich ersetzt."})
        else:
            return jsonify({"status": "error", "message": "Nicht alle Bilder gefunden."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500




if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=55055)
