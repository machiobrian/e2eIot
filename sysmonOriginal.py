import psutil
import os # for temp purposes
import time 
import argparse

def getCpuUsagePct():
    return psutil.cpu_percent(
        interval=0.5
    )
def getCpuFre():
    return int(psutil.cpu_freq().current
    )
def getCpuTemp():
    result = 0.0
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
            if line.isdigit(): # test is the string is an integer
                result = float(line)/1000 # convert to temp-float in degrees
            return result
def getRAMUsage():
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)
def getRAMTotal():
    return int(psutil.virtual_memory().total)
def getRAMUsable():
    return int(psutil.virtual_memory().available)
def getRAMUsagePct():
    return psutil.virtual_memory().percent
def getSwapUsage():
    return psutil.swap_memory().used
def getSwapTotal():
    return psutil.swap_memory().total
def getSwapPct():
    return psutil.swap_memory().percent

# the loop runs infinitely, a payload dictionary containing
# device param information, timestamps and deviceID

def main(interval, deviceID):
    # the function is to run every x seconds
    while True:
        payload = {
            'timestamp': int(time.time()),
            'deviceID': deviceID,
            '% CPU Usage': getCpuUsagePct(),
            'CPU Freq.': getCpuFre(),
            'CPU Temp.': getCpuTemp(),
            'Total RAM': int(getRAMTotal()/1024/1024),
            'Used RAM': int(getRAMUsage()/1024/1024),
            'Available RAM': int(getRAMUsable()/1024/1024)
        }
        print(payload)
        time.sleep(interval)
    ...
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='System Monitor')
    parser.add_argument('--interval', 
                        type=int, 
                        default=5, 
                        help='Interval (seconds)')
    parser.add_argument('--deviceID',
                        type=str,
                        default='IoTDevice',
                        help='Device ID')
    args = parser.parse_args()
    main(args.interval, args.deviceID)