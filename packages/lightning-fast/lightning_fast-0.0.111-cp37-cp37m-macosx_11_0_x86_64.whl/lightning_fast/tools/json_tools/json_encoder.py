import json
from typing import Dict

from lightning_fast.tools.json_tools.encoders.mongodb_doc_encoder import (
    MongodbDocEncoder,
)


class JsonEncoder:
    """
    json序列化
    """

    @classmethod
    def encode_mongodb(cls, mongodb_doc: Dict) -> str:
        """
        将mongodb doc序列化为json字符串
        :param mongodb_doc: mongodb 字典
        :return: str
        """
        return json.dumps(mongodb_doc, cls=MongodbDocEncoder)
