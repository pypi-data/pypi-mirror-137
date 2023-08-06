from pymongo import MongoClient

from lightning_fast.mongodb.clients.client_descriptor.base.client_descriptor_base import (
    ClientDescriptorBase,
)


class SyncMongodbClient(ClientDescriptorBase):
    def _create_client(self) -> MongoClient:
        return MongoClient(self.mongodb_url, connect=False)
