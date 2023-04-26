import dash
from dash import html
import flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from DashBoads import statisticsPage

server = flask.Flask(__name__)


@server.route("/")
def home():
    return "Hello, Flask!"


app1 = statisticsPage

app2 = dash.Dash(requests_pathname_prefix="/app2/")
app2.layout = html.Div("Hello, Dash app 2!")

application = DispatcherMiddleware(
    server,
    {"/app1": app1.server, "/app2": app2.server},
)

if __name__ == "__main__":
    run_simple("localhost", 8050, application)
