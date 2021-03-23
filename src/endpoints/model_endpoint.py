import traceback

from flask import request, jsonify
from flask_restplus import Resource
from werkzeug.datastructures import FileStorage

from src.config.log_config import logger
from src.restplus import api
from src.service.model_service import ModelService

ns_model = api.namespace('model', description='Operações sobre o modelo')

parser_file_data = api.parser()
parser_file_data.add_argument('arquivo', type=FileStorage, location='files')


@ns_model.route('/execute')
class Model(Resource):
    """Processa o arquivo CSV utilizando o modelo analítico vigente"""
    @api.expect(parser_file_data)
    @api.doc(params={'arquivo': 'Arquivo contendo os dados em formato CSV'})
    def post(self):
        try:
            logger.info("Inicio do metodo [Model] [POST]....")
            service = ModelService()
            result_exec = service.execute_model(request)
            return jsonify({'is_ok': 'true', 'result': result_exec})
        except Exception as ex:
            logger.error(traceback.format_exc())
            msg_err = str(ex).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}
