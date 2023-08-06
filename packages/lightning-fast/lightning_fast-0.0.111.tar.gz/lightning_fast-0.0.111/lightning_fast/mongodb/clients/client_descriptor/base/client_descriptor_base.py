from abc import ABCMeta, abstractmethod
from typing import Union

import motor.motor_asyncio
from pymongo import MongoClient

from lightning_fast.config_factory.config_constructor import Config


class ClientDescriptorBase(metaclass=ABCMeta):
    """
    此描述符其宿主必须有config属性，此属性是Config的实例，
    则此描述符的行为是：
    初始化时传入config
    赋值时生成连接字符串
    引用时创建连接
    """

    def __init__(self, mongodb_name: str):
        self.mongodb_url = None
        self.mongodb_client = None
        self.mongodbs_config = None
        self.mongodb_name = mongodb_name

    def __set_name__(self, owner, name):
        """
        创建此描述符实例的时候, 直接拿宿主的config属性复制到描述符里边。
        """
        try:
            config = getattr(owner, "config")
        except AttributeError:
            raise AttributeError(f"{owner} must have 'config' attribute.")
        if not isinstance(config, Config):
            raise TypeError(f"config must be instance of Config")
        try:
            self.mongodbs_config = getattr(config, "mongodbs")
        except AttributeError:
            raise AttributeError(f"config must have 'mongodbs' attribute.")
        self._set_mongodb(self.mongodb_name)

    def __set__(self, instance, mongodb_name: str):
        """
        赋值时直接将配置中的字段名转换为mongodb连接字符串
        """
        self._set_mongodb(mongodb_name)

    def __get__(self, instance, owner):
        """
        引用的时候才会创建client
        """
        if self.mongodb_url is None:
            return self.mongodb_url
        if self.mongodb_client is None:
            self.mongodb_client = self._create_client()
        return self.mongodb_client

    @abstractmethod
    def _create_client(
        self,
    ) -> Union[MongoClient, motor.motor_asyncio.AsyncIOMotorClient]:
        pass

    def _set_mongodb(self, mongodb_name: str):
        if mongodb_name in self.mongodbs_config:
            conf = self.mongodbs_config[mongodb_name]
            if "uri" in conf:
                self.mongodb_url = conf["uri"]
            elif "user_name" in conf and "password" in conf:
                self.mongodb_url = (
                    f"mongodb://{conf['user_name']}:{conf['password']}@{conf['host']}/"
                )
            else:
                self.mongodb_url = None
        else:
            self.mongodb_url = None
