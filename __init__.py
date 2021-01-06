from slakr import app
from app_settings import *
import os

secret_key = os.environ.get('chatre_encryption_key')
if not secret_key:
    secret_key = 'DEV'
app.config["SECRET_KEY"] = secret_key

if __name__ == '__main__':
    app.run(
        host = Run["HOST"],
        port = Run["PORT"],
        debug = Run["DEBUG"]
        )