import subprocess
import time

# Starte alle Apps parallel
subprocess.Popen(["python3", "app.py"])
subprocess.Popen(["python3", "app2.py"])
subprocess.Popen(["python3", "app3.py"])
subprocess.Popen(["python3", "app4.py"])
subprocess.Popen(["python3", "app5.py"])
subprocess.Popen(["python3", "app6.py"])
subprocess.Popen(["python3", "app7.py"])
subprocess.Popen(["python3", "app8.py"])
subprocess.Popen(["python3", "app9.py"])
subprocess.Popen(["python3", "app10.py"])

# Halte das Skript am Leben, sonst beendet systemd den Dienst
while True:
    time.sleep(60)


