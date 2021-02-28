from config.log_config import logger


class StatusService:

    def __init__(self):
        logger.info("Objeto Instânciado.")

    @classmethod
    def get_status_app(self):
        return {'status': 'running'}
