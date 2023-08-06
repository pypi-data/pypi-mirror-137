from typing import Tuple

import pandas as pd
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from dask.distributed import progress


class DaskComputer:
    """
    dask计算器
    """

    @classmethod
    def compute_local_one_thread(cls, *args: dd.DataFrame) -> Tuple[pd.DataFrame]:
        """
        使用本地单线程进行计算，添加进度条
        :param args: 被计算的表，一般为dask df
        :return: 计算结果，一般为pandas df
        """
        with ProgressBar():
            return dd.compute(*args)

    @classmethod
    def compute_local_cluster(cls, *args: dd.DataFrame) -> Tuple[pd.DataFrame]:
        """
        使用本地集群进行计算，添加进度条，生产环境下即使不使用远端集群也应该使用本地集群。
        :param args:
        :return: 计算结果，一般为pandas df
        """
        targets = [arg.persist() for arg in args]
        progress(*targets)
        return dd.compute(*targets)
