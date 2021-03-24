import os

from src.common.app_common import path_app_log
from src.config.init_config import logger


class LogService:

    def __init__(self):
        logger.info("Objeto Instânciado.")

    @classmethod
    def read_log_atual(self, nome_arquivo_log):
        logger.info("Inicio do metodo [read_log_atual]")
        if not os.path.exists(path_app_log):
            raise Exception("Diretório " + path_app_log + " não existe.")
        if not os.path.isfile(path_app_log + "/" + nome_arquivo_log):
            raise Exception("File " + nome_arquivo_log + " not found.")

        with open(path_app_log + '/' + nome_arquivo_log, 'r', encoding='ISO-8859-1') as file:
             return file.read().splitlines()