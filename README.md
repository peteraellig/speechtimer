# speechtimer  
I would like to share my latest project: a web based speech timer that makes managing presentations and talks a breeze.
![Alt-Text](speechtimer1.JPG)

**Introducing SpeechTimer **
Speechtimer is a simple and easy-to-use programme for controlling a presenter's speaking time.  
The basic programme is a python script **app.py** and two HTML files, **admin.html** and **speechtimer.html**  
All these modules must run in the same network. No internet is required.  
Admin and speechtimer run on any device that has a modern browser. (PC/Mac/Lnx/IOS/Android/Kindle etc.)  
You can also start app.py several times by turning app.py into app.py2 and assigning a new port number.  
You can enter the room name in the app instances (app.py / app2.py etc.), this will then be displayed in the TAB tabs of the browser and in the Admin Console.  
Only one timer is currently available on the Raspi image.  

You install Python and the necessary extensions on your computer (PC/Mac/**Raspi***), copy the files into the speechtimer directory.   
then you start python app.py and can then access speechtimer and admin in the same network.  
The details are described in the manuals or visible in the code. 
**For the Raspi4 you can download a ready to use image:**
*[Raspi4 Image link](https://drive.google.com/drive/folders/1aS9zuvYhaSjZAqpjX2A-KHDxk3yzTw-w?usp=sharing)

**Tech Stack**  
Flask + Flask SocketIO backend in Python  
– Serves both the public timer page and the secured admin panel  
– Handles real time events (start, stop, reset, adjust time, and custom messages) via WebSockets 

**HTML/CSS/JS Frontend**  
– Admin Panel (admin.html): select preset times, set custom seconds/minutes, start/stop/reset, adjust on the fly, toggle overtime, show/hide clock, send fullscreen text or images, and play/stop sound cues  
– Timer Display (speechtimer.html): full screen countdown with red warning when time’s up, custom “stop speech” messages, blank screen mode, image or text overlays, and optional clock in the corner  

**Key Features**  
-Preset & Custom Timing: one click buttons for common durations plus manual entry  
-Dynamic Control: pause, resume, reset, and even add/subtract seconds or minutes mid timer  
-Notifications: show a custom “Please finish your speech” alert or any free text message in fullscreen  
-Visual Aids: display images or full screen text overlays  
-Audio Cues: built in sound buttons for start/stop or custom effects, all playing through the admin-browser’s audio output  
-Secure Admin Access: basic HTTP auth protects the control panel  
-Speechtimer.html  can run on any (multiple) device in the same network  

Whether you’re running it on a Raspberry Pi or a PC, the browser driven audio/video features work identically—no extra server side audio libraries needed. Perfect for conferences, classrooms, or any live event speaking setup. 

