import os
import re
from functools import wraps

import luigi
from dateutil.parser import parse


"""
本页decorator务必配合task_bask使用，因为task_base有固定的文件名格式
"""


def delete_task_before_start_date(save_path_keywords: str, protect_end_date: str):
    """
    根据start_date字段，删除保护日期之后，当前之前的输出文件。task路径中
    luigi.Task继承类中必须含有start_date与end_date.
    文件名eg. SpeechRecognitionEvaluationTask(target_type_target_text_start_date_2020-11-02).csv
    :param save_path_keywords 保存路径（文件夹目录，不是文件路径）中含有的特殊字符串，防止误删除
    :param protect_end_date 保护日期（日期格式可以parse即可），保护日期与其之前的文件不会被删除
    """

    def decorate(run):
        @wraps(run)
        def wrapper(self: luigi.Task):
            try:
                start_date = getattr(self, "start_date")
            except AttributeError:
                raise AttributeError("Must had start_date attribute")
            parent_path = os.path.abspath(os.path.join(self.output().path, os.pardir))
            if save_path_keywords not in parent_path:
                raise ValueError("欲删除目录有误，请检查代码以防误删文件")
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            for file in os.listdir(parent_path):
                valid_file = True
                if file.startswith("."):
                    valid_file = False
                if not valid_file:
                    continue
                # eg. SpeechRecognitionEvaluationTask(target_type_target_text_start_date_2020-11-02).csv
                start_date_raw = re.search(r"(start_date_.*?)[)_]", file).group(1)
                if not start_date_raw:
                    continue
                else:
                    start_date_str = start_date_raw.split("_")[-1]
                end_date_raw = re.search(r"(end_date_.*?)[)_]", file).group(1)
                if not end_date_raw:
                    continue
                else:
                    end_date_str = end_date_raw.split("_")[-1]
                try:
                    parsed_start_date = parse(start_date_str)
                    parsed_end_date = parse(end_date_str)
                except ValueError:
                    continue
                if parsed_end_date <= parse(protect_end_date):
                    continue
                else:
                    if parsed_end_date < parse(
                        str(start_date)
                    ) and parsed_start_date < parse(str(start_date)):
                        os.remove(os.path.join(parent_path, file))
            return run(self)

        return wrapper

    return decorate


def delete_task_before_date(save_path_keywords: str, protect_end_date: str):
    """
    根据date字段，删除保护日期之后，当前之前的输出文件。task路径中
    luigi.Task继承类中必须含有date.
    文件名eg. SpeechRecognitionEvaluationTask(target_type_target_text_date_2020-11-02).csv
    :param save_path_keywords 保存路径（文件夹目录，不是文件路径）中含有的特殊字符串，防止误删除
    :param protect_end_date 保护日期（日期格式可以parse即可），保护日期与其之前的文件不会被删除
    """

    def decorate(run):
        @wraps(run)
        def wrapper(self: luigi.Task):
            try:
                date = getattr(self, "date")
            except AttributeError:
                raise AttributeError("Must had date attribute")
            parent_path = os.path.abspath(os.path.join(self.output().path, os.pardir))
            if save_path_keywords not in parent_path:
                raise ValueError("欲删除目录有误，请检查代码以防误删文件")
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            for file in os.listdir(parent_path):
                valid_file = True
                for name, parameter in self.param_kwargs.items():
                    if name != "date" and str(parameter) not in file:
                        valid_file = False
                if not valid_file:
                    continue
                # eg. SpeechRecognitionEvaluationTask(target_type_target_text_date_2020-11-02).csv
                date_raw = re.search(r"(date_.*?)[)_]", file).group(1)
                if not date_raw:
                    continue
                else:
                    date_str = date_raw.split("_")[-1]
                try:
                    parsed_date = parse(date_str)
                except ValueError:
                    continue
                if parsed_date <= parse(protect_end_date):
                    continue
                if parsed_date < parse(str(date)):
                    os.remove(os.path.join(parent_path, file))
            return run(self)

        return wrapper

    return decorate
