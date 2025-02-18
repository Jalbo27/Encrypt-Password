import inspect

def currentLine(file):
    return f"[{file}.py] {inspect.currentframe().f_back.f_lineno}: "