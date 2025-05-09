import inspect, time

def currentLine(file):
    time.tzset()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return f"[{timestamp}] [{file}.py] {inspect.currentframe().f_back.f_lineno}: "