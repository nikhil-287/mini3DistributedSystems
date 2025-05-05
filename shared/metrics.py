import psutil
import time
import os
_process = psutil.Process(os.getpid())

def get_cpu_util():
    return _process.cpu_percent(interval=0.1) / 100.0

def get_timestamp():
    return int(time.time())