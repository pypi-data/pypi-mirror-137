import luigi
from luigi.contrib.hive import HivePartitionTarget


class HiveDtPartitionCheck(luigi.Task):
    """
    事实上在另一个地方: offline/variant_data_indicators/base_components/util_tasks.py
    中有类似的一个通用检查hive partition的任务。但是那里的这个类耦合比较严重, 重构留待之后
    同时继承此类与TaskBase的实现类即可

    """

    hive_path = luigi.Parameter()
    partition = luigi.Parameter()

    def run(self):
        existed = HivePartitionTarget(
            str(self.hive_path), partition={"dt": self.partition}
        ).exists()
        if existed:
            with self.output().open("w") as f:
                f.write(f"Got f{self.partition} of {self.hive_path}。")
        else:
            raise ValueError(f"Got no f{self.partition} of {self.hive_path}。")
