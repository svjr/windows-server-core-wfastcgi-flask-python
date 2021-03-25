import logging
import os
from logging import config as logging_config
from src.common.app_common import path_app_conf, path_app_log
from src.common.app_common import path_app_data, path_app_model
from src.common.app_common import path_app_model_uploaded, path_app_model_generated
from src.common.app_common import path_app_data_successful, path_app_data_unsuccessful


def initialize_log():
    logging.basicConfig(level=logging.DEBUG)
    logging_config.fileConfig(path_app_conf + '/config_log.ini')
    log = logging.getLogger(__name__)
    return log


def __create_directory():
    try:
        if not os.path.exists(path_app_log): os.makedirs(path_app_log)
        if not os.path.exists(path_app_data): os.makedirs(path_app_data)
        if not os.path.exists(path_app_data_successful): os.makedirs(path_app_data_successful)
        if not os.path.exists(path_app_data_unsuccessful): os.makedirs(path_app_data_unsuccessful)
        # Included models directory
        if not os.path.exists(path_app_model): os.makedirs(path_app_model)
        if not os.path.exists(path_app_model_uploaded): os.makedirs(path_app_model_uploaded)
        if not os.path.exists(path_app_model_generated): os.makedirs(path_app_model_generated)

    except Exception as ex:
        print('Erro ao realizar criação dos diretórios. Erro: %s' % (str(ex)))


__create_directory()
logger = initialize_log()
