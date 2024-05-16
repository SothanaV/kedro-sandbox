import os
import signal
import json

timeout = int(os.environ.get('PIPELINE_TIMEOUT', "60"))

def _handle_time(*args, **kwargs):
    print(f"Time out : {timeout} s")
    return None

def handle_timeout(function, args, default_value):
    signal.signal(signalnum=signal.SIGALRM, handler=_handle_time)
    signal.alarm(timeout)
    data = function(**args)
    return data if data != None else json.dumps(default_value).encode('utf-8')