# Speechtimer 1.1.5 · Peter Aellig
# app.py

# wenn für eine weitere Instanz eine APP Kopie erstellt wird,
# muss INSTANCE_ID  um eins erhäht werden


import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_httpauth import HTTPBasicAuth
import threading
import time
import os
import shutil
import logging


# 1. Konfiguration & Hilfsfunktionen

# ========================================
INSTANCE_ID = 1  # <---- Nur diese Zeile muss in app2.py auf 2 gesetzt werden!
# ========================================


password_protection = True  # Auf False setzen, wenn keine Authentifizierung nötig oder gewünscht ist
api_enabled = True  # Auf False setzen, um API-Aufrufe zu deaktivieren

# Portnummern werden automatisch angepasst aufgrund der INSTANCE_ID
# hier wird die erste Portnummer 55055 sein (55054 plus 1)
BASE_PORT = 55054 # <---- Port ändern, falls andere Portnummern gewünscht wären!
PORT = BASE_PORT + INSTANCE_ID  # z.B. 55055 für ID=1, 55056 für ID=2

def get_room_name_filename():
    return f"roomname{INSTANCE_ID}.txt"

def load_room_name():
    try:
        with open(get_room_name_filename(), "r") as f:
            content = f.read().strip()
            if content:
                return content
            else:
                raise ValueError("Room name file is empty.")
    except:
        return f"Room{INSTANCE_ID}"  # Dynamischer Fallback


def save_room_name(name):
    with open(get_room_name_filename(), "w") as f:
        f.write(name.strip())

def get_default_time_filename():
    return f"default_time_{INSTANCE_ID}.txt"

def save_default_time(minutes):
    with open(get_default_time_filename(), "w") as f:
        f.write(str(minutes))

def load_default_time():
    try:
        with open(get_default_time_filename(), "r") as f:
            return int(f.read().strip())
    except:
        return 12  # Fallback-Wert in Minuten

# 2. Flask App Initialisierung
# ========================================

logging.getLogger("eventlet.wsgi").setLevel(logging.ERROR)
logging.getLogger("engineio").setLevel(logging.WARNING)

app = Flask(__name__)
app.debug = True  
APP_INSTANCE_NAME = load_room_name()
socketio = SocketIO(app)
auth = HTTPBasicAuth()

if not password_protection:
    def no_auth_decorator(f):
        return f
    auth.login_required = no_auth_decorator


# 3. Authentifizierung
# ========================================

users = {
    "admin": "password123"
}

@auth.get_password
def get_pw(username):
    return users.get(username)

# 4. Globale Timer-Statusvariablen
# ========================================

current_time = 0
timer_running = False
allow_overtime = False
last_set_time = load_default_time() * 60
timer_thread = None
connected_clients = set()

# 5. Timer-Countdown-Logik
# ========================================

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

# 6. Flask-Routen
# ========================================

@app.route("/")
def index():
    return render_template("speechtimer.html")

@app.route("/admin")
@auth.login_required
def admin():
    return render_template("admin.html", instance_name=APP_INSTANCE_NAME)

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


