from threading import Thread

import waitress
from app import app

from app.app import doStuff

if __name__ == "__main__":
    thread = Thread(target=doStuff, args=(10,))
    thread.start()
    waitress.serve(app, port=8041)
