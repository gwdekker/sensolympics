from threading import Thread

from flask import Flask

from app.app import doStuff
import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)



def create_app(debug=False):
    logger.info("Starting app - before thread")
    thread = Thread(target=doStuff, args=(10,))
    thread.start()
    logger.info("Starting app - after thread")
    app = Flask(__name__)
    logger.info("Starting app - ready!")

    return app

app = create_app()