@app.route("/reboot", methods=["POST"])
@auth.login_required
def reboot_device():
    try:
        # Optional: Logdatei schreiben oder Nachricht senden
        threading.Thread(target=lambda: os.system("sudo reboot")).start()
        return jsonify({"status": "success", "message": "Rebooting..."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api", methods=["GET"])
def api_control():
    if not api_enabled:
        return jsonify({"status": "error", "message": "API-Zugriff ist deaktiviert."}), 403

    function = request.args.get("Function", "").lower()
    value = request.args.get("Value")

    if function == "settime":
        try:
            minutes = float(value)
            set_time(minutes)
            return jsonify({"status": "ok", "message": f"Time set to {minutes} min."})
        except:
            return jsonify({"status": "error", "message": "Ungültiger Zeitwert."}), 400

    elif function == "start":
        start_timer()
        return jsonify({"status": "ok", "message": "Timer gestartet."})

    elif function == "stop":
        stop_timer()
        return jsonify({"status": "ok", "message": "Timer gestoppt."})

    elif function == "reset":
        reset_timer()
        return jsonify({"status": "ok", "message": "Timer zurückgesetzt."})

    elif function == "adjust":
        try:
            seconds = int(value)
            handle_adjust_time(seconds)
            return jsonify({"status": "ok", "message": f"{seconds} Sekunden hinzugefügt."})
        except:
            return jsonify({"status": "error", "message": "Ungültiger Wert für Adjust."}), 400

    else:
        return jsonify({"status": "error", "message": "Unbekannte Funktion."}), 400




# 7. Socket.IO Events – Timersteuerung
# ========================================

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

@socketio.on("reset_timer")
def reset_timer():
    global current_time, last_set_time, timer_running
    if not timer_running:
        current_time = last_set_time
        socketio.emit("update_time", current_time)
        socketio.emit("show_fullscreen_message", "")
        socketio.emit("show_stop_message", "")
        socketio.emit("show_fullscreen_image", "")

@socketio.on("set_time")
def set_time(minutes):
    global current_time, last_set_time
    if not timer_running:
        current_time = int(round(minutes * 60))
        last_set_time = current_time
        socketio.emit("update_time", current_time)

@socketio.on("set_default_time")
def handle_set_default_time(minutes):
    global last_set_time
    save_default_time(int(minutes))
    last_set_time = int(minutes) * 60
    if not timer_running:
        current_time = last_set_time
        socketio.emit("update_time", current_time)


@socketio.on("set_overtime")
def set_overtime(allowed):
    global allow_overtime
    allow_overtime = allowed

@socketio.on("adjust_time")
def handle_adjust_time(delta):
    global current_time
    current_time += int(delta)
    if current_time < 0:
        current_time = 0
    socketio.emit("update_time", current_time)

# 8. Socket.IO Events – Verbindung / Status
# ========================================

@socketio.on("timer_connected")
def handle_timer_connected():
    connected_clients.add(request.sid)
    socketio.emit("timer_status", {"connected": True})

@socketio.on("disconnect")
def handle_disconnect():
    connected_clients.discard(request.sid)
    is_online = len(connected_clients) > 0
    socketio.emit("timer_status", {"connected": is_online})

@socketio.on("request_timer_status")
def handle_request_timer_status():
    is_online = len(connected_clients) > 0
    emit("timer_status", {"connected": is_online})

@socketio.on("request_current_time")
def send_current_time():
    emit("update_time", current_time, room=request.sid)
    emit("show_stop_message", "", room=request.sid)
    emit("show_fullscreen_message", "", room=request.sid)
    emit("show_fullscreen_image", "", room=request.sid)
    emit("toggle_clock", False, room=request.sid)

@socketio.on("request_instance_name")
def send_instance_name():
    emit("instance_name", APP_INSTANCE_NAME, room=request.sid)

@socketio.on("get_default_time")
def handle_get_default_time():
    minutes = load_default_time()
    emit("default_time", minutes, room=request.sid)

# 9. Socket.IO Events – Anzeige / Kommunikation
# ========================================

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

@socketio.on("save_settings")
def handle_save_settings(data):
    roomname = data.get("roomname", "").strip()
    time_minutes = int(data.get("default_time", 12))

    if roomname:
        save_room_name(roomname)
    save_default_time(time_minutes)

    global last_set_time
    last_set_time = time_minutes * 60
    if not timer_running:
        global current_time
        current_time = last_set_time
        socketio.emit("update_time", current_time)

    emit("settings_saved", {"roomname": roomname, "default_time": time_minutes}, room=request.sid)

@socketio.on("reboot")
def handle_reboot():
    try:
        threading.Thread(target=lambda: os.system("sudo /sbin/reboot")).start()
    except Exception as e:
        print(f"Reboot error: {e}")
  


# 10. Startpunkt:
# ========================================

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=PORT)