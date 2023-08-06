from abc import abstractmethod
import pathlib
import re
import sys
from typing import Optional

import luigi


class TaskBase(luigi.Task):
    """
    封装luigi.Task。
    使用类相同路径在data目录下创建生成文件路径
    使用task名字与参数构建生成文件名字。
    如果想自定义文件后缀，则类中覆盖output_file_type
    此Base自行继承并复写base_dir与data_dir, 否则不可用
    """

    output_file_type = "csv"

    @property
    @abstractmethod
    def base_dir(self) -> Optional[pathlib.Path]:
        """
        返回当前项目根目录绝对路径
        :return: 项目根目录绝对路径
        """
        return None

    @property
    @abstractmethod
    def data_dir(self) -> Optional[pathlib.Path]:
        """
        返回欲保存的数据目录的绝对路径
        :return: 保存数据目录绝对路径
        """
        return None

    @property
    def environment(self) -> str:
        """
        返回环境字符串，需要改变则复写此方法
        :return: 环境字符串，比如development
        """
        return "development"

    def output_directory(self) -> Optional[pathlib.Path]:
        """
        有趣的机制，如果这里使用类方法，那么cls.__class__会指向元类。
        这是目前发现的唯一的一个类方法导致与直觉相反的情况。
        """
        if not self.base_dir or not self.data_dir:
            raise ValueError("Please imply base_dir and data_dir")
        file_type_suffix_re = re.compile(r"\.[^.\\/]*?$")
        if self.__class__ == TaskBase:
            return None
        data_dir = self.data_dir
        current_path = sys.modules[self.__class__.__module__].__file__
        current_file_path = pathlib.Path(current_path).absolute()
        current_data_dir = data_dir / current_file_path.relative_to(self.base_dir)
        current_data_dir = pathlib.Path(
            file_type_suffix_re.sub("", str(current_data_dir))
        )
        current_data_dir.mkdir(parents=True, exist_ok=True)
        return current_data_dir

    def output(self):
        output_file_name = self.__class__.__name__
        for parameter_name, parameter_value in self.to_str_params().items():
            output_file_name += "(" + parameter_name + "_" + parameter_value + ")"
        output_file_name += (
            f"(environment_{self.environment})" + f".{self.output_file_type}"
        )
        return luigi.LocalTarget(self.output_directory() / output_file_name)
