import pathlib
import sys
from typing import Type


class ClassDirectory:
    """
    处理class本身文件路径的辅助类
    """

    def __init__(self, class_type: Type):
        self.class_type = class_type

    def get_class_path(self) -> pathlib.Path:
        """
        获取某个class所在文件的绝对路径
        """
        class_file_path = sys.modules[self.class_type.__module__].__file__
        class_file_path = pathlib.Path(class_file_path).absolute()
        return class_file_path
