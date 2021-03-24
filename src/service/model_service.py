import os

from src.common.app_common import path_app_data, path_app_model_generated, path_app_model_uploaded, path_app_model
from src.config.config import configuration
from src.config.init_config import logger
from src.model.ModeloAnalitico import BaseModel
from src.util.util import print_footer, save_file_csv_from_request, save_file_model_from_request, create_syslink
from src.util.util import print_header


class ModelService:

    def __init__(self):
        logger.info("Objeto Instânciado.")

    def execute_model(self, request_received):
        print_header()
        file_data = save_file_csv_from_request(request_received=request_received,
                                               field_request="arquivo",
                                               path_folder=path_app_data,
                                               discard_files_existing=True)

        file_model = configuration.configuration_app.path_file_symbol + "/" + configuration.configuration_app.name_file_symbol
        base_model = BaseModel(file_model=file_model, file_dataframe= file_data)
        return base_model.predict()

    def upload_model(self, request_received):
        logger.info("Inicio do metodo [upload_modelo]")
        save_file_model_from_request(request_received=request_received,
                                     field_request="modelo",
                                     path_folder_upload=path_app_model_uploaded)

    def deploy(self, filename):
        logger.info("Inicio do metodo [deploy]")
        if not os.path.exists(path=configuration.configuration_app.path_file_symbol):
            logger.info(
                "Criando diretório [" + configuration.configuration_app.path_file_symbol + "] pois o mesmo não existe...")
            os.mkdir(configuration.configuration_app.path_file_symbol)

        symbol_link = configuration.configuration_app.path_file_symbol + "/" + configuration.configuration_app.name_file_symbol
        file_target = path_app_model + "/" + filename
        if not os.path.exists(file_target): raise Exception("Arquivo informado não foi encontrado.")
        create_syslink(path_syslink=symbol_link, path_file_target=file_target)
