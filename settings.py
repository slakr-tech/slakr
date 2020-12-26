import os

Run = {
    "DEBUG":True,
    "HOST":'0.0.0.0'
}

def get_port(portENV='PORT', defPort=5000):
    if os.environ.get(portENV):
        if len(os.environ[portENV]) != 4:
            return defPort
        return int(os.environ[portENV])
    return defPort


Run = {
    "DEBUG":True,
    "HOST":'0.0.0.0',
    "PORT":get_port()
}

Rules = {
    "MINIMUM_AGE":13
}

Syntax = {
    "SEP": ''.join(['-' for _ in range(50)]),
    "UNKNOWN_ERROR_TRY_AGAIN": 'An unknown error occured, please try again.',
    "UNKNOWN_ERROR": 'An unknown error occured.'
}