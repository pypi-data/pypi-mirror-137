import pandas as pd
from dateutil.parser import parse


class SpecialDatePoints(object):
    @classmethod
    def get_month_list(cls, start_year_month: str, end_year_month: str):
        """
        返回左闭右开的所有月份，格式为%Y%m
        :param start_year_month:
        :param end_year_month:
        :return: [%Y%m]
        """
        month_list = pd.Series(
            pd.date_range(
                parse(start_year_month),
                parse(end_year_month),
                freq="m",
            )
        ).apply(lambda x: x.strftime("%Y-%m"))
        return month_list


if __name__ == "__main__":
    print(SpecialDatePoints.get_month_list("2020-02", "2020-08"))
