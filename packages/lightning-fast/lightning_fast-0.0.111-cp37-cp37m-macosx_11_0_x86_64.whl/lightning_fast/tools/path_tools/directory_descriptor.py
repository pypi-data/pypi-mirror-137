import os
import pathlib
import logging
from typing import Optional


class DirectoryDescriptor(object):
    """
    此描述器当路径存在的时候不处理，当路径不存在的时候，会创建路径
    """

    def __init__(self, directory: Optional[pathlib.Path]):
        self.directory = directory
        if directory is not None:
            self._create_if_not_existed(directory)

    def __set__(self, instance, value: pathlib.Path):
        if value is not None:
            self._create_if_not_existed(value)
            self.directory = value

    def __get__(self, instance, owner):
        return self.directory

    @classmethod
    def _create_if_not_existed(cls, directory):
        if os.path.exists(directory):
            logging.info(f"{directory}--已存在")
        else:
            logging.info(f"创建--{directory}")
            directory.mkdir(exist_ok=True, parents=True)
