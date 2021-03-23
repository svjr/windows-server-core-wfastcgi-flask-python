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
            
            
@ns_model.route('/listmodels')
class ModelList(Resource):
    def get(self):
        """Recupera lista de todos os modelos disponíveis na pasta da aplicação"""
        try:
            logger.info("Inicio do metodo [ModelList] [GET]....")
            folder = configuracao_app.modelo_configuracao.path_generated
            if not os.path.exists(folder):
                return {"result": "Diretório " + folder + " não existe."}
            else:
                files = [file_json for file_json in os.listdir(folder) if (file_json.endswith('.joblib') or
                                                                           file_json.endswith('.pckl'))]
                logger.info("Quantidade de arquivos: " + str(len(files)))
                return {"modelos": files}
        except Exception as err:
            logger.error(traceback.format_exc())
            return {"result": str(err)}
