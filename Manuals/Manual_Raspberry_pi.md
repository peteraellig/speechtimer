Speechtimer auf Raspi 
(starten mit einem fertigen, mit Raspi Pi Imager erstellten image -64 bit/light
In diesem Beispiel heisst der User nicht pi sondern admin. 

Raspi updaten und Python installieren

Im Terminalfenster (PuTTY):
sudo apt update
sudo apt upgrade
sudo apt install python3-pip -y
pip3 install --break-system-packages flask flask-socketio flask-httpauth eventlet

speechtimer Daten auf den Raspi kopieren

Am einfachsten ist es dann mit WinSCP deinen Python Ordner ins admin verzeichnis kopieren.
Home/admin/speechtimer
Ins Verzeichnis speechtimer wechseln
Python app.py startet den speechtimer


Autostart einrichten

Im Terminalfenster (PuTTY):
sudo nano /etc/systemd/system/speechtimer.service

diesen Text einkopieren und speichern (ohne die Striche):
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

[Unit]
Description=speechtimer Webserver
After=network.target

[Service]
User=admin
WorkingDirectory=/home/admin/speechtimer
ExecStart=/usr/bin/python3 /home/admin/speechtimer/app.py
Restart=always

[Install]
WantedBy=multi-user.target

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_


Dann diese Befehle
# (optional, bei neuen Nutzern)
sudo systemctl daemon-reload
sudo systemctl enable speechtimer.service
sudo systemctl start speechtimer.service

Speechtimer auf PC

Im Terminalfenster (PuTTY):
sudo apt update
sudo apt upgrade
sudo apt install python3-pip -y
pip3 install --break-system-packages flask flask-socketio flask-httpauth eventlet


User : admin PW: speech123

Die Installation legt user admin im home verzeichnis an.


prüfen obs läuft:
sudo systemctl status speechtimer.service
Du solltest active (running) sehen.


 http://:5050/ → Redetimer
 http://:5050/admin → Adminpanel



Ändern der statischen LAN und WLAN adresse
Im Terminalfenster (PuTTY):
sudo nano /etc/dhcpcd.conf

das sieht dann so aus und kann darin angepasst werden 
speichern mit CTRL-O – ENTER – CTRL-X:

interface eth0
static ip\_address=192.168.1.210/24
static routers=192.168.1.1
static domain\_name\_servers=192.168.1.1

interface wlan0
static ip\_address=192.168.1.211/24
static routers=192.168.1.1
static domain\_name\_servers=192.168.1.1


Ändern der SSID und user / pw
Im Terminalfenster (PuTTY):
sudo nano /etc/wpa\_supplicant/wpa\_supplicant.conf

das sieht dann so aus und kann darin angepasst werden 
speichern mit CTRL-O – ENTER – CTRL-X:

ctrl\_interface=DIR=/var/run/wpa\_supplicant GROUP=netdev
update\_config=1
country=DE

network={
 ssid="DeinWLANName"
 psk="DeinWLANPasswort"
}