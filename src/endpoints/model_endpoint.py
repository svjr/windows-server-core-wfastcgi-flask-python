import json
import os
import pandas as pd
from werkzeug.datastructures import FileStorage

from flask import request, jsonify, send_from_directory
from flask_restplus import Resource, fields

from src.common.app_common import path_app_model_uploaded, path_app_model_generated, path_app_model, \
    name_folder_generated, name_folder_uploaded
from src.config.config import configuration
from src.config.init_config import logger
from src.helper import auth_helper
from src.restplus import api
from src.service.model_service import ModelService

import traceback

ns_model = api.namespace('model', description='Operações sobre o modelo')

parser_file_data = api.parser()
parser_file_data.add_argument('arquivo', type=FileStorage, location='files', required=True)
parserFileModelUpload = api.parser()
parserFileModelUpload.add_argument('modelo', type=FileStorage, location='files', required=True)
deploy_model = api.model('Deploy', {
    'filename': fields.String(required=True, description="Nome do arquivo do modelo a ser implantado."),
})


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
            return jsonify({'is_ok': 'true', 'result': result_exec.to_dict('index')})
        except Exception as err:
            logger.error(traceback.format_exc())
            msg_err = str(err).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}


@ns_model.route('/list')
class ModelList(Resource):
    def get(self):
        """Recupera lista de todos os modelos disponíveis na pasta da aplicação (genereated e uploaded)"""
        try:
            logger.info("Inicio do metodo [ModelList] [GET]....")
            files_models = list()
            if os.path.exists(path_app_model_uploaded):
                files_uploaded = [file_json for file_json in os.listdir(path_app_model_uploaded) if
                                  (file_json.endswith('.joblib'))]
                for file_upload in files_uploaded:
                    files_models.append(name_folder_uploaded + "/" + file_upload)
            if os.path.exists(path_app_model_generated):
                files_generated = [file_json for file_json in os.listdir(path_app_model_generated) if
                                   (file_json.endswith('.joblib'))]
                for file_generated in files_generated:
                    files_models.append(name_folder_generated + "/" + file_generated)
            logger.info("Quantidade de arquivos: " + str(len(files_models)))
            return {'is_ok': 'true', 'result': str(files_models)}
        except Exception as err:
            logger.error(traceback.format_exc())
            msg_err = str(err).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}


@ns_model.route('/download')
class ModelFile(Resource):
    def get(self):
        try:
            logger.info("Inicio do metodo [ModelFile] [GET]....")

            if not os.path.exists(path_app_model):
                raise Exception("Diretório " + path_app_model + " não existe.")
            if not os.path.isfile(
                    configuration.configuration_app.path_file_symbol + "/" + configuration.configuration_app.name_file_symbol):
                raise Exception(
                    "Arquivo [" + configuration.configuration_app.path_file_symbol + "/" + configuration.configuration_app.name_file_symbol + " não encontrado")

            return send_from_directory(directory=configuration.configuration_app.path_file_symbol,
                                       filename=configuration.configuration_app.name_file_symbol,
                                       as_attachment=True)
        except Exception as err:
            logger.error(traceback.format_exc())
            msg_err = str(err).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}


@ns_model.route('/upload')
class ModelUpload(Resource):
    """Faz upload de modelo analítico"""

    # @api.doc(params={'token': {'description': 'token de autenticação','type': 'string'}})
    # @auth_helper.token_required
    @api.expect(parserFileModelUpload, validate=True)
    def post(self):
        try:
            logger.info("Inicio do metodo [ModelUpload] [POST]....")
            service_model = ModelService()
            service_model.upload_model(request)
            return {'is_ok': 'true', 'result': 'Upload Realizado com sucesso.'}
        except Exception as err:
            logger.error(traceback.format_exc())
            msg_err = str(err).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}


@ns_model.route('/deploy')
class ModelDeploy(Resource):
    @api.doc(params={'token': {'description': 'token de autenticação', 'type': 'string'}})
    @api.expect(deploy_model)
    # @auth_helper.token_required
    def post(self):
        """Implanta um determinado modelo para que seja utilizado pela aplicação"""
        try:
            logger.info("Inicio do metodo [ModelDeploy] [POST]....")
            service = ModelService()
            data = json.loads(request.data)
            filename = data.get("filename", None)
            if filename is None: return {"result": "O campo filename não foi encontrado no corpo da requisição"}
            service.deploy(filename)
            return {'is_ok': 'true', 'result': 'Deploy realizado com sucesso.'}
        except Exception as err:
            logger.error(traceback.format_exc())
            msg_err = str(err).replace("'", '"')
            return {'is_ok': 'false', 'result': str(msg_err)}
