from views import app
from settings import Run

run_app = Run()

if __name__ == '__main__':
    app.run(
        host = run_app.host,
        port = run_app.getPort(),
        debug = run_app.debug
        )