from datetime import date, timedelta
from typing import Optional

from dateutil.relativedelta import relativedelta


class SpecialDate(object):
    @classmethod
    def _offset_by_one_week(cls, date_require: date, offset: int) -> date:
        """
        获取某天往前看的最近的星期n
        :param date_require 从哪一天开始往前看
        :param offset 1 周日 2 周六 3 周五 4 周四 5 周三 6 周二 7 周一
        """
        today = date.today() if not date_require else date_require
        offset = today.weekday() + offset
        return today - timedelta(days=offset)

    @classmethod
    def last_sunday(cls, date_require: date) -> date:
        """
        获取某天上一周的周日
        :param date_require: 某天
        :return: date
        """
        return cls._offset_by_one_week(date_require, 1)

    @classmethod
    def sunday_before_n_weeks(cls, require_day: date, weeks: int) -> date:
        """
        获取n周前的周日
        :param require_day: 某天
        :param weeks: 周数
        :return: date
        """
        return cls.last_sunday(require_day) - relativedelta(weeks=weeks)


if __name__ == "__main__":
    date_util = SpecialDate.sunday_before_n_weeks(date.today(), 0)
    print(date_util)
