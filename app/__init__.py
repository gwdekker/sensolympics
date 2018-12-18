from threading import Thread

from flask import Flask

from app import globals
from app.main_logic import main_logic


def create_app(debug=False):
    globals.initialize()
    thread = Thread(target=main_logic, args=(10,))
    thread.start()
    my_app = Flask(__name__)

    return my_app


app = create_app()

from app import routes