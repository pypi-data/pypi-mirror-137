from abc import ABCMeta, abstractmethod

import redis

from lightning_fast.config_factory.config_constructor import Config


class PoolDescriptorBase(metaclass=ABCMeta):
    """
    此描述符其宿主必须有config属性，此属性是Config的实例，
    则此描述符的行为是：
    初始化时传入config
    赋值时生成连接字符串
    引用时创建连接
    """

    def __init__(self, redis_name: str):
        self.redis_url = None
        self.redis_client = None
        self.redis_config = None
        self.redis_name = redis_name

    def __set_name__(self, owner, name):
        """
        创建此描述符实例的时候, 直接拿宿主的config属性复制到描述符里边。
        """
        try:
            config: Config = getattr(owner, "config")
        except AttributeError:
            raise AttributeError(f"{owner} must have 'config' attribute.")
        if not isinstance(config, Config):
            raise TypeError(f"config must be instance of Config")
        try:
            self.redis_config = getattr(config, "redis")
        except AttributeError:
            raise AttributeError(f"config must have 'redis' attribute.")
        self._set_redis(self.redis_name)

    def __set__(self, instance, mongodb_name: str):
        """
        赋值时直接将配置中的字段名转换为mongodb连接字符串
        """
        self._set_redis(mongodb_name)

    def __get__(self, instance, owner):
        """
        引用的时候才会创建client
        """
        if self.redis_client is None:
            self.redis_client = self._create_pool()
        return self.redis_client

    @abstractmethod
    def _create_pool(
        self,
    ) -> redis.ConnectionPool:
        pass

    def _set_redis(self, redis_name: str):
        if redis_name in self.redis_config:
            conf = self.redis_config[redis_name]
            redis_host = conf.get("host", "127.0.0.1")
            redis_port = conf.get("port", "6379")
            redis_db = conf.get("db", 0)
            self.redis_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
        else:
            self.redis_url = None
