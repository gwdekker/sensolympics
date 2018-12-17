from flask import Flask


def create_app(debug=False):
    app = Flask(__name__)

    return app

import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.DEBUG)

app = create_app()
