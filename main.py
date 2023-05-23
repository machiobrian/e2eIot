import os 
import time 
from datetime import datetime
import argparse
import sysmon
import aws_shadow_updater as aws_iot 

def get_aws_iot_certs(deviceID): #*******check point1
    certs_dir = os.getenv('CERTS_DIR')
    root_ca_cert = os.path.join(certs_dir, "{}AmazonRootCA1.pem".format(deviceID))
    device_cert = os.path.join(certs_dir, "{}certificate.pem.crt".format(deviceID))
    device_private_key = os.path.join(certs_dir, "{}private.pem.key".format(deviceID))

    assert os.path.exists(root_ca_cert), "Root CA certificate not found"
    assert os.path.exists(device_cert), "Device certificate not found"
    assert os.path.exists(device_private_key), "Device Private Key Not Found"

    return root_ca_cert, device_cert, device_private_key

# def get_aws_iot_certs(deviceID):
#     certs_dir = os.getenv('CERTS_DIR')
#     root_ca_cert = os.path.join(certs_dir, "systemMonitorAmazonRootCA1.pem")
#     device_cert = os.path.join(certs_dir, "systemMonitorcertificate.pem.crt")
#     device_private_key = os.path.join(certs_dir, "systemMonitorprivate.pem.key")

#     assert os.path.exists(root_ca_cert), "Root CA certificate not found"
#     assert os.path.exists(device_cert), "Device certificate not found"
#     assert os.path.exists(device_private_key), "Device Private Key Not Found"

#     return root_ca_cert, device_cert, device_private_key

def get_shadow_handler(deviceID):
    """
    Given a deviceID, create a configuration for connecting to 
    AWS IoT, it creates a returns a device_shadow_handler
    """
    # fetch the certs
    root_ca_cert, device_cert, device_private_key = get_aws_iot_certs(deviceID)
    # put the config together as a dictionary
    aws_iot_config = {
        "host": os.getenv("AWS_IOT_HOST"),
        "useWebsocket": False,
        "rootCAPath": root_ca_cert,
        "certificatePath":device_cert,
        "privateKeyPath": device_private_key,
        "thingName": deviceID
    }
    return aws_iot.init_device_shadow_handler(aws_iot_config)

def get_metrics():
    """
    Get the metrics together into an object that can be logged/sent to AWS IoT
    """
    metrics = {
        'timestamp': int(datetime.now().timestamp()),
        '%CPU_Usage': sysmon.getCpuUsagePct(),
        'CPU_Freq.': sysmon.getCpuFre(),
        'CPU_Temp.': sysmon.getCpuTemp(),
        'Total_RAM': int(sysmon.getRAMTotal()/1024/1024),
        'Used_RAM': int(sysmon.getRAMUsage()/1024/1024),
        'Available_RAM': int(sysmon.getRAMUsable()/1024/1024)
    }
    return metrics

def main(handler):
    # get sys metrics and update the device shadow
    payload = get_metrics()
    print("On device: ", payload)
    aws_iot.update_device_shadow(handler, payload)

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description="Monitor & Report System Params"
    )
    parser.add_argument(
        'interval', metavar='INTERVAL',
        type=int, help='reporting interval in sec.'
    )
    parser.add_argument(
        'deviceID', metavar='DEVICEID',
        help='id of the device.'
    )
    args = parser.parse_args()
    device_shadow_handler = get_shadow_handler(args.deviceID)

    while(1):
        main(device_shadow_handler)
        time.sleep(args.interval)
