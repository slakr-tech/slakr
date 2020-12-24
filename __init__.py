from views import app
from settings import *

app.config["SECRET_KEY"] = 'DEV'

if __name__ == '__main__':
    app.run(
        host = Run["HOST"],
        port = Run["PORT"],
        debug = Run["DEBUG"]
        )