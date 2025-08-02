# speechtimer  1.1.6
I would like to share my latest project: a web based speech timer that makes managing talks a breeze.  
Admin and Speechtimer run on any device that has a modern browser. (PC/Mac/Lnx/IOS/Android/Kindle etc.)  
The easiest was is to set it up on a normal Windows PC. Any Office PC/Laptop is good enough.  
**See the little video speechtimer.mp4**  
Install Python from their website, install a few addons, copy the speechtimer folder on c: and run it from there.  
On a Windows Computer this takes less than 5 minutes to install.  If you copy the Raspi image to a card and insert the card into a Raspi4, you are immediately ready to go.  
Can your rundown software send commands via HTTP? Speechtimer can also be controlled via HTTP API.  
A Streamdeck can also be used to control the timer. (API Request Plugin)  

I also have one ready to use Raspi4 image (desktop). It fits on a 16GB card. Burn it with BaleaEdger on a Micro SD Card. insert it in your Raspi and start, using it.
Use any IP scanner to find your DHCP adress of your raspi. If you are using the Waveshare PoE HAT (Typ B) – SKU: 18014 for Raspi 4, it shows the LAN DHCP IP on the little OLED display.

On the server side, it also runs on a Mac, but a new empty Windows PC without Python can be set up in a few minutes. Once Python is installed, one line is enough to install all the necessary extensions. Then copy the Speechtimer folder to C: and you can get started. On a Mac, unless it's from a developer, it takes quite a bit of extra effort. However, I managed to do it anyway, so it also runs on a Macbook. But since a Mac never displays a proper full screen in the browser without checking dozens of boxes, I wouldn't bother with it. You can get a Raspi for 50 euros, clone the image, plug it in, and start it up. Or you can get a small PC for 120 euros. Both are better options.

![Alt-Text](speechtimer1.JPG)

**Introducing SpeechTimer **
Speechtimer is a simple and easy-to-use programme for controlling a presenter's speaking time.  
The basic programme is a python script **app.py** and two HTML files, **admin.html** and **speechtimer.html**  
All these modules must run in the same network. No internet is required.  
Admin and speechtimer run on any device that has a modern browser. (PC/Mac/Lnx/IOS/Android/Kindle etc.)  
You can also start app.py several times by turning app.py into app.py2 and assigning a new instance number.  
You can change the room name in the admin console (admin.html) this will then be displayed in the TAB tabs of the browser and in the Admin Console.  
**Raspi4 Image** 10 instances are installed on the Raspi-Image and start automatically when booting. Attach a monitor, keyboard an mouse to setup your network settings easy. 
Each Insance has its own default time and Roomname, which can be changed in the admin screen. Changing the roomname requires to reboot the server (app.py)
You can activate the admin or speech timer on any device at any time, without affecting any running timer.

You install Python and the necessary extensions on your computer (PC/Mac/**Raspi***), copy the files into the speechtimer directory.   
then you start python app.py and can then access speechtimer and admin in the same network.  
The details are described in the manuals or visible in the code.  
The Raspi Images will autostart 10 Instances of the Timer (port55055 -55064)  

**For the Raspi4 you can download a larger (fits on a 16GB card) ready to use image:**  
*[Raspi4 Image links](https://drive.google.com/drive/folders/1aS9zuvYhaSjZAqpjX2A-KHDxk3yzTw-w?usp=sharing)  

**Tech Stack**  
Flask + Flask SocketIO backend in Python  
– Serves both the public timer page and the secured admin panel  
– Handles real time events (start, stop, reset, adjust time, and custom messages) via WebSockets 
– can run multiple times, just adapt the roomname und the port adress

**HTML/CSS/JS Frontend**  
start your server with python app.py  
Start your output and controls with 192.168.1.210:55055 this shows the speechtimer and 192.168.1.210:55055/admin shows the control (IP and Port Numbers are examples only)  
start your second timer with python app2.py  
Start your SECOND output and controls with 192.168.1.210:55056 this shows the speechtimer and 192.168.1.210:55056/admin shows the control (IP and Port Numbers are examples only)  

– Admin Panel (admin.html): select preset times, set custom seconds/minutes, start/stop/reset, adjust on the fly, toggle overtime, show/hide clock, send fullscreen text or images, and play/stop sound cues, change default time, change room name
– Timer Display (speechtimer.html): full screen countdown with red warning when time’s up, custom “stop speech” messages, blank screen mode, image or text overlays, and optional daytime clock in the lower right corner  

**Key Features**  
-Preset & Custom Timing: one click buttons for common durations plus manual entry  
-Dynamic Control: pause, resume, reset, and even add/subtract seconds or minutes mid timer  
-Notifications: can show a custom “Please finish your speech” alert or any free text message in fullscreen  
-Visual Aids: display images or full screen text overlays  
-Audio Cues: built in sound buttons for start/stop or custom effects, all playing through the admin-browser’s device audio output  
-Secure Admin Access: basic HTTP auth protects the control panel  
-Speechtimer.html  can run on any (multiple) device in the same network  

Whether you’re running it on a Raspberry Pi or a PC, the browser features work identically.

