from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app1 import app as app1
from app2 import app as app2
from flask_app import flask_app
from flask import Flask

from flask_ngrok import run_with_ngrok

application = Flask(__name__)
application.wsgi_app = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    '/app2': app2.server,
})
run_with_ngrok(application)

if __name__ == '__main__':
    application.run()
