import os
from flask_restplus import Api
from src.config.init_config import logger


def _read_description_api():
    try:
        path_api_txt = os.path.join(os.getcwd(), 'src', '', "api.txt")
        file_api = open(path_api_txt, "r", encoding='utf-8')
        desc = file_api.read()
        file_api.close()
        return desc
    except Exception as err:
        logger.error("Erro ao tentar ler descrição da API via arquivo [api.txt]. Erro=" + str(err))
        return ""


api = Api(version='0.1', title='EXECUÇÃO DE MODELO ANALÍTICO', description=_read_description_api())


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500
