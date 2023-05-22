import psutil
import os # for temp purposes

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