from flask import Flask, Blueprint, render_template
from sqlalchemy import create_engine

from prometheus_client import make_wsgi_app, Summary
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics

import os


#
# Constants
#
CONFIG = {"version": "v0.1.2", "config": "staging"}
MAIN = Blueprint("main", __name__)


db_name = os.getenv('POSTGRES_DB', 'test')
db_user = os.getenv('POSTGRES_USER', 'test')
db_pass = os.getenv('POSTGRES_PASSWORD', 'test')
db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_HOST_PORT', '5432')
# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

@MAIN.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', name = 'Docker', registros = get_rows_count() )


# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('python_web_get_records_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def get_rows_count():
    query = "SELECT COUNT(*) FROM numbers"
    result_set = db.execute(query)
    for (r) in result_set:
        return r[0]


#if __name__ == '__main__':
    # Prometheus - Start up the server to expose the metrics.
    #start_http_server(8071)

    # Iniciar Flask
    # https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
    # app.run(debug=True, host='app-web', port=6500)
    #app.run(debug=True,host='0.0.0.0', port=6500)

    # provide app's version and deploy environment/config name to set a gauge metric
    #register_metrics(app, app_version="v0.1.2", app_config="staging")

    # Plug metrics WSGI app to your main app with dispatcher
    #dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

    #run_simple(hostname="0.0.0.0", port=6500, application=dispatcher)


def register_blueprints(app):
    # Register blueprints to the app
    app.register_blueprint(MAIN)


def create_app(config):
    # Application factory

    app = Flask(__name__)
    register_blueprints(app)
    register_metrics(app, app_version=config["version"], app_config=config["config"])
    return app


#
# Dispatcher
def create_dispatcher() -> DispatcherMiddleware:
    # App factory for dispatcher middleware managing multiple WSGI apps
    main_app = create_app(config=CONFIG)
    return DispatcherMiddleware(main_app.wsgi_app, {"/metrics": make_wsgi_app()})


#
# Run
if __name__ == "__main__":
    run_simple(
       "0.0.0.0",
       6500,
       create_dispatcher(),
       use_reloader=True,
       use_debugger=True,
       use_evalex=True,
    )