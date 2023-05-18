from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from DashBoads import statisticsPage
from NewsPage import FamiliesNewsPage
from MainPage import flask_app
from flask import Flask

from flask_ngrok import run_with_ngrok

application = Flask(__name__)
application.wsgi_app = DispatcherMiddleware(flask_app, {
    '/statisticsPage': statisticsPage.server,
    '/FamiliesNewsPage': FamiliesNewsPage.server,
})
run_with_ngrok(application)

if __name__ == '__main__':
    run_with_ngrok(application)
    application.run()

