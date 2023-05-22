from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json, logging, time, argparse

# custom shadow callback
def shadow_update_callback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Update request "+ token + " timeout!")
    if responseStatus == "accepted":
        payloadDict = json.load(payload)
        print("On AWS IoT: ".payloadDict.get("state").get("reported"))
    if responseStatus == "rejected":
        print("Update request " + token + " rejected")

def shadow_delete_callback(payload, responseStatus, token):
    if responseStatus == "timeout":
        print("Delete request "+ token + " timeout!")
    if responseStatus == "accepted":
        print("Delete request token: "+ token + " accepted!")
    if responseStatus == "rejected":
        print("Delete request "+ token + " rejected!")

def init_device_shadow_handler(args):
    host = args.get("host")
    rootCAPath = args.get("rootCAPath")
    certificatePath = args.get("certificatePath")
    privateKeyPath = args.get("privateKeyPath")
    port = args.get("port")
    useWebsocket = args.get("useWebsocket")
    thingName = args.get("thingName")
    clientId = args.get("clientId")

    if not clientId: # we make use of thingName if clientId is not provided
        clientId = thingName
    if useWebsocket and certificatePath and privateKeyPath:
        print("X.509 cert authentication and websocket are mutually exclusince. Pick One.")
        exit(2)
    if not useWebsocket and (not certificatePath or not privateKeyPath):
        print("Missing Credentials for Authentication.")
        exit(2)

    # port defaults
    if useWebsocket and not port:
        port = 443 # when there's no port override for WebSocket, default to 443
    if not useWebsocket and not port:
        port = 8883 # when no port override for nonwebsocket, default to 8883

    # Init AWSIoTMQTTShadowClient 
    myAWSIoTMQTTShadowClient = None 
    if useWebsocket:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(
            clientId,
            useWebsocket=True
        )
        myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
        myAWSIoTMQTTShadowClient.configureCredentials(
            rootCAPath,
            privateKeyPath,
            certificatePath
        )
    else:
        myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
        myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
        myAWSIoTMQTTShadowClient.configureCredentials(
            rootCAPath,
            privateKeyPath,
            certificatePath
        )

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    # baseReconnectQuietTime maxReconnectQuietTime, stableConnectionTime
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10) # seconds
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5) # seconds

    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()

    # create a deviceShadow json doc
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(
        thingName,
        True
    )

    # delete existing shadow JSON doc
    deviceShadowHandler._isDeleteSubscribed(shadow_delete_callback, 5)

    return deviceShadowHandler

def update_device_shadow(handler, payload):
    json_payload = json.dumps({
        "state":{
            "reported": payload
        }
    })
    handler.shadowUpdate(json_payload, shadow_update_callback, 5)