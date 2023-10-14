import socket
import threading
import json
from ServiceDispatcher.gui import WizardOfOzInterface
import qi
import sys
import argparse
from Utils.Message import messageManager
from ServiceDispatcher.Robot import Robot
import Tkinter as tk
from Utils.Utils import activities_running, action_dict, send, callbacks_running, isRetro

def timer_callbacks():
    for key, function in callbacks_running.items():
        function()

    threading.Timer(1.0, timer_callbacks).start()


def timer_activities():
    for key, value in activities_running.items():
        send(value.getIdResponse(), value.getResponseType(), value.getParams())

    threading.Timer(10.0, timer_activities).start()


def safe_str(obj):
    try:
        return str(obj)
    except UnicodeEncodeError:
        return obj.encode(FORMAT, 'ignore').decode(FORMAT)


def receive_request():
    while 1:
        conn, addr = server.accept()
        thread = threading.Thread(target=lambda: handle_client(conn))
        thread.start()

def handle_client(conn):
    msg_length = conn.recv(HEADER)
    msg_length = msg_length.decode(FORMAT, 'ignore')
    msg_length = safe_str(msg_length)
    y = safe_str(msg_length).split('{')
    json_string = ""
    for val in range(1, len(y)):
        json_string = json_string + "{" + y[val]
    print "RECIBIENDO"
    print json_string
    jsonObj = json.loads(json_string)
    callFunction(jsonObj)


def callFunction(jsonObj):
    print "IN CALL FUNCTION"
    function = robot.getFunction(jsonObj["methodName"])
    params = jsonObj["params"]
    params["id"] = jsonObj["id"]
    activities_running[action_dict[jsonObj["methodName"]]] = jsonObj["id"]
    if jsonObj["methodName"] == "SAY":
        isRetro["value"] = "retro" in params
    print "activities_running are" + str(activities_running)
    if not is_local:
        if "ledIntensity" in params:
            robot.set_leds_intensity("AllLeds", params["ledIntensity"])
        if "speed" in params:
            robot.factorVelocity = params["speed"]
        if "ledColor" in params:
            robot.change_led_color(params["ledColor"], 1)
        if "speechPitch" in params:
            robot.alTexToSpeech.setParameter("pitchShift", params["speechPitch"])
        if "speechSpeed" in params:
            robot.alTexToSpeech.setParameter("speed", params["speechSpeed"])
    if params is None:
        _ = function()
    else:
        _ = function(params)


HOST = '10.195.22.60'
HOST_LOCAL = '127.0.0.1'
print("Server starting on", HOST_LOCAL)
PORT = 7896
ADDR = (HOST_LOCAL, PORT)
server = None
HEADER = 10000
FORMAT = 'utf-8'
global is_local
is_local = False
session = None
app = None
if not is_local:
    # ------------------------------------------------------------------------------------------------
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.223.95", help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559, help="Naoqi port number")
    args = parser.parse_args()

    try:
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["ResPwa", "--qi-url=" + connection_url])
        app.start()
        session = app.session
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) + ".\n"
                                                                                            "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ADDR = (HOST_LOCAL, PORT)
server.bind(ADDR)
server.listen(5)
print("[STARTING] server is listening on", HOST_LOCAL)
#t = threading.Timer(10.0, timer_activities)
#t.start()

root = tk.Tk()
gui = WizardOfOzInterface(root)
print("Interface started")
robot = Robot(app, session, gui)
print("Robot Created")
robot.start()
print("Robot Started")
thread = threading.Thread(target=receive_request)
thread.start()
print("Starting main loop")
root.mainloop()
