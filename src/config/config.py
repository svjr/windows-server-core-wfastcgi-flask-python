import yaml
import os
from src.common.app_common import path_app_conf
from src.config.model.application_config import ApplicationConfiguration


class Configuration:

    def __init__(self):
        self.__configuration_app = ApplicationConfiguration()
        self.__load_configuration()

    def __load_configuration(self):
        here = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.abspath(os.path.join(here, path_app_conf + '/config.yaml')), "r",
                  encoding='utf-8') as yml_file:
            cfg = yaml.safe_load(yml_file)
        self.__configuration_app.configure_build(cfg)
        self.__logging_config = os.path.abspath(os.path.join(here, path_app_conf + '/config_log.ini'))

    @property
    def configuration_app(self):
        return self.__configuration_app


configuration = Configuration()
