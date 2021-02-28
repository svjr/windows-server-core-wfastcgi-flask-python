from restplus import api
from flask_restplus import Resource
from config.log_config import logger
from service.status_service import StatusService

ns_status = api.namespace('app', description='Status do Aplicativo')


@ns_status.route('/status')
class Status(Resource):

    def get(self):
        status_service = StatusService()
        logger.info("Inicio do método [get_status] via HTTP GET")
        """Retorna o status da aplicação."""
        return status_service.get_status_app()
