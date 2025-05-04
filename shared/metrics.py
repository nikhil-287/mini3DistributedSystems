import psutil
import time

def get_cpu_util():
    return psutil.cpu_percent(interval=0.1) / 100.0

def get_timestamp():
    return int(time.time())
