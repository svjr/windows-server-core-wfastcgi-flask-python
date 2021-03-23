from src.common.app_common import path_app_data
from src.config.log_config import logger
from src.util.util import print_footer, save_file_csv_from_request
from src.util.util import print_header


class ModelService:

    def __init__(self):
        logger.info("Objeto Instânciado.")

    def execute_model(self, request):
        print_header()

        file_data = save_file_csv_from_request(request=request,
                                               field_request="arquivo",
                                               path_folder=path_app_data,
                                               discard_files_existing=True)

        logger.info("[TODO]....")

        print_footer()
        return 0.0
