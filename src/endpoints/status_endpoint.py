from src.restplus import api
from flask_restplus import Resource

ns_status = api.namespace('status', description='Status do Aplicativo')


@ns_status.route('/now')
class Status(Resource):
    def get(self):
        """Retorna o status da aplicação."""
        return {'is_ok': 'true', 'result': 'running'}
