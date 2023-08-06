import multiprocessing
import pathlib
import re
import socket
from typing import Optional

import dask
import psutil

from dask.distributed import LocalCluster, Client


class DaskConfigController:
    """
    用于生成dask一般配置的辅助类
    """

    @classmethod
    def set_local_one_thread_config(cls) -> None:
        """
        配置dask为本地单线程
        """
        dask.config.set({"scheduler": "single-threaded"})

    @classmethod
    def set_local_cluster_config(
        cls,
        tmp_directory: pathlib.Path,
        worker_count: Optional[int] = None,
        dashboard_port: int = 5000,
    ) -> None:
        """
        配置dask为本地集群模式
        :param tmp_directory: 临时文件储存位置
        :param worker_count: worker数量
        :param dashboard_port: dask进度监控端口
        """
        if worker_count is None:
            worker_count = (
                16 if multiprocessing.cpu_count() > 16 else multiprocessing.cpu_count()
            )
        else:
            worker_count = worker_count
        valid_memory_mb = psutil.virtual_memory().available >> 20
        memory_limit = int(valid_memory_mb / worker_count)
        dask.config.set(
            {
                "temporary-directory": str(tmp_directory / "dask-worker-space"),
                "memory-limit": f"{memory_limit} MB",
            }
        )
        cluster = LocalCluster(
            n_workers=worker_count, dashboard_address=f":{dashboard_port}"
        )
        Client(cluster)
        try:
            origin_ip = socket.gethostbyname(socket.gethostname())
            # noinspection HttpUrlsUsage
            origin_hostname = re.sub(
                r"^.*:", "http://" + origin_ip + ":", cluster.dashboard_link
            )
            print(
                f"\033[1;32;43m dashboard_address(origin): {origin_hostname} \033[0m!"
            )
            print(
                f"\033[1;32;43m dashboard_address(local): {cluster.dashboard_link} \033[0m!"
            )
        except socket.gaierror:
            print(
                f"\033[1;32;43m dashboard_address(local): {socket.gethostname()} \033[0m!"
            )
