from flask import Flask, url_for, render_template

flask_app = Flask(__name__)
from DashBoads import statisticsPage as dash_app


@flask_app.route('/')
def index():
    return render_template('index.html')


@flask_app.route('/dash')
def dash_page():
    return dash_app.index()
