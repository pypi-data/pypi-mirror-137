import pathlib
from typing import Optional

from lightning_fast.tools.path_tools import DirectoryDescriptor


class SimpleDirectoryCollection(dict):
    """
    将config中的pathlib.Path(__file__).absolute传进来，总之这里传一个项目根目录的绝对路径进来
    """

    base_dir = DirectoryDescriptor(None)
    data_dir = DirectoryDescriptor(None)
    log_dir = DirectoryDescriptor(None)
    tmp_dir = DirectoryDescriptor(None)

    def __init__(self, base_directory: Optional[pathlib.Path]):
        if base_directory is not None:
            self.base_dir = base_directory
            self.data_dir = base_directory / "data"
            self.log_dir = base_directory / "log"
            self.tmp_dir = base_directory / "tmp"
        super().__init__()
