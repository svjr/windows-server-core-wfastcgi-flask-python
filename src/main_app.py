import os
import threading

from flask import Flask, Blueprint
import werkzeug

from src.config.config import configuration
from src.monitor.monitor_memory import memory_monitor

werkzeug.cached_property = werkzeug.utils.cached_property
from src.restplus import api
from src.endpoints.log_endpoint import ns_log
from src.endpoints.status_endpoint import ns_status
from src.endpoints.model_endpoint import ns_model
from src.endpoints.auth_endpoint import ns_auth
from src.config.log_config import logger

##################################################################
# Inicialização
##################################################################

app = Flask(__name__)


@app.before_first_request
def startup():
    max_mb_upload = configuration.configuration_app.max_mb_file_upload * 1024 * 1024
    app.config['ERROR_404_HELP'] = False
    app.config['RESTPLUS_VALIDATE'] = True
    app.config['MAX_CONTENT_LENGTH'] = max_mb_upload
    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    app.register_blueprint(blueprint)
    api.add_namespace(ns_log)
    api.add_namespace(ns_status)
    api.add_namespace(ns_model)
    api.add_namespace(ns_auth)
    api.version = "0.1"
    threads = list()
    t = threading.Thread(target=memory_monitor, name="MONITOR_MEMORIA")
    threads.append(t)
    t.start()


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
    logger.info('>>>>> Starting development server at http://{}/ <<<<<'.format(app.config['SERVER_NAME']))
