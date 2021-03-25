import psutil
import time

from src.config.init_config import logger
from src.config.config import configuration


def memory_monitor():
    while True:
        memory_percent = psutil.virtual_memory().percent
        ram_total = int(int(psutil.virtual_memory().total) / 1024 / 1024)
        memory_swap = int(int(psutil.swap_memory().used) / 1024 / 1024)
        memory_swap_total = int(int(psutil.swap_memory().total) / 1024 / 1024)
        memory_swap_percent = psutil.swap_memory().percent

        logger.info("===> RAM total is {} MB ### "
                    "RAM usage is {} % ### "
                    "Swap total is {} MB ### "
                    "Swap usage is {} MB ### "
                    "Swap usage is {} %".format(ram_total, memory_percent, memory_swap, memory_swap_total,
                                                memory_swap_percent))

        time.sleep(configuration.configuration_app.refresh_time_monitor)
