import os
from functools import partial

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm

from utils.local_c_tools_compiler import LocalCToolsCompiler
from tests.time_statistic.old_encoder_statistic import (
    LabelEncoderComparison,
    SingleSpendStatistic,
)
from tests.test_config import ROOT_PATH

if len(list(os.listdir(LocalCToolsCompiler.target_dir))) == 0:
    LocalCToolsCompiler().compile_local_c_tools()

encoders = LocalCToolsCompiler.import_encoders()
CLabelEncoder = encoders.LabelEncoder
OneDStringVector = encoders.OneDStringVector

if __name__ == "__main__":
    tmp_directory = ROOT_PATH / "tmp"
    tmp_directory.mkdir(exist_ok=True, parents=True)
    test_chars = ["赵", "钱", "孙", "李", "周", "吴", "郑", "王"]
    total_test_words = LabelEncoderComparison.generate_words(test_chars, 0, 7, 6000000)
    result = []
    for i in tqdm(
        range(
            1000000,
            6000000,
            int((6000000 - 1000000) / 5),
        )
    ):
        sklearn_test_words = total_test_words[:i]
        sklearn_label_encoder = LabelEncoder()
        c_test_words = OneDStringVector(sklearn_test_words)
        c_label_encoder = CLabelEncoder()
        sk_fit_time = SingleSpendStatistic.get_function_ms(
            partial(sklearn_label_encoder.fit, sklearn_test_words)
        )
        sk_transform_time = SingleSpendStatistic.get_function_ms(
            partial(sklearn_label_encoder.transform, sklearn_test_words)
        )
        c_fit_time = SingleSpendStatistic.get_function_ms(
            partial(c_label_encoder.encode_1d, c_test_words)
        )
        c_transform_time = SingleSpendStatistic.get_function_ms(
            partial(c_label_encoder.transform_1d, c_test_words, 2)
        )
        print(
            f"sk_fit_time: {sk_fit_time}, c_fit_time: {c_fit_time}, sk_transform_time: {sk_transform_time}, c_transform_time: {c_transform_time}"
        )
        result.append([i, sk_fit_time, sk_transform_time, c_fit_time, c_transform_time])

    columns = [
        "word_count",
        "sk_fit_time",
        "sk_transform_time",
        "c_fit_time",
        "c_transform_time",
    ]
    result_df = pd.DataFrame(result, columns=columns)
    plt.close()
    result_df.plot(x="word_count")
    plt.savefig(tmp_directory / f"new_compare.png")
