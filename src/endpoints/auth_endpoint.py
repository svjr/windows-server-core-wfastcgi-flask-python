import traceback

from flask import jsonify

from src.restplus import api
from src.config.log_config  import logger
from flask_restplus import Resource
from src.helper.auth_helper import exec_auth

authorizations = {
    'basicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}
ns_auth = api.namespace('auth', description='Autenticação', authorizations=authorizations)


@ns_auth.route('')
class Auth(Resource):
    """Realiza login """
    @api.doc(security='basicAuth')
    def post(self):
        try:
            logger.info("Requisição [Auth] [POST] iniciada...")
            result_exec = exec_auth()
            return jsonify({'is_ok': 'true', 'result': result_exec})
        except Exception as ex:
            logger.error(traceback.format_exc())
            msg_err = str(ex).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}, 401



