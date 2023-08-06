from redis import ConnectionPool

from lightning_fast.redis_connection.pool.base.pool_descriptor_base import (
    PoolDescriptorBase,
)


class SyncRedisPool(PoolDescriptorBase):
    def _create_pool(self) -> ConnectionPool:
        return ConnectionPool.from_url(self.redis_url)
