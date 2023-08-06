import inspect
import logging
import pathlib
from collections import Callable

from lightning_fast.tools.logging_tools import LoggerUtil
from lightning_fast.tools.meta_tools import SingletonMeta


class LogInjection(metaclass=SingletonMeta):
    """
    实例化此类然后调用generate_log_injection会生成一个类装饰器,
    使用此装饰器之后会将被装饰的类的__info__方法打印并保存日志,
    被装饰类的__info__方法返回字符串，之后类中所有调用__info__方法的记录都会使用logging打印。
    """

    def __init__(
        self,
        logger_name: str = None,
        logger_level: int = logging.INFO,
        log_dir: pathlib.Path = None,
    ):
        if not logger_name or not log_dir:
            self.info_logger = LoggerUtil.get_simple_logger()
        else:
            self.info_logger = LoggerUtil.get_simple_logger(
                log_dir, f"{logger_name}_info", logger_level
            )
        # self.info_logger.setLevel(logging.INFO)

    def generate_log_injection(self) -> Callable:
        def log_injection(other_cls):
            if hasattr(other_cls, "__info__"):
                origin_info_func = other_cls.__info__

                def __inject_info(*args, **kwargs):

                    if inspect.ismethod(origin_info_func):
                        # 如果是绑定方法即类方法或者普通方法
                        self.info_logger.info(origin_info_func(*args[1:], **kwargs))
                    else:
                        self.info_logger.info(origin_info_func(*args, **kwargs))

                setattr(other_cls, "__info__", __inject_info)
            return other_cls

        return log_injection
