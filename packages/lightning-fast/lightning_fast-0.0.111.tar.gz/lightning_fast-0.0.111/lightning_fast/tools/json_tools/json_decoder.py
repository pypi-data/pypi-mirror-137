import json
from typing import Dict

from lightning_fast.tools.json_tools.decoders.mongodb_doc_decoder import (
    MongodbDocDecoder,
)


class JsonDecoder:
    """
    json反序列化
    """

    @classmethod
    def decode_mongodb(cls, mongodb_string) -> Dict:
        """
        反序列化mongodb中的doc
        :param mongodb_string: mongodb字符串
        :return: dict
        """
        return json.loads(
            mongodb_string,
            cls=MongodbDocDecoder,
        )
