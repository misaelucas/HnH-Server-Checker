import os
import sys
import time
import urllib.request
from pygame import mixer
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
from datetime import datetime

# Initialize pygame mixer only if audio device is available
try:
    mixer.init()
    audio_available = True
    print("Audio device available.")
except Exception as e:
    audio_available = False
    print(f"Audio device not available. Continuing without audio. Error: {e}")

audio_path_up = 'free_alarm_stolen_from_misa.mp3'
audio_path_crashed = 'BOBERKURWA.mp3'

url = "http://www.havenandhearth.com/mt/srv-mon"

# Variables to track the server state, crash count, and crash dates
last_state = None
crash_count = 0
crash_dates = []

# Function to check the server status
def check_server_status():
    global last_state, crash_count, crash_dates
    try:
        with urllib.request.urlopen(url) as s:
            while ln := s.readline():
                words = ln.decode("ascii").split()
                if not words:
                    sys.stderr.write("haven-alarm: connected\n")
                    continue
                if words[0] == "state":
                    current_state = " ".join(words[1:])
                    if current_state != last_state:
                        if words[1] == "hafen" and words[2] == "crashed":
                            if audio_available:
                                mixer.music.load(audio_path_crashed)
                                mixer.music.play()
                            crash_count += 1
                            crash_dates.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            last_state = current_state
                            print(f"Server state changed: {current_state}")
                        elif words[1] == "hafen" and words[2] == "up":
                            if audio_available:
                                mixer.music.load(audio_path_up)
                                mixer.music.play()
                            last_state = current_state
                            print(f"Server state changed: {current_state}")
                elif words[0] == "users":
                    print(f"Current users: {words[1]}")
    except urllib.error.URLError as exc:
        sys.stderr.write(f"haven-alarm: warning: could not connect: {exc}\n")
        time.sleep(60)
        sys.stderr.write("haven-alarm: reconnecting\n")

# HTTP request handler class
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "crash_count": crash_count,
                "crash_dates": crash_dates
            }
            self.wfile.write(bytes(json.dumps(data), "utf-8"))
        else:
            self.send_error(404, "File Not Found")

# Function to run the web server
def run_server(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting web server on port {port}")
    httpd.serve_forever()

# Run the server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

while True:
    check_server_status()
    time.sleep(60)  
