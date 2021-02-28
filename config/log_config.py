import logging
import os
from logging import config as logging_config


def initialize_log():
    logging.basicConfig(level=logging.DEBUG)
    logging_config.fileConfig('c:/inetpub/wwwroot/config/config_log.ini')
    log = logging.getLogger(__name__)
    return log


def __create_diretorio_log():
    try:
        if not os.path.exists("c:\\app_teste\\log\\"):
            os.makedirs("c:\\app_teste\\log\\")
    except FileExistsError:
        print("Diretório [LOG] encontrado com sucesso.")


__create_diretorio_log()
logger = initialize_log()
