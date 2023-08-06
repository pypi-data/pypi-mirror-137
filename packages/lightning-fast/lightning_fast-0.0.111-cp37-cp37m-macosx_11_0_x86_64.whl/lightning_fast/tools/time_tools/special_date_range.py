from datetime import timedelta, date
from typing import Optional

import pandas as pd
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from lightning_fast.tools.time_tools.special_date import SpecialDate


class SpecialDateRange:
    @classmethod
    def get_week_bins(cls, start_date, end_date, weeks=1):
        # 将给定的起止时间调整为开始时间向前最近的周一，结束时间向后最近的周日
        # 返回范围内的长度为weeks周的周1-周日列表
        start_week_range = pd.date_range(
            parse(start_date) - timedelta(days=6), parse(start_date)
        )
        nearest_monday = start_week_range[start_week_range.weekday == 0][0]
        end_week_range = pd.date_range(
            parse(end_date), parse(end_date) + timedelta(days=6)
        )
        nearest_sunday = end_week_range[end_week_range.weekday == 6][0]
        return pd.DataFrame(
            {
                "start_date": pd.date_range(
                    nearest_monday, nearest_sunday, freq=f"{weeks * 7}D", closed="left"
                )
                .strftime("%Y-%m-%d")
                .to_list(),
                "end_date": (
                    pd.date_range(
                        nearest_monday,
                        nearest_sunday,
                        freq=f"{weeks * 7}D",
                        closed="left",
                    )
                    + timedelta(days=weeks * 7 - 1)
                )
                .strftime("%Y-%m-%d")
                .to_list(),
            }
        )

    @classmethod
    def get_week_range_by_date(cls, some_date):
        """
        当前日期所属周范围
        :param some_date: 指定日期
        :return: 当前周1到周日
        """
        first_date = some_date - timedelta(days=some_date.weekday())
        last_date = some_date + timedelta(days=7 - some_date.weekday() - 1)
        return first_date.strftime("%Y-%m-%d"), last_date.strftime("%Y-%m-%d")

    @classmethod
    def generate_week_index(cls, start_date, end_date):
        """
        返回从开始日期到结束日期的按周分时间段
        :param start_date: 开始时间
        :param end_date: 结束时间
        :return: [(周1, 周日), ...]
        """
        date_range = pd.date_range(start_date, end_date)
        week_index = pd.Series(
            date_range.map(lambda x: x.isocalendar()[0] * 10000 + x.isocalendar()[1])
        ).rank(method="dense")
        date_week = pd.DataFrame([date_range, week_index.rank(method="dense")]).T
        bin_starts = (
            date_week.groupby(1)
            .first()[0]
            .map(lambda x: x.strftime("%Y-%m-%d"))
            .values.tolist()
        )
        bin_ends = (
            date_week.groupby(1)
            .last()[0]
            .map(lambda x: x.strftime("%Y-%m-%d"))
            .values.tolist()
        )
        return list(zip(bin_starts, bin_ends))

    @classmethod
    def get_nature_week_ranges_before_month_and_week(
        cls,
        date_require: Optional[date] = None,
        week_count_range: int = 1,
        months: int = 1,
        weeks: int = 0,
    ):
        """
        months与weeks定义需要获取的范围宽度，比如months=1, weeks=1则获取的区间长度都是1月加一周
        week_count_range定义需要从date_require前数多少周获取这个范围。
        上述参数返回值为
        [
            [last sunday - months - weeks , last sunday],
            [last sunday - months - weeks - 7, last sunday - 7],
            [last sunday - months - weeks - 14, last sunday - 14],
        ]
        :param date_require: 以哪天为基准
        :param week_count_range: 前数几周
        :param months: n月前
        :param weeks: n周前
        :return: 二维数组
        """
        if not date_require:
            date_require = date.today()
        position_date = SpecialDate.last_sunday(date_require)
        return [
            [
                (
                    position_date
                    - timedelta(days=count * 7)
                    - relativedelta(months=months)
                    - relativedelta(weeks=weeks)
                ),
                (position_date - timedelta(days=count * 7)),
            ]
            for count in range(week_count_range)
        ]


if __name__ == "__main__":
    print(SpecialDateRange.get_week_bins("2019-11-01", "2020-11-01", 1))
    print(SpecialDateRange.generate_week_index("2019-11-01", "2020-11-01"))
