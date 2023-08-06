import json
from bson import json_util


class MongodbDocDecoder(json.JSONDecoder):
    """
    mongodb中的doc使用json反序列化
    """

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self,
            object_hook=json_util.object_hook,
            object_pairs_hook=json_util.object_pairs_hook,
            *args,
            **kwargs
        )
