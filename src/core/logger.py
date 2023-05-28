import logging

from src.core.config import config


class ModuleNameFormatter(logging.Formatter):
    def format(self, record):
        record.module_name = record.name
        return super().format(record)


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module_name)s - %(message)s"
formatter = ModuleNameFormatter(LOG_FORMAT)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(config.loglevel)
