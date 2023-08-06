import os
import json
from datetime import datetime, timedelta
from functools import lru_cache
from random import randint, seed
import joblib
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

from lightning_fast.config import ROOT_PATH
from lightning_fast.encoders import CommonLabelEncoder, CLabelEncoder


class BaseStatisticResult(object):
    def __init__(
        self,
        name,
        word_count,
        create_spend,
        fit_spend,
        transform_spend,
        save_spend,
        load_spend,
    ):
        self.name = name
        self.word_count = word_count
        self.create_spend = create_spend
        self.fit_spend = fit_spend
        self.transform_spend = transform_spend
        self.save_spend = save_spend
        self.load_spend = load_spend

    def to_dict(self):
        result = vars(self)
        for key in result:
            if isinstance(result[key], timedelta):
                result[key] = result[key].total_seconds()
        return result

    def __str__(self):
        result = vars(self)
        for key in result:
            result[key] = str(result[key])
        return str(json.dumps(result, indent=2))

    def __repr__(self):
        return self.__str__()


class SingleSpendStatistic(object):
    def __init__(self, test_words, tmp_file_path, encoder):
        self.test_words = test_words
        self.tmp_file_path = tmp_file_path
        self.encoder = encoder
        self.encoder_instance = None

    def get_statistic(self):
        return BaseStatisticResult(
            self.encoder_type,
            len(self.test_words),
            self.get_function_ms(self._create),
            self.get_function_ms(self._fit),
            self.get_function_ms(self._transform),
            self.get_function_ms(self._save),
            self.get_function_ms(self._load),
        )

    @classmethod
    def get_function_ms(cls, func):
        start = datetime.now()
        func()
        end = datetime.now()
        return end - start

    @property
    @lru_cache()
    def encoder_type(self):
        if self.encoder.__name__ == "LabelEncoder":
            return "scikit"
        elif self.encoder.__name__ == "CommonLabelEncoder":
            return "common"
        elif self.encoder.__name__ == "CLabelEncoder":
            return "c"
        else:
            raise TypeError("Wrong encoder type!")

    def _create(self):
        if self.encoder_type == "scikit":
            self.encoder_instance = LabelEncoder()
        elif self.encoder_type == "common":
            self.encoder_instance = CommonLabelEncoder()
        else:
            self.encoder_instance = CLabelEncoder()

    def _fit(self):
        self.encoder_instance.fit(self.test_words)

    def _transform(self):
        self.encoder_instance.transform(self.test_words)

    def _save(self):
        if self.encoder_type == "scikit":
            joblib.dump(self.encoder_instance, self.tmp_file_path)
        else:
            self.encoder_instance.save_encoder(self.tmp_file_path)

    def _load(self):
        if self.encoder_type == "scikit":
            joblib.load(self.tmp_file_path)
        elif self.encoder_type == "c":
            self.encoder_instance.load_encoder(self.tmp_file_path)
            self.encoder_instance.free_encoder()
        else:
            self.encoder_instance.load_encoder(self.tmp_file_path)

    def _del_tmp_file(self):
        os.remove(self.tmp_file_path)


class LabelEncoderComparison(object):
    tmp_c_label_encoder_path = ROOT_PATH / "tmp/c_label_encoder.tpl"
    tmp_common_label_encoder_path = ROOT_PATH / "tmp/common_label_encoder.tpl"
    tmp_scikit_label_encoder_path = ROOT_PATH / "tmp/scikit_label_encoder.tpl"

    def __init__(
        self, chars, word_min_length, word_max_length, word_count, test_words=None
    ):
        if not test_words:
            self.test_words = test_words
        else:
            self.test_words = self.generate_words(
                chars, word_min_length, word_max_length, word_count
            )

    def process(self):
        scikit_label_encoder_result = SingleSpendStatistic(
            self.test_words, self.tmp_scikit_label_encoder_path, LabelEncoder
        ).get_statistic()
        common_label_encoder_result = SingleSpendStatistic(
            self.test_words, self.tmp_common_label_encoder_path, CommonLabelEncoder
        ).get_statistic()
        c_label_encoder_result = SingleSpendStatistic(
            self.test_words, self.tmp_c_label_encoder_path, CLabelEncoder
        ).get_statistic()
        return (
            scikit_label_encoder_result,
            common_label_encoder_result,
            c_label_encoder_result,
        )

    @classmethod
    def generate_words(cls, chars, word_min_length, word_max_length, word_count):
        seed(222)
        test_words = []
        for i in range(word_count):
            sub_word = ""
            for j in range(randint(word_min_length, word_max_length)):
                sub_word += chars[randint(0, len(chars) - 1)]
            test_words.append(sub_word)
        return test_words


class VarCompareResult(object):
    bins = 50

    def __init__(
        self, chars, word_min_length, word_max_length, word_min_count, word_max_count
    ):
        self.chars = chars
        self.word_min_length = word_min_length
        self.word_max_length = word_max_length
        self.word_min_count = word_min_count
        self.word_max_count = word_max_count
        self.total_test_words = LabelEncoderComparison.generate_words(
            chars, word_min_length, word_max_length, word_max_count
        )

    def get_var_result(self):
        result = []
        for i in tqdm(
            range(
                self.word_min_count,
                self.word_max_count,
                int((self.word_max_count - self.word_min_count) / self.bins),
            )
        ):
            sub_results = LabelEncoderComparison(
                self.chars,
                self.word_min_length,
                self.word_max_length,
                i,
                self.total_test_words[0:i],
            ).process()
            result += [sub_result.to_dict() for sub_result in sub_results]
        return result

    def draw_pic(self, tmp_directory):
        columns = [
            "create_spend",
            "fit_spend",
            "transform_spend",
            "save_spend",
            "load_spend",
        ]
        result_df = pd.DataFrame(self.get_var_result())
        result_df.loc[:, "word_count"] = result_df.loc[:, "word_count"].astype(int)
        for column in columns:
            result_df.loc[:, column] = result_df.loc[:, column].astype(float)
        for column in columns:
            plt.close()
            sns.lineplot(result_df["word_count"], result_df[column], result_df["name"])
            plt.savefig(tmp_directory / f"{column}.png")


if __name__ == "__main__":
    test_chars = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王"]
    test_word_min_length = 0
    test_word_max_length = 7
    test_word_count = 600000
    # single_compare_result = LabelEncoderComparison(
    #     test_chars, test_word_min_length, test_word_max_length, test_word_count
    # ).process()
    # print(single_compare_result)
    var_compare_result = VarCompareResult(
        test_chars, test_word_min_length, test_word_max_length, 100000, test_word_count
    )
    test_tmp_directory = ROOT_PATH / "tmp/label_encoder_comparison"
    test_tmp_directory.mkdir(exist_ok=True, parents=True)
    var_compare_result.draw_pic(test_tmp_directory)
