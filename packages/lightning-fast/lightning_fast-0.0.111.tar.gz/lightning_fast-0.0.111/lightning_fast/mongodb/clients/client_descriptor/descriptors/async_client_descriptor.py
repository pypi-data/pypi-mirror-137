import motor.motor_asyncio

from lightning_fast.mongodb.clients.client_descriptor.base.client_descriptor_base import (
    ClientDescriptorBase,
)


class AsyncMongodbClient(ClientDescriptorBase):
    def _create_client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        return motor.motor_asyncio.AsyncIOMotorClient(self.mongodb_url)
