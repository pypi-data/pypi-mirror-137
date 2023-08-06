import json

from bson import json_util


class MongodbDocEncoder(json.JSONEncoder):
    """
    将json格式的题目中不符合规范的数值类型进行转换
    """

    def default(self, o):
        return json_util.default(o)
