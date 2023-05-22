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
