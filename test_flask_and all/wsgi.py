from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app1 import app as app1
from app2 import app as app2

from flask_app import flask_app
from flask_ngrok import run_with_ngrok


run_with_ngrok(flask_app)
application = DispatcherMiddleware(flask_app, {
    '/app1': app1.server,
    '/app2': app2.server,
})

if __name__ == "__main__":
    flask_app.run()
