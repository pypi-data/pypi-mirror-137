import pathlib
from io import StringIO
from typing import Optional, Union, Dict

import pandas as pd
import dask.dataframe as dd


class DaskReader:
    """
    通过dask读取数据的一般工具
    """

    @classmethod
    def read_raw_hive_data(
        cls,
        file_path: Union[pathlib.Path, str],
        sep: str = "\t",
        dtype: Optional[Dict] = None,
        partitions: int = 1,
        limit: Optional[int] = None,
    ) -> dd.DataFrame:
        """
        从一般的原始hive拉取下来的csv中读取数据，通过limit控制使用dask还是pandas
        :param file_path: 文件路径
        :param sep: csv分隔符
        :param dtype: csv列的数据类型
        :param partitions: 分区数
        :param limit: 限制前limit条数据
        :return: 读取后的数据表
        """
        if limit is None:
            df = dd.read_csv(file_path, sep=sep, dtype=dtype)
        else:
            df_string = ""
            with open(file_path) as f:
                current_count = 0
                while current_count < limit:
                    df_string += f.readline()
                    current_count += 1
            df = dd.from_pandas(
                pd.read_csv(StringIO(df_string), sep=sep, dtype=dtype),
                npartitions=partitions,
            )
        return df
