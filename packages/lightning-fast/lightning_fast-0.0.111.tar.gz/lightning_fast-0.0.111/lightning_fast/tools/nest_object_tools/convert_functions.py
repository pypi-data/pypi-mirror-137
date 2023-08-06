import re


def underline_to_camel(name: str) -> str:
    """
    这是一个奖下划线转为驼峰的方法
    :param name: 待转换字符串
    :return: 转换后字符串
    """
    under_pat = re.compile(r"_([0-9a-z])")
    return under_pat.sub(lambda x: x.group(1).upper(), name)
