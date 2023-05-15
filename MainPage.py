from flask import Flask, url_for, render_template

flask_app = Flask(__name__)
from DashBoads import statisticsPage
from NewsPage import FamiliesNewsPage


@flask_app.route('/')
def index():
    return render_template('mainPage.html')


@flask_app.route('/mainFraim')
def mainFraim():
    return render_template('mainFraim.html')


@flask_app.route('/statistics')
def statistics():
    return render_template('statisticPage.html')


@flask_app.route('/statisticsPage')
def dash_page():
    return statisticsPage.index()


@flask_app.route('/newsPage')
def newsPage():
    return render_template('Families.html')


@flask_app.route('/FamiliesNewsPage')
def FamiliesPage():
    return FamiliesNewsPage.index()


@flask_app.route('/InfoPage')
def InfoPage():
    return render_template('InfoPage.html')
