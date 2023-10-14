import json
from datetime import datetime
from socket import socket, AF_INET, SOCK_STREAM


activities_running = {}
callbacks_running = {}

action_dict ={"SAY":"talk",
              "SHOWVIDEO":"showVideo",
              "RUNANIMATION":"runAnimationResponse",
              "KILLALL":"stopAnimationResponse",
              "SHOWIMG":"showImage",
              "HIDEIMG":"hideImage",
              "QUITVIDEO":"quitVideo",
              "STOPALL":"noTalk"}

animation_task_dict = {}

responsesXTime = dict()
isRetro = {"value":False}


def json_creator(id_response, function_type ,responseType, params):
    params["userID"] = "0"
    json_string = {
        "primitiveID": id_response,
        "action": function_type,
        "robotData": {
            "function": function_type,
            "service":responseType,
            "parameters":params
            }
    }
    return json.loads(json.dumps(json_string))


def send(id_response, responseType, function_type, params, block=True):
    HOST_LOCAL = '127.0.0.1'
    PORTS = {"INTERFACEEVENT":53152,"MAIL":53153,"ROBOT_RESOURCES":53154,"MOVEMENT":53155,"EMOTIONEXTRACTOR":53156,"RAWVIDEO":53157,"SPEECHENGINE":53158,"SENTIMENTANALYSIS":53159}
    should_send_message = True
    port = PORTS[responseType]
    if should_send_message or (block is False):
        ADDR = (HOST_LOCAL, port)
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(ADDR)
        msg_to_send = json.dumps(json_creator(id_response,function_type,responseType, params))
        if "getUserEmotions" not in msg_to_send:
            print "send ", msg_to_send

        client.send(msg_to_send + '\r\n')
        client.close()

def isAnEmotionalAck(params):
    encontrado = False
    emotionalAck = [
        "peopleDetected",
        "personStopsLookingAtRobot",
        "personMovedAway",
        "speechDetected"
    ]
    for i in emotionalAck:
        if params.__contains__(i):
            encontrado = True

    return encontrado

def checkTimeMessageSended(params):
    isCorrectToSend = True
    if (responsesXTime.get(params).hour - datetime.now().hour) < 1:

        if (responsesXTime.get(params).minute - datetime.now().minute) < 2:

            if (abs(datetime.now().second - responsesXTime.get(params).second)) < 5:
                isCorrectToSend = False

            if (abs(datetime.now().second - responsesXTime.get(params).second)) > 20:
                isCorrectToSend = False
                deleteExpiredAction( params )

    return isCorrectToSend

def deleteExpiredAction( expiredAction ):
    if activities_running and (expiredAction in activities_running):
        activities_running.pop( expiredAction )