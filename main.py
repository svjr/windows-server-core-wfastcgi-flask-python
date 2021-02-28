from flask import Flask, Blueprint
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property
from restplus import api
from endpoints.status_endpoint import ns_status
from config.log_config import logger

app = Flask(__name__)


@app.before_first_request
def startup():
    app.config['ERROR_404_HELP'] = False
    app.config['RESTPLUS_VALIDATE'] = True
    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    api.add_namespace(ns_status)
    api.version = "3.0"


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
    logger.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
