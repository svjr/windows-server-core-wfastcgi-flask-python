import traceback

from src.restplus import api
from src.config.log_config import logger
from flask_restplus import Resource
from src.service.log_service import LogService

ns_log = api.namespace('log', description='Operações referentes aos Logs')


@ns_log.route('/now')
class LogActual(Resource):
    """Retorna o log atual da aplicação"""

    def get(self):
        logger.info("Requisição [LogActual] [GET] iniciada...")
        try:
            service = LogService()
            result_exec = service.read_log_atual('app.log')
            return {'is_ok': 'true', 'result': result_exec}
        except Exception as ex:
            logger.error(traceback.format_exc())
            msg_err = str(ex).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}
