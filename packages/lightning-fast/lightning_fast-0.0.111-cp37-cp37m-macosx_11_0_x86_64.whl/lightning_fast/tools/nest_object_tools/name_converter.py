from typing import Callable


class NameConverter:
    """
    这是一个把嵌套dict、list格式的对象所有key进行转换的类，常用为将一个文档转为驼峰传入前端。
    传入函数可以在convention_functions中找到
    """

    @classmethod
    def change_naming_convention(cls, origin, convert_function: Callable):
        if isinstance(origin, list):
            new_list = []
            for info in origin:
                new_list.append(cls.change_naming_convention(info, convert_function))
            return new_list
        elif isinstance(origin, dict):
            new_dict = {}
            for k, v in origin.items():
                # 这里是进行特殊key特殊处理的地方。如果遇到需要这样处理的情况再改进。
                # if k == "answers":
                #     for sub_v in v:
                #         sub_v["subAnswers"] = []
                if isinstance(v, dict):
                    new_v = cls.change_naming_convention(v, convert_function)
                elif isinstance(v, list):
                    new_v = [
                        cls.change_naming_convention(x, convert_function) for x in v
                    ]
                else:
                    new_v = v
                new_dict[convert_function(k)] = new_v
            return new_dict
        else:
            return origin
