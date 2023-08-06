import logging
import pathlib
from logging import handlers
from typing import Optional


class LoggerUtil(object):
    """
    使用此类生成一个简单的logger。此logger可以将log分文件打印并保存。
    """

    @classmethod
    def get_simple_logger(
        cls,
        log_path: Optional[pathlib.Path] = None,
        log_file_name: Optional[str] = None,
        logger_level: Optional[int] = None,
    ) -> logging.Logger:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        logger_level = logging.INFO if not logger_level else logger_level
        if not log_path or not log_file_name:
            logger = logging.getLogger()
        else:
            # log_path.mkdir(parents=True, exist_ok=True)
            logger = logging.getLogger(log_file_name)
            fh = handlers.RotatingFileHandler(
                log_path / f"{log_file_name}.log",
                maxBytes=10240 * 1000,
                backupCount=5,
            )
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)
        logger.setLevel(logger_level)
        return logger
